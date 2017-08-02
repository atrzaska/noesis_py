#this is a super-half-assed UE4 importer implementation, with explicit serialization for better tracking. it's here to provide a base to dig further into
#customized-engine UE4 content, but it will not be maintained and will certainly break frequently with new UE4 releases. if you want UE3 compatibility or
#something more complete and actively maintained, use gildor's umodel. to avoid butthurt through inference - this script was not based on umodel at all, but
#later incorporated a bunch of gildor's version hacks in preference to scouring through version history, which also resulted in some light reorganization.
#said version hacks are probably at varying levels of parity with umodel. plenty of changes have been made to umodel versioning logic since then as well,
#as some of it didn't appear to be working with what looked to be UE4 stock (in terms of serialization) test data from some VIVE demos. thanks to gildor
#for his versioning logic, although his serialization generally looks 1:1 with stock UE4 code and uses identical object names, so we shouldn't pretend any
#of this required any reverse engineering or "research"!

from inc_noesis import *
import os

#registerNoesisTypes is called by Noesis to allow the script to register formats.
#Do not implement this function in script files unless you want them to be dedicated format modules!
def registerNoesisTypes():
    handle = noesis.register("UE4 Archive", ".pak")
    noesis.setHandlerExtractArc(handle, ue4ExtractArc)
    
    handle = noesis.register("UE4 Asset", ".uasset")
    noesis.setHandlerTypeCheck(handle, ue4CheckType)
    noesis.setHandlerLoadModel(handle, ue4LoadModel)
    noesis.addOption(handle, "-ue4serialver", "force serialization version to <arg>.", noesis.OPTFLAG_WANTARG)
    noesis.addOption(handle, "-ue4gamehack", "force gamehack to <arg>. see UE4_GAMEHACK_*.", noesis.OPTFLAG_WANTARG)
    noesis.addOption(handle, "-ue4tex1dthin", "force texture untiling.", 0)
    noesis.addOption(handle, "-ue4defaultmtl", "force default material names.", 0)
    noesis.addOption(handle, "-ue4nosecname", "don't name meshes by section.", 0)
    noesis.addOption(handle, "-ue4bidx", "name bones by index.", 0) #apparently ue4 allows identically-named bones
    noesis.addOption(handle, "-ue4datapath", "scan <arg> recursively for export data.", noesis.OPTFLAG_WANTARG)

    return 1
        

UE4_GAMEHACK_NONE = 0
UE4_GAMEHACK_T7 = 1
        
class UE4Asset:
    def __init__(self, bs):
        self.bs = bs
        
    def parse(self):
        try:
            bs = self.bs
            id = bs.readUInt()
            if id != 0x9E2A83C1:
                if id == 0xC1832A9E:
                    bs.setEndian(NOE_BIGENDIAN)
                else:
                    return -1
            self.version = bs.readInt()
            #this support/script is pretty half-assed (not a complete implementation, just here to update as needed in order to get at select data), so i'm not supporting a whitelist.
            #at the time of this writing, i'm loading version -7, 0, 0, 0 files.
            if self.version >= 0:
                return -1
            self.verA = bs.readInt()
            self.verB = bs.readInt()
            self.verLic = bs.readInt()
            self.versionList = ue4ReadList(self, UE4VersionType)
            
            self.gameHack = UE4_GAMEHACK_NONE
            if noesis.optWasInvoked("-ue4gamehack"):
                self.gameHack = int(noesis.optGetArg("-ue4gamehack"))
                
            if self.gameHack == UE4_GAMEHACK_T7:
                self.serialVersion = 508
            elif noesis.optWasInvoked("-ue4serialver"):
                self.serialVersion = int(noesis.optGetArg("-ue4serialver"))
            else:
                self.serialVersion = self.verB & 0xFFFF
                if self.serialVersion == 0:
                    if self.version < -7:
                        self.serialVersion = 511 #currently assume -8
                    elif self.version == -6:
                        self.serialVersion = 498
                    elif self.version == -5 or self.version == -4:
                        self.serialVersion = 434
                    else:
                        self.serialVersion = 508 #assume version -7

            self.headersSize = bs.readInt()

            self.packageGroup = ue4ReadString(self)
            self.packageFlags = bs.readInt()

            self.namesCount = bs.readInt()
            self.namesOffset = bs.readInt()
            
            if self.serialVersion >= 459:
                self.gatherableTextDataCount = bs.readInt()
                self.gatherableTextDataOffset = bs.readInt()

            self.exportCount = bs.readInt()
            self.exportOffset = bs.readInt()
            self.importCount = bs.readInt()
            self.importOffset = bs.readInt()
            self.dependsOffset = bs.readInt()

            if self.serialVersion >= 384:
                self.assetStringRefCount = bs.readInt()
                self.assetStringRefOffset = bs.readInt()
            if self.serialVersion >= 510:
                bs.readInt() #searchableNamesOffset

            self.thumbnailTableOffset = bs.readInt()

            self.guid = UE4Guid(self)
            
            self.generations = ue4ReadList(self, UE4GenerationInfo)
            if self.serialVersion >= 336:
                self.engineVersion = UE4EngineVersion(self)
            if self.serialVersion >= 444:
                self.compatVersion = UE4EngineVersion(self)
            
            self.compressionFlags = bs.readInt()
            self.compressionChunks = ue4ReadList(self, UE4CompressedChunk)
            
            self.pkgSource = bs.readInt()
            self.cookPackages = ue4ReadList(self, UE4String)
            
            if self.serialVersion < 508:
                bs.readInt() #numTextureAllocations
            
            if self.serialVersion >= 112:
                self.assetRegistryOffset = bs.readInt()
            if self.serialVersion >= 212:
                self.bulkDataOffset = bs.readInt()
            else:
                self.bulkDataOffset = 0
        except:
            return -1
        
        return 0
        
    def getName(self, index):
        if index >= 0 and index < len(self.names):
            name, flags = self.names[index]
            return name
        return None
        
    def getImportExportName(self, index):
        if index < 0:
            index = -index
            if index > 0 and index <= len(self.imports):
                return repr(self.imports[index - 1].objectName)
        elif index > 0:
            if index > 0 and index <= len(self.exports):
                return repr(self.exports[index - 1].objectName)
        return "None"
        
    def getVersionByGuid(self, guid):
        for version in self.versionList:
            if version.key == guid:
                return version.version
        return -1
        
    def getRenderingObjectVersion(self):
        guid = UE4Guid.fromValue(0x12F88B9F, 0x88754AFC, 0xA67CD90C, 0x383ABD29)
        ver = self.getVersionByGuid(guid)
        if ver < 0:
            if self.serialVersion < 504:
                return 0
            elif self.serialVersion <= 504:
                return 2
            elif self.serialVersion <= 505:
                return 4
            elif self.gameHack == UE4_GAMEHACK_T7:
                return 9
            elif self.serialVersion <= 510:
                return 12
            return 15

    def getEditorObjectVersion(self):
        guid = UE4Guid.fromValue(0xE4B068ED, 0xF49442E9, 0xA231DA0B, 0x2E46BB41)
        ver = self.getVersionByGuid(guid)
        if ver < 0:
            if self.serialVersion < 504:
                return 0
            elif self.serialVersion <= 504:
                return 2
            elif self.serialVersion <= 505:
                return 6
            elif self.serialVersion <= 508:
                return 8
            elif self.serialVersion <= 510:
                return 14
            return 15
            
    def getSkeletalMeshVersion(self):
        guid = UE4Guid.fromValue(0xD78A4A00, 0xE8584697, 0xBAA819B5, 0x487D46B4)
        ver = self.getVersionByGuid(guid)
        if ver < 0:
            if self.serialVersion < 505:
                return 0
            elif self.serialVersion <= 505:
                return 4
            elif self.serialVersion <= 508:
                return 5
            elif self.serialVersion <= 510:
                return 7
            return 10

    def getRecomputeTangentVersion(self):
        guid = UE4Guid.fromValue(0x5579F886, 0x933A4C1F, 0x83BA087B, 0x6361B92F)
        ver = self.getVersionByGuid(guid)
        if ver < 0:
            if self.serialVersion < 504:
                return 0
            return 1
                        
    def getExportableObjectByName(self, exportName):
        for object in self.serializedObjects:
            export = noeSafeGet(object, "exportEntry")
            if export and repr(export.objectName) == exportName:
                return object
        return None
                        
    def loadTables(self):
        bs = self.bs
        self.names = []
        self.imports = []
        self.exports = []
        if self.namesCount > 0:
            bs.seek(self.namesOffset, NOESEEK_ABS)
            for nameIndex in range(0, self.namesCount):
                name = ue4ReadString(self)
                flags = bs.readInt() if self.serialVersion >= 504 else 0
                self.names.append((name, flags))
        if self.importCount > 0:
            bs.seek(self.importOffset, NOESEEK_ABS)
            for importIndex in range(0, self.importCount):
                self.imports.append(UE4ImportObject(self))
        if self.exportCount > 0:
            bs.seek(self.exportOffset, NOESEEK_ABS)
            for exportIndex in range(0, self.exportCount):
                self.exports.append(UE4ExportObject(self))

    def loadAssetData(self):
        #todo - support compression? would usually be pointless in practice to compress cooked uassets (package-level or native platform compression), so might not be common
        bs = self.bs
        self.textures = []
        self.meshes = []
        self.serializedObjects = []
        for export in self.exports:
            className = self.getImportExportName(export.classIndex)
            print("Examining export", className, "-", export.objectName)
            if className in ue4LoaderDict:
                bs.seek(export.serialOffset, NOESEEK_ABS)
                newObject = ue4LoaderDict[className](self)
                newObject.load(export)
                self.serializedObjects.append(newObject)
        for object in self.serializedObjects:
            object.postLoad()
                    
    def transferTextures(self, noeTextures):
        if len(self.textures) > 0:
            for uTexture in self.textures:
                if uTexture.texture:
                    uTexture.noeTextureIndex = len(noeTextures)
                    noeTextures.append(uTexture.texture)    

                    
#=================================================================
# UObject implementations
#=================================================================
        
class UE4Object:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
    def load(self, export):
        bs = self.asset.bs
        self.exportEntry = export
        self.propTags = {}
        while not bs.checkEOF():
            propTag = UE4PropertyTag(self.asset)
            if propTag.name.lower() == "none":
                break
            self.propTags[propTag.name.lower()] = propTag
        if bs.readInt():
            self.objectGuid = UE4Guid(self.asset)
    def postLoad(self):
        pass
    def findPropertyTagByName(self, tagName):
        lTagName = tagName.lower()
        if lTagName in self.propTags:
            return self.propTags[lTagName]
        return None

class UE4StaticMesh(UE4Object):
    def __init__(self, asset):
        super().__init__(asset)
    def load(self, export):
        super().load(export)
        asset = self.asset
        bs = asset.bs

        stripFlags = UE4StripFlags(asset)
        isCooked = bs.readInt() != 0

        if not stripFlags.isEditorDataStripped():
            print("Unstripped StaticMesh is unimplemented.")
            return
        elif not isCooked:
            print("Uncooked StaticMesh is unimplemented.")
            return
        
        self.refSkeleton = None
        
        self.bodySetupRef = UE4ObjectRef(asset)
        if asset.gameHack != UE4_GAMEHACK_T7:
            self.navCollisionRef = UE4ObjectRef(asset)
        
        #if not stripFlags.isEditorDataStripped():
        #    UE4String(asset)
        #    bs.readUInt()
            
        self.lightingGuid = UE4Guid(asset)
        self.sockets = ue4ReadList(asset, UE4ObjectRef)

        self.lods = ue4ReadList(asset, UE4StaticModelLOD)
        
        if asset.serialVersion >= 394:
            stripVolumeData = False
            if asset.serialVersion >= 416:
                stripFlags = UE4StripFlags(asset)
                stripVolumeData = stripFlags.isRenderDataStripped()
            if not stripVolumeData:
                for lodIndex in range(0, len(self.lods)):
                    if bs.readInt() != 0:
                        UE4DistanceFieldVolumeData(asset)

        self.bounds = UE4BoxSphereBounds(asset)
        bs.readInt() #LODsShareStaticLighting
        
        if asset.serialVersion < 508:
            bs.readInt() #simplygon flag
            
        renderVer = asset.getRenderingObjectVersion()
        if renderVer < 10:
            #streaming texture factors
            bs.readFloat()
            bs.readFloat()
            bs.readFloat()
            bs.readFloat()
            bs.readFloat()
            bs.readFloat()
            bs.readFloat()
            bs.readFloat()
            bs.readFloat()
        
        maxLods = 8 if asset.serialVersion >= 482 else 4
        for lodIndex in range(0, maxLods):
            bs.readFloat()
            
        self.materials = []
        
        hasStaticMaterials = False
        if asset.serialVersion >= 508:
            hasSpeedTreeData = bs.readInt() != 0
            if hasSpeedTreeData:
                print("Warning: SpeedTree parsing unimplemented.")
            else:
                if asset.getEditorObjectVersion() >= 8:
                    self.materials = ue4ReadList(asset, UE4StaticMaterial)
                    hasStaticMaterials = len(self.materials) > 0
                    
        if not hasStaticMaterials:
            #if necessary, yank them out of properties
            if len(self.materials) == 0:
                materialArrayProp = self.findPropertyTagByName("Materials")
                if materialArrayProp:
                    matInstNameList = materialArrayProp.readProperty()
                    for matName in matInstNameList:
                        self.materials.append(UE4LegacyMaterial(asset, matName))
        
        asset.meshes.append(self)
            
class UE4SkeletalMesh(UE4Object):
    def __init__(self, asset):
        super().__init__(asset)
    def load(self, export):
        super().load(export)
        asset = self.asset
        stripFlags = UE4StripFlags(asset)
        self.bounds = UE4BoxSphereBounds(asset)
        self.materials = ue4ReadList(asset, UE4SkeletalMaterial)
        self.refSkeleton = UE4RefSkeleton(asset)
        self.lods = ue4ReadList(asset, UE4SkeletalModelLOD, self)
        
        self.asset.meshes.append(self)
            
class UE4Texture(UE4Object):
    def __init__(self, asset):
        super().__init__(asset)
    def load(self, export):
        super().load(export)
        stripFlags = UE4StripFlags(self.asset)
        if not stripFlags.isEditorDataStripped():
            self.sourceArt = UE4ByteBulkData(self.asset)
            
        self.texture = None
        self.noeTextureIndex = -1
        self.asset.textures.append(self)
        
class UE4Texture2D(UE4Texture):
    def __init__(self, asset):
        super().__init__(asset)
    def load(self, export):
        super().load(export)
        bs = self.asset.bs
        
        UE4StripFlags(self.asset)
        isCooked = bs.readInt() != 0
        if isCooked:
            pixelFormat = repr(UE4Name(self.asset))
            while pixelFormat.lower() != "none":
                dataSize = bs.readInt()
                if self.texture is None:
                    width = bs.readInt()
                    height = bs.readInt()
                    depth = bs.readInt()
                    imagePixelFormat = repr(UE4String(self.asset))
                    firstMip = bs.readInt()
                    mips = ue4ReadList(self.asset, UE4Texture2DMip)
                    if len(mips) > 0:
                        #textureData = bytearray()
                        #for mip in mips:
                        #    textureData += mip.bulkData.readData()
                        #for now, just take mip 0. although generally we could just do the above for windows, other platforms will have a variety of alignment/packing rules.
                        textureData = mips[firstMip].bulkData.readData()
                        if textureData:
                            mipWidth = mips[firstMip].width
                            mipHeight = mips[firstMip].height
                            textureData, noeFormat = ue4ConvertTextureData(mipWidth, mipHeight, textureData, imagePixelFormat)
                            if textureData:
                                self.texture = NoeTexture(repr(export.objectName) if export else "ue4tex", mipWidth, mipHeight, textureData, noeFormat)
                                self.texture.uTexture = self
                else:
                    if dataSize <= 0:
                        break
                    bs.seek(dataSize, NOESEEK_REL)
                pixelFormat = repr(UE4Name(self.asset))
        else:
            print("Warning: Uncooked texture data unimplemented.")
        
#currently, this is used generically for all material instance objects. we only care about digging props out.
class UE4MaterialInstance(UE4Object):
    def __init__(self, asset):
        super().__init__(asset)
    def load(self, export):
        super().load(export)
        self.parentObject = None
        self.parentInstance = None
        parentTag = self.findPropertyTagByName("Parent")
        if parentTag:
            self.parentInstance = parentTag.readProperty()
            
        self.albedoTex = None
        self.normalTex = None
        self.roughnessTex = None
        self.compositeTex = None
        self.compositeType = None
        self.metalnessTex = None
            
        paramVals = self.findPropertyTagByName("TextureParameterValues")
        if paramVals:
            listsOfParamProps = paramVals.readProperty()
            for propList in listsOfParamProps:
                nameProp = ue4FindPropertyTagLinear("ParameterName", propList)
                valueProp = ue4FindPropertyTagLinear("ParameterValue", propList)
                if nameProp and valueProp:
                    ue4SetTextureOverride(self, nameProp.readProperty(), valueProp.readProperty())
                    
    def loadDependencies(self, loadedDeps):
        if self.parentInstance:
            self.parentObject = ue4ImportDependency(self.parentInstance, loadedDeps)
            if self.parentObject:
                self.parentObject.loadDependencies(loadedDeps)
            else:
                print("Warning: Failed to load material instance parent:", self.parentInstance)
        self.albedoObject = ue4ImportDependency(self.albedoTex, loadedDeps)
        self.normalObject = ue4ImportDependency(self.normalTex, loadedDeps)
        self.roughnessObject = ue4ImportDependency(self.roughnessTex, loadedDeps)
        self.compositeObject = ue4ImportDependency(self.compositeTex, loadedDeps)
        self.metalnessObject = ue4ImportDependency(self.metalnessTex, loadedDeps)
        
    def getAlbedo(self):
        if self.albedoTex:
            return self.albedoTex
        if self.parentObject:
            return self.parentObject.getAlbedo()
        return ""
    def getNormal(self):
        if self.normalTex:
            return self.normalTex
        if self.parentObject:
            return self.parentObject.getNormal()
        return ""
    def getRoughness(self):
        if self.roughnessTex:
            return self.roughnessTex
        if self.parentObject:
            return self.parentObject.getRoughness()
        return ""
    def getComposite(self):
        if self.compositeTex:
            return self.compositeTex
        if self.parentObject:
            return self.parentObject.getComposite()
        return ""
    def getCompositeType(self):
        if self.compositeType:
            return self.compositeType
        if self.parentObject:
            return self.parentObject.getCompositeType()
        return ""
    def getMetalness(self):
        if self.metalnessTex:
            return self.metalnessTex
        if self.parentObject:
            return self.parentObject.getMetalness()
        return ""
                
class UE4Material(UE4Object):
    def __init__(self, asset):
        super().__init__(asset)
    def load(self, export):
        super().load(export)
        self.parentInstance = None
        self.albedoTex = None
        self.normalTex = None
        self.roughnessTex = None
        self.compositeTex = None
        self.compositeType = None
        self.metalnessTex = None
        #could potentially parse out all of the expression objects to try to dig through and find reasonable inputs to trace back through to get
        #better default texture assignments. currently not nearly enough shits are given.
        #baseColorProp = self.findPropertyTagByName("BaseColor")
        #normalProp = self.findPropertyTagByName("Normal")
        #roughnessProp = self.findPropertyTagByName("Roughness")
        #metalnessProp = self.findPropertyTagByName("Metallic")
        
    def loadDependencies(self, loadedDeps):
        self.albedoObject = ue4ImportDependency(self.albedoTex, loadedDeps)
        self.normalObject = ue4ImportDependency(self.normalTex, loadedDeps)
        self.roughnessObject = ue4ImportDependency(self.roughnessTex, loadedDeps)
        self.compositeObject = ue4ImportDependency(self.compositeTex, loadedDeps)
        self.metalnessObject = ue4ImportDependency(self.metalnessTex, loadedDeps)
        
    def getAlbedo(self):
        return self.albedoTex if self.albedoTex else ""
    def getNormal(self):
        return self.normalTex if self.normalTex else ""
    def getRoughness(self):
        return self.roughnessTex if self.roughnessTex else ""
    def getComposite(self):
        return self.compositeTex if self.compositeTex else ""
    def getCompositeType(self):
        return self.compositeType if self.compositeType else ""
    def getMetalness(self):
        return self.metalnessTex if self.metalnessTex else ""
        
class UE4MaterialExpressionTexture(UE4Object):
    def __init__(self, asset):
        super().__init__(asset)
    def load(self, export):
        super().load(export)
        self.paramName = self.findPropertyTagByName("ParameterName")
        self.materialName = self.findPropertyTagByName("Material")
        self.textureName = self.findPropertyTagByName("Texture")
    def postLoad(self):
        super().postLoad()
        if self.paramName and self.materialName and self.textureName:
            materialName = self.materialName.readProperty()
            foundMaterial = self.asset.getExportableObjectByName(materialName)
            if foundMaterial:
                ue4SetTextureOverride(foundMaterial, self.paramName.readProperty(), self.textureName.readProperty())


#=================================================================
# Data implementations
#=================================================================

class UE4StaticMaterial:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.materialInterfaceRef = bs.readInt()
        self.materialName = asset.getImportExportName(self.materialInterfaceRef)
        self.materialSlotName = UE4Name(asset)
        if asset.getRenderingObjectVersion() >= 10:
            self.uvChannelInfo = UE4MeshUVChannelInfo(asset)
            
class UE4SkeletalMaterial:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.materialInterfaceRef = bs.readInt()
        self.materialName = asset.getImportExportName(self.materialInterfaceRef)
        if asset.getEditorObjectVersion() >= 8:
            self.materialSlotName = UE4Name(asset)
        else:
            if asset.serialVersion >= 302:
                bs.readInt() #enableShadowCasting
            if asset.getRecomputeTangentVersion() > 0:
                self.recomputeTangent = bs.readInt() != 0
        if asset.getRenderingObjectVersion() >= 10:
            self.uvChannelInfo = UE4MeshUVChannelInfo(asset)
            
class UE4LegacyMaterial:
    def __init__(self, asset, materialName):
        ue4BaseObjectSetup(self, asset)
        self.materialName = materialName
    
class UE4MeshUVChannelInfo:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.initialized = bs.readInt() != 0
        self.overrideDensities = bs.readInt() != 0
        for channelIndex in range(0, 4):
            bs.readFloat() #uv densities
        
class UE4RefSkeleton:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        self.boneInfo = ue4ReadList(asset, UE4MeshBoneInfo)
        self.bindPose = ue4ReadList(asset, UE4Transform)
        if asset.serialVersion >= 310:
            #currently just assuming mats and info are 1:1
            self.nameToIndex = ue4ReadPairList(asset, UE4Name, UE4RawType.typeInt)
        if asset.serialVersion < 312 and len(self.boneInfo) > 0:
            #how revolting, maybe an actorx exporter remnant
            self.boneInfo[0].parentIndex = -1
        
class UE4MeshBoneInfo:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.name = UE4Name(asset)
        self.parentIndex = bs.readInt()
        if asset.serialVersion < 310:
            self.color = UE4Color(asset)

class UE4SkeletalMeshSection:
    def __init__(self, asset, objectOwner):
        ue4BaseObjectSetup(self, asset, objectOwner)
        bs = asset.bs
        
        stripFlags = UE4StripFlags(asset)
        self.materialIndex = bs.readShort()
        
        #the majority of this is unnecessary, but we have to parse to completion as these things are back-to-back in storage
        skelMeshVer = asset.getSkeletalMeshVersion()
        if skelMeshVer < 1:
            bs.readShort() #chunkIndex

        if stripFlags.isRenderDataStripped():
            self.firstIndex = 0
            self.triangleCount = 0
        else:
            self.firstIndex = bs.readInt()
            self.triangleCount = bs.readInt()
        
        self.triangleSorting = bs.readByte()
        if asset.serialVersion >= 254:
            self.disabled = bs.readInt() != 0
            self.clothIndex = bs.readShort()
            if asset.serialVersion >= 280:
                bs.readByte() #enableClothLOD
        else:
            self.disabled = False
            
        if asset.getRecomputeTangentVersion() > 0:
            self.recomputeTangent = bs.readInt() != 0
        if asset.getEditorObjectVersion() >= 8 and asset.gameHack != UE4_GAMEHACK_T7:
            self.castShadow = bs.readInt() != 0
            
        if skelMeshVer >= 1:
            if not stripFlags.isRenderDataStripped():
                self.baseVertexIndex = bs.readInt()
            if not stripFlags.isEditorDataStripped():
                if skelMeshVer < 2:
                    ue4ReadList(asset, UE4RigidVertex)
                ue4ReadList(asset, UE4SoftVertex)
            
            self.boneMap = ue4ReadList(asset, UE4RawType.typeShort)
            if skelMeshVer >= 4:
                self.vertCount = bs.readInt()
            if skelMeshVer < 2:
                bs.readInt() #numRigidVerts
                bs.readInt() #numSoftVerts
            self.maxBoneInfluences = bs.readInt()
            
            #cloth stuff, don't care
            clothSize = len(ue4ReadList(asset, UE4ApexClothPhysToRenderVertData))
            if clothSize > 0:
                objectOwner.hasCloth = True
            ue4ReadList(asset, UE4Vector)
            ue4ReadList(asset, UE4Vector)
            if skelMeshVer < 8:
                bs.readInt()
            else:
                UE4ClothingSectionData(asset)
            
class UE4StaticMeshSection:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.materialIndex = bs.readInt()
        self.firstIndex = bs.readInt()
        self.triangleCount = bs.readInt()
        self.minVertIndex = bs.readInt()
        self.maxVertIndex = bs.readInt()
        self.enableCollision = bs.readInt() != 0
        self.castShadow = bs.readInt() != 0
            
class UE4VertexPositions:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.stride = bs.readInt()
        self.count = bs.readInt()
        arrayStride, arrayCount, arrayData = ue4ReadBulkArray(asset)
        self.data = arrayData
        
class UE4VertexColors:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.stride = bs.readInt()
        self.count = bs.readInt()
        stripFlags = UE4StripFlags(asset)
        if not stripFlags.isRenderDataStripped() and self.count > 0:
            arrayStride, arrayCount, arrayData = ue4ReadBulkArray(asset)
            self.data = arrayData #rgba32
        else:
            self.data = None

class UE4VertexColorsLegacy:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        strippedColor = False
        if asset.serialVersion >= 269:
            stripFlags = UE4StripFlags(asset)
            strippedColor = stripFlags.isRenderDataStripped()
        if not strippedColor:
            arrayStride, arrayCount, arrayData = ue4ReadBulkArray(asset)
            self.data = arrayData #rgba32
            self.stride = arrayStride
            self.count = arrayCount
        else:
            self.data = None
            
class UE4VertexInterleaved:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        UE4StripFlags(asset)
        self.uvSetCount = bs.readInt()
        self.stride = bs.readInt()
        self.vertCount = bs.readInt()
        self.fullPrecisionUV = bs.readInt() != 0
        self.fullPrecisionTangent = False
        if asset.serialVersion >= 504:
            self.fullPrecisionTangent = bs.readInt() != 0
        interleavedStride, interleavedCount, interleavedData = ue4ReadBulkArray(asset)
        self.interleavedData = interleavedData
        self.normTanOffset = 0
        self.uvsOffset = 16 if self.fullPrecisionTangent else 8
        self.uvSetSize = 8 if self.fullPrecisionUV else 4
            
class UE4SkeletalMeshVertexBuffer:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        UE4StripFlags(asset)
        self.uvSetCount = bs.readInt()
        self.fullPrecisionUV = bs.readInt() != 0
        self.extraBoneWeights = False
        skelMeshVer = asset.getSkeletalMeshVersion()
        if asset.serialVersion >= 334 and skelMeshVer < 7:
            self.extraBoneWeights = bs.readInt() != 0
        self.meshExtent = UE4Vector(asset)
        self.meshOrigin = UE4Vector(asset)
        
        skelMeshVer = asset.getSkeletalMeshVersion()
        #position should really come first here, and for that matter be packed next to the weights. but, you know, ue4.
        self.normTanOffset = 0
        self.weightsOffset = -1
        self.weightsPerVert = 8 if self.extraBoneWeights else 4
        postNormalsOffset = self.normTanOffset + 8
        if skelMeshVer < 7:
            self.weightsOffset = postNormalsOffset
            postNormalsOffset += 2 * self.weightsPerVert
        self.posOffset = postNormalsOffset
        self.uvsOffset = self.posOffset + 12
        self.uvSetSize = 8 if self.fullPrecisionUV else 4
        self.stride = self.uvsOffset + self.uvSetCount * self.uvSetSize
        #we don't serialize each vert
        arrayStride, arrayCount, arrayData = ue4ReadBulkArray(asset)
        self.data = arrayData
            
class UE4RawIndices:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.indexSize = 4 if bs.readInt() != 0 else 2
        arrayStride, arrayCount, arrayData = ue4ReadBulkArray(asset)
        self.indexCount = (arrayStride * arrayCount) // self.indexSize
        self.data = arrayData

class UE4MultiSizeIndices:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        if asset.serialVersion < 283:
            bs.readInt() #needsCPUAccess
        self.indexSize = bs.readByte()
        if self.indexSize <= 0:
            self.indexSize = 4
        arrayStride, arrayCount, arrayData = ue4ReadBulkArray(asset)
        self.indexCount = (arrayStride * arrayCount) // self.indexSize
        self.data = arrayData
        
class UE4SkeletalModelLOD:
    def __init__(self, asset, objectOwner):
        ue4BaseObjectSetup(self, asset, objectOwner)
        bs = asset.bs
        stripFlags = UE4StripFlags(asset)
        if not stripFlags.isEditorDataStripped():
            noesis.doException("Unstripped SkeletalModelLOD editor data is not supported.")
        
        self.hasCloth = False
        self.chunks = []
        self.sections = ue4ReadList(asset, UE4SkeletalMeshSection, self)
        self.indices = UE4MultiSizeIndices(asset)
        self.activeBoneIndices = ue4ReadList(asset, UE4RawType.typeShort)
        skelMeshVer = asset.getSkeletalMeshVersion()
        if skelMeshVer < 1:
            self.chunks = ue4ReadList(asset, UE4SkelMeshChunk, self)
        self.size = bs.readInt()
        if stripFlags.isRenderDataStripped():
            self.vertCount = 0
        else:
            self.vertCount = bs.readInt()
        self.requiredBones = ue4ReadList(asset, UE4RawType.typeShort)
        if asset.serialVersion >= 152:
            #self.meshToImportVertexMap = ue4ReadList(asset, UE4RawType.typeInt)
            ue4ReadListAsRawData(asset, 4) #don't need this, so don't waste time serializing each element
            self.maxImportVertex = bs.readInt()
            
        if stripFlags.isRenderDataStripped():
            self.uvSetCount = 0
            self.vertSkinnable = None
        else:
            self.uvSetCount = bs.readInt()
            self.vertSkinnable = UE4SkeletalMeshVertexBuffer(asset)
            self.weightData = None
            if skelMeshVer >= 7: #bsn - may not be accurate, not present in some v510
                #weight data may be stored in a separate array, not interleaved with the vertSkinnable data
                weightStripFlags = UE4StripFlags(asset)
                self.extraBoneWeights = bs.readInt() != 0
                if not weightStripFlags.isRenderDataStripped():
                    self.weightsPerVert = 8 if self.extraBoneWeights else 4
                    self.weightData = bs.readBytes(4 * self.weightsPerVert)
                    
            vertexColorProp = objectOwner.findPropertyTagByName("bHasVertexColors")
            if vertexColorProp and noeSafeGet(vertexColorProp, "boolValue") is True:
                if skelMeshVer < 7: #bsn - may not be accurate, legacy present in some v510
                    self.vertColors = UE4VertexColorsLegacy(asset)
                else:
                    self.vertColors = UE4VertexColors(asset)
            if (stripFlags.classStripFlags & 1) == 0:
                UE4MultiSizeIndices(asset) #adjacency index buffer
            if self.hasCloth:
                clothStripFlags = UE4StripFlags(asset)
                if not stripFlags.isRenderDataStripped():
                    ue4ReadBulkArray(asset)
        
class UE4StaticModelLOD:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        stripFlags = UE4StripFlags(asset)
        self.chunks = []
        self.sections = ue4ReadList(asset, UE4StaticMeshSection)
        self.maxDeviation = bs.readFloat()
        self.vertSkinnable = None
        self.vertPositions = None
        if not stripFlags.isRenderDataStripped():
            self.vertPositions = UE4VertexPositions(asset)
            self.vertInterleaved = UE4VertexInterleaved(asset)
            self.vertColors = UE4VertexColors(asset)
            
            self.indices = UE4RawIndices(asset)
            #so many turds
            if asset.serialVersion >= 489:
                UE4RawIndices(asset) #reversed indices
            UE4RawIndices(asset) #depth-only indices
            if asset.serialVersion >= 489:
                UE4RawIndices(asset) #reversed depth-only indices
                
            if asset.serialVersion >= 368 and asset.serialVersion < 394:
                UE4DistanceFieldVolumeData(self.asset)        
                
            if not stripFlags.isEditorDataStripped():
                UE4RawIndices(asset) #wireframe index buffer
            if (stripFlags.classStripFlags & 1) == 0:
                UE4RawIndices(asset) #adjacency index buffer
        
class UE4Texture2DMip:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        isCooked = bs.readInt() != 0
        self.bulkData = UE4ByteBulkData(asset)
        self.width = bs.readInt()
        self.height = bs.readInt()
        if not isCooked:
            UE4String(asset)
            
class UE4PropertyTag:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.name = repr(UE4Name(asset))
        if self.name.lower() != "none":
            self.propType = repr(UE4Name(asset))
            self.dataSize = bs.readInt()
            self.arrayIndex = bs.readInt()
            if self.propType == "StructProperty":
                self.structName = repr(UE4Name(asset))
                if asset.serialVersion >= 441:
                    self.structGuid = UE4Guid(asset)
            elif self.propType == "BoolProperty":
                self.boolValue = bs.readUByte() > 0
            elif self.propType == "ByteProperty":
                self.enumName = repr(UE4Name(asset))
            elif self.propType == "ArrayProperty":
                self.innerTypeName = repr(UE4Name(asset))
                
            if asset.serialVersion >= 509:
                if self.propType == "SetProperty":
                    self.innerTypeName = repr(UE4Name(asset))
                elif self.propType == "MapProperty_UE4":
                    self.innerTypeName = repr(UE4Name(asset))
                    self.valueTypeName = repr(UE4Name(asset))
                    
            if asset.serialVersion >= 503:
                if bs.readUByte() > 0:
                    UE4Guid(asset)
            self.dataOffset = bs.tell() #can be parsed later on demand, if needed
            bs.seek(self.dataSize, NOESEEK_REL)
    def readProperty(self):
        asset = self.asset
        bs = asset.bs
        prevOffset = bs.tell()
        bs.seek(self.dataOffset, NOESEEK_ABS)
        
        #limited support, only implementing what i need as i need it
        r = None
        if self.propType == "NameProperty":
            r = repr(UE4Name(asset))
        elif self.propType == "StructProperty":
            #return self.structName + " " + repr(self.dataSize) + " " + repr(bs.tell())
            entryTag = UE4PropertyTag(asset)
            r = []
            while entryTag.name.lower() != "none":
                r.append(entryTag)
                entryTag = UE4PropertyTag(asset)
        elif self.propType == "ObjectProperty":
            objectRef = bs.readInt()
            return asset.getImportExportName(objectRef)
        elif self.propType == "ArrayProperty":
            r = []
            dataCount = bs.readInt()
            if self.innerTypeName == "StructProperty":
                if asset.serialVersion >= 500:
                    innerTag = UE4PropertyTag(asset)
                    bs.seek(innerTag.dataOffset, NOESEEK_ABS)
            
                for dataIndex in range(0, dataCount):
                    entryTag = UE4PropertyTag(asset)
                    tagList = []
                    while entryTag.name.lower() != "none":
                        tagList.append(entryTag)
                        entryTag = UE4PropertyTag(asset)
                    r.append(tagList)
            elif self.innerTypeName == "ObjectProperty":
                for dataIndex in range(0, dataCount):
                    objectRef = bs.readInt()
                    objectName = asset.getImportExportName(objectRef)
                    r.append(objectName)
            
        bs.seek(prevOffset, NOESEEK_ABS)
        return r
            
class UE4ByteBulkData:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.dataFlags = bs.readInt()
        self.elementCount = bs.readInt()
        self.dataSize = bs.readInt()
        self.dataOffset = bs.readInt64()
        self.endOfHeader = bs.tell()
        if self.dataFlags & 64:
            bs.seek(self.dataSize, NOESEEK_REL)
    def readData(self):
        if self.dataFlags & 256:
            return None #in a separate file, not currently supported
        bs = self.asset.bs
        prevOffset = bs.tell()
        
        #print("bulk read:", self.dataFlags, self.dataSize, self.endOfHeader, self.dataOffset, self.asset.bulkDataOffset)
        data = None
        if self.dataFlags & 1: #elsewhere in file
            bs.seek(self.asset.bulkDataOffset + self.dataOffset, NOESEEK_ABS)
        else: #assume inline, not really correct
            bs.seek(self.endOfHeader, NOESEEK_ABS)
        data = bs.readBytes(self.dataSize)
        bs.seek(prevOffset, NOESEEK_ABS)
        return data
        
class UE4DistanceFieldVolumeData:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.data = ue4ReadListAsRawData(asset, 2)
        self.size = UE4IntVector(asset)
        self.box = UE4Box(asset)
        self.meshWasClosed = bs.readInt() != 0
        if asset.serialVersion >= 394:
            bs.readInt() #builtAsIfTwoSided
            if asset.serialVersion >= 397:
                bs.readInt() #meshWasPlane

class UE4ApexClothPhysToRenderVertData:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.positionBaryCoordsAndDist = UE4Vector4(asset)
        self.normalBaryCoordsAndDist = UE4Vector4(asset)
        self.tangentBaryCoordsAndDist = UE4Vector4(asset)
        self.simMeshVertInidices = (bs.readShort(), bs.readShort(), bs.readShort(), bs.readShort())
        bs.readInt() #pad
        bs.readInt() #pad
        
class UE4ClothingSectionData:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.guid = UE4Guid(asset)
        self.assetLodIndex = bs.readInt()

class UE4SkelMeshChunk:
    def __init__(self, asset, objectOwner):
        ue4BaseObjectSetup(self, asset, objectOwner)
        bs = asset.bs
        stripFlags = UE4StripFlags(asset)
        if stripFlags.isRenderDataStripped():
            noesis.doException("Stripped SkelMeshChunk data is not supported.")

        self.baseVertexIndex = bs.readInt()
        if not stripFlags.isEditorDataStripped():
            ue4ReadList(asset, UE4RigidVertex)
            ue4ReadList(asset, UE4SoftVertex)
        self.boneMap = ue4ReadList(asset, UE4RawType.typeShort)
        bs.readInt() #numRigidVerts
        bs.readInt() #numSoftVerts
        self.maxBoneInfluences = bs.readInt()

        if asset.serialVersion >= 254:
            clothSize = len(ue4ReadList(asset, UE4ApexClothPhysToRenderVertData))
            if clothSize > 0:
                objectOwner.hasCloth = True
            ue4ReadList(asset, UE4Vector)
            ue4ReadList(asset, UE4Vector)
            bs.readShort()
            bs.readShort()
        
class UE4RigidVertex:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.pos = UE4Vector(asset)
        self.normals = (UE4PackedNormal(asset), UE4PackedNormal(asset), UE4PackedNormal(asset))
        self.uvs = []
        for uvSetIndex in range(0, 4):
            self.uvs.append(UE4UVFloat(asset))
        self.boneIndex = bs.readUByte()
        self.color = UE4Color(asset)

class UE4SoftVertex:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.pos = UE4Vector(asset)
        self.normals = (UE4PackedNormal(asset), UE4PackedNormal(asset), UE4PackedNormal(asset))
        self.uvs = []
        for uvSetIndex in range(0, 4):
            self.uvs.append(UE4UVFloat(asset))
        self.color = UE4Color(asset)
        self.boneIndices = []
        self.boneWeights = []
        weightsPerVert = 8 if asset.serialVersion >= 332 else 4
        for weightIndex in range(0, weightsPerVert):
            self.boneIndices.append(bs.readUByte())
        for weightIndex in range(0, weightsPerVert):
            self.boneWeights.append(bs.readUByte())
        
class UE4Box:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.mins = UE4Vector(asset)
        self.maxs = UE4Vector(asset)
        self.isValid = bs.readByte() != 0
        
class UE4BoxSphereBounds:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.origin = UE4Vector(asset)
        self.extent = UE4Vector(asset)
        self.radius = bs.readFloat()
        
class UE4Vector:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.v = (bs.readFloat(), bs.readFloat(), bs.readFloat())
    def __repr__(self):
        return repr(self.v)
        
class UE4Vector4:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.v = (bs.readFloat(), bs.readFloat(), bs.readFloat(), bs.readFloat())
    def __repr__(self):
        return repr(self.v)
        
class UE4IntVector:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.v = (bs.readInt(), bs.readInt(), bs.readInt())
    def __repr__(self):
        return repr(self.v)

class UE4Quat:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.q = (bs.readFloat(), bs.readFloat(), bs.readFloat(), bs.readFloat())
    def __repr__(self):
        return repr(self.q)
        
class UE4Transform:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        self.rotation = UE4Quat(asset)
        self.translation = UE4Vector(asset)
        self.scale = UE4Vector(asset)
    def __repr__(self):
        return "(" + repr(self.rotation) + ", " + repr(self.translation) + ", " + repr(self.scale) + ")"
    def toNoeMat43(self):
        t = NoeVec3(self.translation.v)
        r = NoeQuat(self.rotation.q)
        s = NoeVec3(self.scale.v)
        noeMat = r.toMat43(1)
        noeMat[0] *= s[0] #note - untested, scaling transform might need to be transposed
        noeMat[1] *= s[1]
        noeMat[2] *= s[2]
        noeMat[3] = t
        return noeMat
    
class UE4UVFloat:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.uv = (bs.readFloat(), bs.readFloat())
    
class UE4PackedNormal:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.data = bs.readUInt()
    
class UE4Color:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        bs.r = bs.readUByte()
        bs.g = bs.readUByte()
        bs.b = bs.readUByte()
        bs.a = bs.readUByte()
        
class UE4StripFlags:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.globalStripFlags = bs.readUByte()
        self.classStripFlags = bs.readUByte()
    def isEditorDataStripped(self):
        return (self.globalStripFlags & 1) != 0
    def isRenderDataStripped(self):
        return (self.globalStripFlags & 2) != 0
        
class UE4VersionType:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.key = UE4Guid(asset)
        self.version = bs.readInt()

class UE4EngineVersion:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.verMajor = bs.readUShort()
        self.verMinor = bs.readUShort()
        self.verPatch = bs.readUShort()
        self.clNumber = bs.readUInt()
        self.branch = ue4ReadString(asset)
                
class UE4ObjectRef:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.refIndex = bs.readInt()
        
class UE4Guid:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        if asset:
            bs = asset.bs
            self.A = bs.readUInt()
            self.B = bs.readUInt()
            self.C = bs.readUInt()
            self.D = bs.readUInt()
    @classmethod
    def fromValue(classObject, a, b, c, d):
        inst = classObject(None)
        inst.A = a
        inst.B = b
        inst.C = c
        inst.D = d
        return inst
    def __eq__(self, other):
        return self.A == other.A and self.B == other.B and self.C == other.C and self.D == other.D
    def __ne__(self, other):
        return self.A != other.A or self.B != other.B or self.C != other.C or self.D != other.D
        
class UE4GenerationInfo:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.exportCount = bs.readInt()
        self.nameCount = bs.readInt()
        
class UE4CompressedChunk:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.decompOffset = bs.readInt()
        self.decompSize = bs.readInt()
        self.compOffset = bs.readInt()
        self.compSize = bs.readInt()
        
class UE4String:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        self.data = ue4ReadString(asset)
    def __repr__(self):
        return self.data
        
class UE4Name:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.index = bs.readInt()
        self.extraIndex = bs.readInt()
        self.data = asset.getName(self.index)
        if self.data is None:
            self.data = "None"
    def __repr__(self):
        return self.data
        
class UE4ImportObject:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.classPackage = UE4Name(asset)
        self.className = UE4Name(asset)
        self.packageIndex = bs.readInt()
        self.objectName = UE4Name(asset)
        
class UE4ExportObject:
    def __init__(self, asset):
        ue4BaseObjectSetup(self, asset)
        bs = asset.bs
        self.classIndex = bs.readInt()
        self.superIndex = bs.readInt()
        if asset.serialVersion >= 508:
            self.templateIndex = bs.readInt()
        self.packageIndex = bs.readInt()
        self.objectName = UE4Name(asset)
        self.objectFlags = bs.readInt()

        if asset.serialVersion >= 511:
            self.serialSize = bs.readInt64()
            self.serialOffset = bs.readInt64()
        else:
            self.serialSize = bs.readInt()
            self.serialOffset = bs.readInt()
            
        bs.readInt() #forced export
        bs.readInt() #not for client
        bs.readInt() #not for server
        
        self.guid = UE4Guid(asset)
        self.packageFlags = bs.readInt()
        
        bs.readInt() #not for editor
        self.isAsset = bs.readInt() != 0
        if asset.serialVersion >= 507:
            #preload dependencies
            bs.readInt()
            bs.readInt()
            bs.readInt()
            bs.readInt()
            bs.readInt()

class UE4RawType:
    def __init__(self, asset, data):
        ue4BaseObjectSetup(self, asset)
        self.data = data
    def __repr__(self):
        return repr(self.data)
    @classmethod
    def typeInt(classObject, asset):
        bs = asset.bs
        data = bs.readInt()
        return classObject(asset, data)
    @classmethod
    def typeShort(classObject, asset):
        bs = asset.bs
        data = bs.readShort()
        return classObject(asset, data)
        
class UE4ImportableObject:
    def __init__(self, export, fullPath):
        self.export = export
        self.filePath = fullPath
        

#=================================================================
# Utility implementations
#=================================================================

ue4LoaderDict = {
    "Texture2D" : UE4Texture2D,
    "StaticMesh" : UE4StaticMesh,
    "SkeletalMesh" : UE4SkeletalMesh,
    "Material" : UE4Material,
    "MaterialInstance" : UE4MaterialInstance,
    "MaterialInstanceConstant" : UE4MaterialInstance,
    "MaterialExpressionTextureSample" : UE4MaterialExpressionTexture,
    "MaterialExpressionTextureSampleParameter2D" : UE4MaterialExpressionTexture
}

def ue4ReadList(asset, listType, objectOwner = None):
    bs = asset.bs
    count = bs.readUInt()
    list = []
    for index in range(0, count):
        if objectOwner is None:
            list.append(listType(asset))
        else:
            list.append(listType(asset, objectOwner))
    return list

def ue4ReadListAsRawData(asset, elemSize):
    bs = asset.bs
    count = bs.readUInt()
    return bs.readBytes(elemSize * count)
    
def ue4ReadPairList(asset, firstType, secondType):
    bs = asset.bs
    count = bs.readUInt()
    list = []
    for index in range(0, count):
        list.append((firstType(asset), secondType(asset)))
    return list
    
def ue4ReadBulkArray(asset):
    bs = asset.bs
    stride = bs.readInt()
    count = bs.readInt()
    data = bs.readBytes(stride * count)
    return stride, count, data
    
def ue4ReadString(asset):
    bs = asset.bs
    stringLength = bs.readInt()
    if stringLength >= 0:
        return noeStrFromBytes(bs.readBytes(stringLength), "UTF-8")
    else:
        return noeStrFromBytes(bs.readBytes(-stringLength * 2), "UTF-16")    
        
def ue4BaseObjectSetup(object, asset, objectOwner = None):
    object.asset = asset
    object.objectOwner = None
        
def ue4FindPropertyTagLinear(name, propList):
    for prop in propList:
        if prop.name == name:
            return prop
    return None

def ue4SetTextureOverride(material, paramName, textureName):
    namePropVal = paramName.lower()
    #here's some hacked up bullshit, for now
    if namePropVal.startswith("base") or namePropVal.startswith("bace") or namePropVal.startswith("diffuse") or namePropVal.startswith("albedo"):
        material.albedoTex = textureName
    elif namePropVal.startswith("normal") or namePropVal.startswith("nomal"):
        material.normalTex = textureName
    elif namePropVal.startswith("rough"):
        material.roughnessTex = textureName
    elif namePropVal.startswith("metal"):
        material.metalnessTex = textureName
    elif namePropVal.startswith("srma"):
        material.compositeTex = textureName
        material.compositeType = "srma"
    elif material.asset.gameHack == UE4_GAMEHACK_T7 and (namePropVal.startswith("specluar") or namePropVal.startswith("specular")):
        material.compositeTex = textureName
        material.compositeType = "rnasmul"
    elif material.asset.gameHack == UE4_GAMEHACK_T7 and namePropVal.startswith("color"):
        material.albedoTex = textureName
    #else:
    #    print("Discard texture property:", namePropVal, textureName)

def ue4UntileTexture(width, height, textureData, bitsPerTexel, bcFlag):
    if noesis.optWasInvoked("-ue4tex1dthin"):
        textureData = rapi.callExtensionMethod("untile_1dthin", textureData, width, height, bitsPerTexel, bcFlag)
    return textureData

def ue4ConvertTextureData(width, height, textureData, pixelFormat):
    noeFormat = noesis.NOESISTEX_RGBA32
    if pixelFormat == "PF_BC5":
        textureData = ue4UntileTexture(width, height, textureData, 8, 1)
        textureData = rapi.imageDecodeDXT(textureData, width, height, noesis.FOURCC_ATI2)
        noeFormat = noesis.NOESISTEX_RGBA32
    elif pixelFormat == "PF_BC4":
        textureData = ue4UntileTexture(width, height, textureData, 4, 1)
        textureData = rapi.imageDecodeDXT(textureData, width, height, noesis.FOURCC_ATI1)
        noeFormat = noesis.NOESISTEX_RGBA32
    elif pixelFormat == "PF_B8G8R8A8":
        textureData = ue4UntileTexture(width, height, textureData, 32, 0)
        noeFormat = noesis.NOESISTEX_RGBA32
    elif pixelFormat == "PF_DXT1":
        textureData = ue4UntileTexture(width, height, textureData, 4, 1)
        noeFormat = noesis.NOESISTEX_DXT1
    elif pixelFormat == "PF_DXT3":
        textureData = ue4UntileTexture(width, height, textureData, 8, 1)
        noeFormat = noesis.NOESISTEX_DXT3
    elif pixelFormat == "PF_DXT5":
        textureData = ue4UntileTexture(width, height, textureData, 8, 1)
        noeFormat = noesis.NOESISTEX_DXT5
    #could easily support PVRTC and ASTC as decoders are already exposed to python, but don't have any test data at the moment.
    #ue4 doesn't look to even support PVRTC2, although noesis supports that too. (PF_PVRTC2 == PVRTC 2bpp, not PVRTC2)
    else:
        print("Unhandled pixel format:", pixelFormat)
        textureData = None
    return textureData, noeFormat

ue4LastScanPath = None
ue4AssetDatabase = {}

def ue4ImportDependency(objectName, loadedDeps):
    global ue4AssetDatabase
    if objectName is None:
        return None
    if objectName in ue4AssetDatabase: #alright, someone has it
        importableObject = ue4AssetDatabase[objectName]
        #see if it's already been loaded
        depAsset = None
        if importableObject.filePath in loadedDeps:
            depAsset = loadedDeps[importableObject.filePath]
        else:
        #attempt to load it
            print("Loading dependency:", importableObject.filePath)
            with open(importableObject.filePath, "rb") as f:
                data = f.read()
                bs = NoeBitStream(data)
                testAsset = UE4Asset(bs)
                if testAsset.parse() == 0:
                    depAsset = testAsset
                    loadedDeps[importableObject.filePath] = depAsset
                    depAsset.loadTables()
                    depAsset.loadAssetData()
        if depAsset:
            importedObject = depAsset.getExportableObjectByName(objectName)
            if not importedObject:
                print("Warning: Object", objectName, "not found in expected package.")
            return importedObject
    return None

def ue4ScanAssetData(scanDataPath):
    global ue4LastScanPath
    global ue4AssetDatabase
    
    ue4LastScanPath = scanDataPath
    ue4AssetDatabase = {}
    if not ue4LastScanPath:
        return
    for root, dirs, files in os.walk(scanDataPath):
        for fileName in files:
            lowerName = fileName.lower()
            if lowerName.endswith(".uasset"):
                fullPath = os.path.join(root, fileName)
                print("Attempting to scan:", fullPath)
                with open(fullPath, "rb") as f:
                    bs = NoeFileStream(f)
                    asset = UE4Asset(bs)
                    if asset.parse() == 0:
                        asset.loadTables()
                        for export in asset.exports:
                            className = asset.getImportExportName(export.classIndex)
                            ue4AssetDatabase[repr(export.objectName)] = UE4ImportableObject(export, fullPath)
        
        
#=================================================================
# Noesis implementations
#=================================================================
        
def ue4CheckType(data):
    asset = UE4Asset(NoeBitStream(data))
    if asset.parse() != 0:
        return 0
    return 1
    
def ue4LoadModel(data, mdlList):
    asset = UE4Asset(NoeBitStream(data))
    if asset.parse() != 0:
        return 0
        
    print("UE4 version info:", asset.version, asset.serialVersion, asset.verA, asset.verB, asset.verLic)

    asset.loadTables()
    
    scanDataPath = None
    if noesis.optWasInvoked("-ue4datapath"):
        scanDataPath = noesis.optGetArg("-ue4datapath")
    global ue4LastScanPath
    if scanDataPath != ue4LastScanPath:
        ue4ScanAssetData(scanDataPath)
    
    asset.loadAssetData()

    noeTextures = []
    noeMaterials = []
    
    loadedDeps = {}
    #let's check the database for material dependencies
    for mesh in asset.meshes:
        for lod in mesh.lods:
            for section in lod.sections:
                if section.materialIndex >= 0 and section.materialIndex < len(mesh.materials) and not noesis.optWasInvoked("-ue4defaultmtl"):
                    materialName = mesh.materials[section.materialIndex].materialName
                    foundMaterial = False
                    for noeMat in noeMaterials:
                        if noeMat.name == materialName:
                            foundMaterial = True
                            break
                    if not foundMaterial:
                        noeMat = NoeMaterial(materialName, "")
                        noeMat.setMetal(0.0, 0.0)
                    
                        materialObject = ue4ImportDependency(materialName, loadedDeps)
                        albedoTex = ""
                        normalTex = ""
                        roughnessTex = ""
                        compositeTex = ""
                        compositeType = ""
                        if materialObject:
                            materialObject.loadDependencies(loadedDeps)
                            albedoTex = materialObject.getAlbedo()
                            normalTex = materialObject.getNormal()
                            roughnessTex = materialObject.getRoughness()
                            compositeTex = materialObject.getComposite()
                            compositeType = materialObject.getCompositeType()
                        if compositeTex == "" and roughnessTex == "":
                            roughnessTex = noesis.getScenesPath() + "sample_pbr_o.png"
                            noeMat.setMetal(0.0, 0.0)
                            noeMat.setRoughness(0.0, 0.75)
                        if albedoTex == "":
                            albedoTex = noesis.getScenesPath() + "sample_pbr_o.png"
                            noeMat.setMetal(0.0, 1.0)
                            noeMat.setRoughness(0.0, 0.25)
                        hadNormalTex = (normalTex != "")
                        if normalTex == "":
                            normalTex = noesis.getScenesPath() + "sample_pbr_n.png"

                        noeMat.setTexture(albedoTex)
                        noeMat.setNormalTexture(normalTex)
                        if compositeTex != "":
                            noeMat.setSpecularTexture(compositeTex)
                            if compositeType == "srma":
                                noeMat.flags |= noesis.NMATFLAG_PBR_METAL | noesis.NMATFLAG_PBR_SPEC_IR_RG
                                noeMat.setMetal(1.0, 0.0)
                                noeMat.setSpecularSwizzle( NoeMat44([[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]]) )
                            if compositeType == "rnasmul":
                                #flag it as metal and just eliminate metal contribution. spec map is often shared with albedo and
                                #doesn't look good as a scalar.
                                noeMat.flags |= noesis.NMATFLAG_PBR_METAL | noesis.NMATFLAG_PBR_ROUGHNESS_NRMALPHA
                                noeMat.setMetal(0.0, 0.0)
                            else:
                                noeMat.flags |= noesis.NMATFLAG_PBR_METAL | noesis.NMATFLAG_PBR_SPEC_IR_RG
                                print("Warning: Unhandled composite type", compositeType)
                        else:
                            if hadNormalTex and asset.gameHack == UE4_GAMEHACK_T7:
                                noeMat.flags |= noesis.NMATFLAG_PBR_METAL | noesis.NMATFLAG_PBR_ROUGHNESS_NRMALPHA
                                noeMat.setMetal(0.0, 0.0)
                                noeMat.setRoughness(1.0, 0.0)
                                
                            noeMat.setSpecularTexture(roughnessTex)
                            noeMat.flags |= noesis.NMATFLAG_PBR_METAL | noesis.NMATFLAG_PBR_SPEC_IR_RG
                        noeMat.setEnvTexture(noesis.getScenesPath() + "sample_pbr_e4.dds")
                        noeMat.uMaterial = materialObject
                        noeMaterials.append(noeMat)

    #transfer all loaded textures into the noesis list
    asset.transferTextures(noeTextures)
    for depAsset in loadedDeps.values():
        depAsset.transferTextures(noeTextures)

    mdlMats = NoeModelMaterials(noeTextures, noeMaterials) if len(noeTextures) > 0 or len(noeMaterials) > 0 else None
    
    for meshIndex in range(0, len(asset.meshes)):
        ctx = rapi.rpgCreateContext()
        rapi.rpgSetOption(noesis.RPGOPT_TRIWINDBACKWARD, 1)
        #possible todo - if asset is big-endian, set rpg mode, since we keep all rendering data in the native endian.
        #however, don't have any UE4 big-endian data to test with.

        mesh = asset.meshes[meshIndex]
        if len(mesh.lods) == 0:
            continue
        lod = mesh.lods[0] #for now, just always pick the first lod.
        
        if mesh.exportEntry:
            rapi.rpgSetName(repr(mesh.exportEntry.objectName))

        if lod.vertSkinnable: #skeletal mesh path
            ilv = lod.vertSkinnable
            rapi.rpgBindPositionBufferOfs(ilv.data, noesis.RPGEODATA_FLOAT, ilv.stride, ilv.posOffset)
            rapi.rpgBindTangentBufferOfs(ilv.data, noesis.RPGEODATA_UBYTE, ilv.stride, ilv.normTanOffset)
            rapi.rpgBindNormalBufferOfs(ilv.data, noesis.RPGEODATA_UBYTE, ilv.stride, ilv.normTanOffset + 4)
            if ilv.uvSetCount > 0:
                uvFormat = noesis.RPGEODATA_FLOAT if ilv.fullPrecisionUV else noesis.RPGEODATA_HALFFLOAT
                rapi.rpgBindUV1BufferOfs(ilv.data, uvFormat, ilv.stride, ilv.uvsOffset)
                if ilv.uvSetCount > 1:
                    rapi.rpgBindUV2BufferOfs(ilv.data, uvFormat, ilv.stride, ilv.uvsOffset + ilv.uvSetSize)
            if ilv.weightsOffset >= 0:
                rapi.rpgBindBoneIndexBufferOfs(ilv.data, noesis.RPGEODATA_UBYTE, ilv.stride, ilv.weightsOffset, ilv.weightsPerVert)
                rapi.rpgBindBoneWeightBufferOfs(ilv.data, noesis.RPGEODATA_UBYTE, ilv.stride, ilv.weightsOffset + ilv.weightsPerVert, ilv.weightsPerVert)
            elif lod.weightData: #stored in a separate array
                rapi.rpgBindBoneIndexBufferOfs(lod.weightData, noesis.RPGEODATA_UBYTE, lod.weightsPerVert * 2, 0, lod.weightsPerVert)
                rapi.rpgBindBoneWeightBufferOfs(lod.weightData, noesis.RPGEODATA_UBYTE, lod.weightsPerVert * 2, lod.weightsPerVert, lod.weightsPerVert)
        else: #static mesh path
            pos = noeSafeGet(lod, "vertPositions")
            if pos is None:
                continue
            rapi.rpgBindPositionBufferOfs(pos.data, noesis.RPGEODATA_FLOAT, pos.stride, 0)
            ilv = lod.vertInterleaved
            if ilv.vertCount == pos.count:
                normTanFormat = noesis.RPGEODATA_USHORT if ilv.fullPrecisionTangent else noesis.RPGEODATA_UBYTE
                normalOffset = 8 if ilv.fullPrecisionTangent else 4
                rapi.rpgBindTangentBufferOfs(ilv.interleavedData, normTanFormat, ilv.stride, ilv.normTanOffset)
                rapi.rpgBindNormalBufferOfs(ilv.interleavedData, normTanFormat, ilv.stride, ilv.normTanOffset + normalOffset)
                if ilv.uvSetCount > 0:
                    uvFormat = noesis.RPGEODATA_FLOAT if ilv.fullPrecisionUV else noesis.RPGEODATA_HALFFLOAT
                    rapi.rpgBindUV1BufferOfs(ilv.interleavedData, uvFormat, ilv.stride, ilv.uvsOffset)
                    if ilv.uvSetCount > 1:
                        rapi.rpgBindUV2BufferOfs(ilv.interleavedData, uvFormat, ilv.stride, ilv.uvsOffset + ilv.uvSetSize)
            
        indexType = noesis.RPGEODATA_USHORT if lod.indices.indexSize == 2 else noesis.RPGEODATA_INT
        
        if len(lod.sections) > 0:
            for sectionIndex in range(0, len(lod.sections)):
                section = lod.sections[sectionIndex]
            
                if len(lod.chunks) == len(lod.sections): #if chunks are still around, pull the bonemap out of the corresponding chunk
                    boneMap = lod.chunks[sectionIndex].boneMap
                else: #otherwise assume it's part of the section data
                    boneMap = noeSafeGet(section, "boneMap")
            
                if boneMap:
                    translatedBoneMap = []
                    for boneMapData in boneMap:
                        translatedBoneMap.append(int(boneMapData.data))
                    rapi.rpgSetBoneMap(translatedBoneMap)
            
                if section.materialIndex >= 0 and section.materialIndex < len(mesh.materials) and not noesis.optWasInvoked("-ue4defaultmtl"):
                    materialName = mesh.materials[section.materialIndex].materialName
                else:
                    materialName = "ue4_material_%03i"%section.materialIndex
                    
                if not noesis.optWasInvoked("-ue4nosecname"):
                    if mesh.exportEntry:
                        rapi.rpgSetName(repr(mesh.exportEntry.objectName) + "_section%03i"%sectionIndex)
                    else:
                        rapi.rpgSetName("mesh%03i_section%03i"%(meshIndex, sectionIndex))
                    
                rapi.rpgSetMaterial(materialName)
                rapi.rpgCommitTriangles(lod.indices.data[section.firstIndex * lod.indices.indexSize:], indexType, section.triangleCount * 3, noesis.RPGEO_TRIANGLE, 1)
                rapi.rpgSetBoneMap(None)
        else:
            rapi.rpgCommitTriangles(lod.indices.data, indexType, lod.indices.indexCount, noesis.RPGEO_TRIANGLE, 1)
        
        rapi.rpgClearBufferBinds()
        
        mdl = rapi.rpgConstructModel()
        if mdl:
            if mesh.refSkeleton:
                #convert the bones for this skeleton
                noeBones = []
                for boneIndex in range(0, len(mesh.refSkeleton.boneInfo)):
                    boneInfo = mesh.refSkeleton.boneInfo[boneIndex]
                    bindTransform = mesh.refSkeleton.bindPose[boneIndex]
                    boneName = repr(boneInfo.name)
                    if noesis.optWasInvoked("-ue4bidx"):
                        boneName = "%04i_"%boneIndex + boneName
                    noeBone = NoeBone(boneIndex, boneName, bindTransform.toNoeMat43(), None, boneInfo.parentIndex)
                    noeBones.append(noeBone)
                noeBones = rapi.multiplyBones(noeBones)
                mdl.setBones(noeBones)
            mdlList.append(mdl)

    if mdlMats:
        #if no model exists, create a container for the texture(s)
        if len(mdlList) == 0:
            mdlList.append(NoeModel())
        #associate shared textures + materials with all models
        for mdl in mdlList:
            mdl.setModelMaterials(mdlMats)
        
    if len(mdlList) != 0:
        rapi.setPreviewOption("setAngOfs", "0 90 0")
        rapi.setPreviewOption("autoLoadNonDiffuse", "1")
    else:
        print("Found nothing of interest in the package.")
        
    return 1
        

#=================================================================
# Archive handling
#=================================================================

def ue4FileReadString(f, endian):
    stringLength = noeUnpack(endian + "i", f.read(4))[0]
    if stringLength >= 0:
        return noeStrFromBytes(f.read(stringLength), "UTF-8")
    else:
        return noeStrFromBytes(f.read(-stringLength * 2), "UTF-16")
        
class UE4ArcEntry:
    def __init__(self, name, offset, compSize, decompSize, compType, encrypted, chunkList, chunkSize, entryOffset, entrySize):
        self.name = name
        self.offset = offset
        self.compSize = compSize
        self.decompSize = decompSize
        self.compType = compType
        self.encrypted = encrypted
        self.chunkList = chunkList
        self.chunkSize = chunkSize
        self.entryOffset = entryOffset
        self.entrySize = entrySize
        
def ue4DecryptData(data, key):
    if key is None or len(data) == 0:
        return data
    data = rapi.decryptAES(data, key)
    return data
        
#see if the file in question is a valid pak file
def ue4ExtractArc(fileName, fileLen, justChecking):
    if fileLen <= 44:
        return 0
    with open(fileName, "rb") as f:
        try:
            f.seek(fileLen - 44, os.SEEK_SET)
            endian = "<"
            id = noeUnpack(endian + "I", f.read(4))[0]
            if id == 0xE1126F5A:
                endian = ">"
            elif id != 0x5A6F12E1:
                return 0
                
            ver, entriesOffset, entriesSize = noeUnpack(endian + "IQI", f.read(4 + 8 + 4))
            if ver != 3 or entriesOffset <= 0 or entriesSize <= 0:
                return 0
        except:
            return 0

        if justChecking: #it's valid
            return 1
        
        f.seek(entriesOffset, os.SEEK_SET)
        basePath = ue4FileReadString(f, endian)
        entryCount = noeUnpack(endian + "I", f.read(4))[0]
        
        print("Extracting", entryCount, "files.")
        
        anyEncryption = False
        entries = []
        for entryIndex in range(0, entryCount):
            name = ue4FileReadString(f, endian)
            entryOffset = f.tell()
            offset, compSize, decompSize, compType = noeUnpack(endian + "QQQI", f.read(8 + 8 + 8 + 4))
            f.seek(20, os.SEEK_CUR) #unused
            chunkList = []
            if compType != 0:
                chunkCount = noeUnpack(endian + "I", f.read(4))[0]
                for chunkIndex in range(0, chunkCount):
                    chunkOffset, nextChunkOffset = noeUnpack(endian + "QQ", f.read(8 + 8))
                    chunkList.append((chunkOffset, nextChunkOffset))
            encrypted, chunkSize = noeUnpack(endian + "BI", f.read(1 + 4))
            entrySize = f.tell() - entryOffset
            if encrypted > 0:
                anyEncryption = True
            entries.append(UE4ArcEntry(name, offset, compSize, decompSize, compType, encrypted, chunkList, chunkSize, entryOffset, entrySize))
    
        if anyEncryption:
            decryptKey = noesis.userPrompt(noesis.NOEUSERVAL_STRING, "Enter Key", "Some entries in this archive are encrypted. Please enter a decryption key.", "", None)
            if decryptKey is None:
                print("Warning: No key provided. Proceeding to extract data without decryption. Results may be invalid.")
            else:
                decryptKey = noePaddedByteArray(bytearray(decryptKey, "ASCII"), 32)
    
        for entry in entries:
            print("Writing", entry.name)
            if len(entry.chunkList) > 0:
                data = bytearray()
                for chunkOffset, nextChunkOffset in entry.chunkList:
                    f.seek(chunkOffset, os.SEEK_SET)
                    chunkReadSize = nextChunkOffset - chunkOffset
                    if entry.encrypted > 0: #needs to be padded out to aes block size
                        chunkReadSize = (chunkReadSize + 15) & ~15
                        
                    chunkData = f.read(chunkReadSize)
                    if entry.encrypted > 0:
                        chunkData = ue4DecryptData(chunkData, decryptKey)
                    if entry.compType > 0:
                        chunkData = rapi.decompInflate(chunkData, entry.chunkSize)
                    data += chunkData
            else:
                f.seek(entry.offset + entry.entrySize, os.SEEK_SET)
                readSize = entry.compSize
                if entry.encrypted > 0: #needs to be padded out to aes block size
                    readSize = (readSize + 15) & ~15
                
                data = f.read(readSize)
                if entry.encrypted > 0:
                    data = ue4DecryptData(data, decryptKey)
                if entry.compType > 0:
                    data = rapi.decompInflate(fileData, entry.decompSize)

            if len(data) > entry.decompSize:
                #encryption or compression might've resulted on padding off the end, so be lazy and just truncate at the end before writing.
                data = data[:entry.decompSize]
            rapi.exportArchiveFile(entry.name, data)
            
    return 1
