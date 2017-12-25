from inc_noesis import *
import noesis
import rapi

def registerNoesisTypes():
    handle = noesis.register('VF 5 _obj.bin', '.bin')
    noesis.setHandlerTypeCheck(handle, checkType)
    noesis.setHandlerLoadModel(handle, loadModel)
    return 1

def checkType(data):
    bs = NoeBitStream(data)
    magic = bs.readInt()
    if len(data) < 4:
        return 0
    if magic != 0x05062500:
        return 0
    return 1

def loadModel(data, mdlList):
    loader = DreamyTheaterLoader(data, mdlList)
    loader.load()

def readFixedString(bs, length):
    return bs.readBytes(length).decode('ASCII').rstrip('\0')

class Header:
    def __init__(self, bs):
        self.magic = bs.readUInt()
        self.sectionCount = bs.readUInt()
        self.boneCount = bs.readUInt()
        self.sectionOffsetsStart = bs.readUInt()
        self.bonesOffsetsStart = bs.readUInt()
        self.meshNameOffsetsStart = bs.readUInt()
        self.nameSectionIdOffsetsStart = bs.readUInt()
        self.texNameIdsStart = bs.readUInt()
        self.texNameIdsCount = bs.readUInt()

class Section:
    def __init__(self, bs):
        self.name = None
        self.materialSections = []
        self.meshes = []
        self.boneSection = None

        self.unk1 = bs.readUInt()
        self.unk2 = bs.readUInt()
        self.unkFloat1 = bs.readFloat()
        self.unkFloat2 = bs.readFloat()
        self.unkFloat3 = bs.readFloat()
        self.unkFloat4 = bs.readFloat()
        self.meshCount = bs.readUInt()
        self.meshTableStart = bs.readUInt()
        self.materialCount = bs.readUInt()
        self.materialSectionStart = bs.readUInt()

class Mesh:
    def __init__(self, bs):
        self.faceSections = []

        self.unk1 = bs.readFloat()
        self.unk2 = bs.readFloat()
        self.unk3 = bs.readFloat()
        self.unk4 = bs.readFloat()
        self.unk5 = bs.readFloat()
        self.meshFaceSectionCount = bs.readUInt()
        self.meshFaceHeaderStart = bs.readUInt()
        self.unk_C13_17 = bs.readUInt()
        self.unkNum50 = bs.readUInt()
        self.vertexCount = bs.readUInt()
        self.vertexStart = bs.readUInt()
        self.normalStart = bs.readUInt()
        self.vertexColorStart = bs.readUInt()
        self.unkNull01 = bs.readUInt()
        self.uvStart = bs.readUInt()
        self.stageStruct2Start = bs.readUInt()
        self.unk6 = bs.readFloat()
        self.unk7 = bs.readFloat()
        self.stageStruct1Start = bs.readUInt()
        self.unk8 = bs.readFloat()
        self.weightStart = bs.readUInt()
        self.boneIdStart = bs.readUInt()
        self.unkMatrix = bs.read('16I')
        self.meshName = readFixedString(bs, 64)

class FaceSection:
    def __init__(self, bs):
        self.unk1 = bs.readFloat()
        self.unk2 = bs.readFloat()
        self.unk3 = bs.readFloat()
        self.unk4 = bs.readFloat()
        self.unk5 = bs.readFloat()
        self.matNumber = bs.readUInt()
        self.unk6 = bs.readFloat()
        self.unk7 = bs.readFloat()
        self.faceCount1 = bs.readUInt()
        self.faceOffset1 = bs.readUInt()
        self.unk_Num4 = bs.readUInt()
        self.facetype = bs.readUInt()
        self.unk_Num1 = bs.readUInt()
        self.faceCount2 = bs.readUInt()
        self.faceOffset2 = bs.readUInt()
        self.unk8 = bs.readUInt()
        self.null1 = bs.readUInt()
        self.null2 = bs.readUInt()
        self.null3 = bs.readUInt()
        self.null4 = bs.readUInt()
        self.null5 = bs.readUInt()
        self.null6 = bs.readUInt()
        self.null7 = bs.readUInt()

class MaterialUnk:
    def __init__(self, bs):
        self.numUnk = bs.readUInt()
        self.unk1 = bs.readUInt()
        self.unk2 = bs.readUInt()
        self.unk3 = bs.readFloat()
        self.unk4 = bs.readFloat()
        self.unk5 = bs.readFloat()
        self.unk6 = bs.readFloat()
        self.unk7 = bs.readFloat()
        self.unk8 = bs.readFloat()
        self.unk9 = bs.readFloat()
        self.unk10 = bs.readFloat()
        self.unk11 = bs.readFloat()
        self.unk12 = bs.readFloat()
        self.unk13 = bs.readFloat()
        self.unk14 = bs.readFloat()
        self.unk15 = bs.readFloat()
        self.unk16 = bs.readFloat()
        self.unk17 = bs.readFloat()
        self.unk18 = bs.readFloat()
        self.unk19 = bs.readFloat()
        self.unk20 = bs.readFloat()
        self.unk21 = bs.readFloat()
        self.unk22 = bs.readFloat()
        self.unk23 = bs.readFloat()
        self.unk24 = bs.readFloat()
        self.unk25 = bs.readFloat()
        self.unk26 = bs.readFloat()
        self.unk27 = bs.readFloat()
        self.unk28 = bs.readFloat()
        self.unk_0xFFFFFFFF = bs.readUInt()

class MaterialUnkFloats:
    def __init__(self, bs):
        self.numUnk = bs.readUInt()
        self.unk1 = bs.readUInt()
        self.unk2 = bs.readFloat()
        self.unk3 = bs.readFloat()
        self.unk4 = bs.readFloat()
        self.unk5 = bs.readFloat()
        self.unk6 = bs.readFloat()
        self.unk7 = bs.readFloat()
        self.unk8 = bs.readFloat()
        self.unk9 = bs.readFloat()
        self.unk10 = bs.readFloat()
        self.unk11 = bs.readFloat()
        self.unk12 = bs.readFloat()
        self.unk13 = bs.readFloat()
        self.unk14 = bs.readFloat()
        self.unk15 = bs.readFloat()
        self.unk16 = bs.readFloat()
        self.unk17 = bs.readFloat()
        self.unk18 = bs.readFloat()
        self.unk19 = bs.readFloat()
        self.unk20 = bs.readFloat()
        self.unk21 = bs.readFloat()
        self.unk22 = bs.readFloat()
        self.unk23 = bs.readFloat()
        self.unk24 = bs.readFloat()
        self.unk25 = bs.readFloat()
        self.unk26 = bs.readFloat()
        self.unk27 = bs.readFloat()

        self.numUnk2 = bs.readUInt()
        self.unk28 = bs.readFloat()
        self.unk29 = bs.readFloat()
        self.unk30 = bs.readFloat()
        self.unk31 = bs.readFloat()
        self.unk32 = bs.readFloat()
        self.unk33 = bs.readFloat()
        self.unk34 = bs.readFloat()
        self.unk35 = bs.readFloat()
        self.unk36 = bs.readFloat()
        self.unk37 = bs.readFloat()
        self.unk38 = bs.readFloat()
        self.unk39 = bs.readFloat()
        self.unk40 = bs.readFloat()
        self.unk41 = bs.readFloat()
        self.unk42 = bs.readFloat()
        self.unk43 = bs.readFloat()
        self.unk44 = bs.readFloat()

        self.unk45 = bs.readUInt()
        self.unk46 = bs.readUInt()
        self.unk47 = bs.readUInt()
        self.unk48 = bs.readUInt()
        self.unk49 = bs.readUInt()

class MaterialSection:
    def __init__(self, bs):
        self.unk = bs.readUInt()
        self.unk = bs.readUInt()
        self.materialType = readFixedString(bs, 8)
        self.unk = bs.readUInt()
        self.unk = bs.readUInt()
        self.texDbNumber = bs.readUInt()
        self.materialUnknowns = []
        for i in range(7):
            self.materialUnknowns.append(MaterialUnk(bs))
        self.materialUnkFloats = MaterialUnkFloats(bs)
        self.matName = readFixedString(bs, 40)
        self.mat11 = bs.readFloat()
        self.mat12 = bs.readFloat()
        self.mat13 = bs.readFloat()
        self.mat14 = bs.readFloat()
        self.mat21 = bs.readFloat()
        self.mat22 = bs.readFloat()
        self.mat23 = bs.readFloat()
        self.mat24 = bs.readFloat()
        self.mat31 = bs.readFloat()
        self.mat32 = bs.readFloat()
        self.mat33 = bs.readFloat()
        self.mat34 = bs.readFloat()
        self.mat41 = bs.readFloat()
        self.mat42 = bs.readFloat()
        self.mat43 = bs.readFloat()
        self.mat44 = bs.readFloat()
        self.unk = bs.readUInt()
        self.unk = bs.readUInt()
        self.unk = bs.readUInt()
        self.unk = bs.readUInt()
        self.unk = bs.readUInt()
        self.unk = bs.readUInt()

class BoneSection:
    def __init__(self, bs):
        self.boneParents = []
        self.boneMatrices = []
        self.boneNames = []

        self.boneParentsStart = bs.readUInt()
        self.boneMatricesStart = bs.readUInt()
        self.boneNameOffsetsStart = bs.readUInt()
        self.boneOffset4 = bs.readUInt() # can be null
        self.boneCount = bs.readUInt()
        self.boneOffset5 = bs.readUInt()

class BoneMatrix:
    def __init__(self, bs):
        self.matrix11 = bs.readFloat()
        self.matrix12 = bs.readFloat()
        self.matrix13 = bs.readFloat()
        self.matrix14 = bs.readFloat()
        self.matrix21 = bs.readFloat()
        self.matrix22 = bs.readFloat()
        self.matrix23 = bs.readFloat()
        self.matrix24 = bs.readFloat()
        self.matrix31 = bs.readFloat()
        self.matrix32 = bs.readFloat()
        self.matrix33 = bs.readFloat()
        self.matrix34 = bs.readFloat()
        self.matrix41 = bs.readFloat()
        self.matrix42 = bs.readFloat()
        self.matrix43 = bs.readFloat()
        self.matrix44 = bs.readFloat()

class DreamyTheaterLoader:
    def __init__(self, data, mdlList):
        self.data = data
        self.mdlList = mdlList
        self.texList = []
        self.matList = []
        self.boneList = []
        self.animList = []
        self.textureIdToName = {}
        self.texNameIds = []
        self.bs = NoeBitStream(self.data)
        self.baseName = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))[:-4]
        self.boneData_Array = []

    def load(self):
        ctx = rapi.rpgCreateContext()

        self.load_binTexDB()
        self.load_binBone()
        self.load_BinModel()
        self.load_binTex()

        mdl = rapi.rpgConstructModel()
        mdl.setModelMaterials(NoeModelMaterials(self.texList, self.matList))
        mdl.setBones(self.boneList)
        mdl.setAnims(self.animList)
        self.mdlList.append(mdl)

    def load_binTexDB(self):
        data = rapi.loadIntoByteArray(rapi.getDirForFilePath(rapi.getLastCheckedName()) + 'tex_db.bin')
        bs = NoeBitStream(data)
        tableOffsetCount = bs.readUInt()
        tableOffset = bs.readUInt()
        bs.setOffset(tableOffset)

        for i in range(tableOffsetCount):
            id = bs.readUInt()
            nameOffset = bs.readUInt()
            currentOffset = bs.getOffset()
            bs.setOffset(nameOffset)
            name = bs.readString()
            bs.setOffset(currentOffset)
            self.textureIdToName[id] = name

    def load_binBone(self):
        data = rapi.loadIntoByteArray(rapi.getDirForFilePath(rapi.getLastCheckedName()) + 'bone_data.bin')

        bs = NoeBitStream(data)
        idString = bs.readInt()
        sectionCount = bs.readInt()
        skeletonsOff = bs.readInt()
        unk1 = bs.readInt()
        skeletonInfo = []
        character = []
        bs.seek(skeletonsOff)

        for i in range(sectionCount):
            sI = bs.readInt()
            skeletonInfo.append(sI)

        for i in range(sectionCount):
            character.append(bs.readString())

        characterName = self.baseName[:-6]

        if characterName.upper() in character:
            bs.seek(skeletonInfo[character.index(characterName.upper())])
        else:
            bs.seek(skeletonInfo[0])

        unk2 = bs.readInt()
        skelCount1 = bs.readInt()
        skelMatrixOff = bs.readInt()
        unk3 = bs.readInt()
        skelCount2 = bs.readInt()
        skelNameOff1 = bs.readInt()
        skelCount3 = bs.readInt()
        skelNameOff2 = bs.readInt()
        skelParents = bs.readInt()
        boneMatrix_Array = []
        bs.seek(skelMatrixOff)

        for i in range(skelCount1):
            m01, m02, m03 = bs.read('3f')
            boneMatrix_Array.append((m01, m02, m03))

        boneNames1_Array = []
        bs.seek(skelNameOff1)
        current = bs.tell()

        for i in range(skelCount2):
            bs.seek(current)
            boneNameOff = bs.readInt()
            current = bs.tell()
            bs.seek(boneNameOff)
            boneNames1_Array.append(bs.readString())

        boneNames2_Array = []
        bs.seek(skelNameOff2)
        current = bs.tell()

        for i in range(skelCount3):
            bs.seek(current)
            boneNameOff = bs.readInt()
            current = bs.tell()
            bs.seek(boneNameOff)
            boneNames2_Array.append(bs.readString())

        boneParent_Array = []
        bs.seek(skelParents)

        for i in range(skelCount3):
            bpa = bs.readShort()
            boneParent_Array.append(bpa)

        bones = []

        for i in range(skelCount3):
            if boneNames2_Array[i] in boneNames1_Array:
                index = boneNames1_Array.index(boneNames2_Array[i])
                pos = NoeVec3(boneMatrix_Array[index + 2])
            else:
                pos = NoeVec3((0, 0, 0))
            boneMtx = NoeMat43()
            boneMtx[3] = pos
            bones.append(boneMtx)

        self.boneData_Array.append(boneNames2_Array)
        self.boneData_Array.append(boneParent_Array)
        self.boneData_Array.append(bones)

    def load_BinModel(self):
        bs = self.bs

        # header
        header = Header(bs)

        # sectionOffsets
        bs.setOffset(header.sectionOffsetsStart)
        sectionOffsets = bs.read(str(header.sectionCount) + 'i')

        # boneSectionOffsets
        bs.setOffset(header.bonesOffsetsStart)
        boneSectionOffsets = bs.read(str(header.sectionCount) + 'i')

        # meshNameOffsets
        bs.setOffset(header.meshNameOffsetsStart)
        meshNameOffsets = bs.read(str(header.sectionCount) + 'i')

        # nameSectionIdOffsets
        bs.setOffset(header.nameSectionIdOffsetsStart)
        nameSectionIdOffsets = bs.read(str(header.sectionCount) + 'i')

        # texNameIds
        bs.setOffset(header.texNameIdsStart)
        self.texNameIds = bs.read(str(header.texNameIdsCount) + 'i')

        sections = []
        matDupCheck = []
        for i in range(header.sectionCount):
            sectionOffset = sectionOffsets[i]
            nameSectionOffset = meshNameOffsets[i]
            boneSectionOffset = boneSectionOffsets[i]

            # section
            bs.setOffset(sectionOffset)
            section = Section(bs)
            sections.append(section)

            # meshes
            bs.setOffset(sectionOffset + section.meshTableStart)
            for j in range(section.meshCount):
                section.meshes.append(Mesh(bs))

            # materialSections # TODO: cleanup this mess
            if(section.materialSectionStart > 0):
                bs.setOffset(sectionOffset + section.materialSectionStart)

                materialNames = []
                uvScales = []
                for a in range(0, section.materialCount):
                    bs.seek(0x8, NOESEEK_REL)
                    matType = readFixedString(bs, 8)
                    materialInfos = []

                    for b in range(0, 8):
                        unk1 = bs.readInt()
                        unk2 = bs.readInt()
                        textureId = bs.readInt()
                        textureType = bs.readInt()

                        if b == 0:
                            bs.seek(0x0C, NOESEEK_REL)
                            uvX = bs.readFloat()
                            bs.seek(0x10, NOESEEK_REL)
                            uvY = bs.readFloat()
                            bs.seek(0x10, NOESEEK_REL)
                            uvZ = bs.readFloat()
                            uvScales.append([uvX, uvY, uvZ])
                            bs.seek(0x30, NOESEEK_REL)
                        else:
                            bs.seek(0x68, NOESEEK_REL)

                        materialInfos.append({ 'textureType': textureType, 'textureId': textureId })

                    bs.seek(0x8, NOESEEK_REL)
                    diffColour = bs.read('4f')
                    ambiColour = bs.read('4f')
                    specColour = bs.read('4f')
                    lightColour = bs.read('4f')
                    specPower = bs.readFloat()
                    bs.seek(0x14, NOESEEK_REL)
                    matName = readFixedString(bs, 64)
                    bs.seek(0x40, NOESEEK_REL)

                    if matName in matDupCheck:
                        matName = matName + '_' + str(count)
                        count += 1
                    else:
                        pass

                    matDupCheck.append(matName)
                    material = NoeMaterial(matType + '_' + matName, '')

                    for b in range(0, 8):
                        materialInfo = materialInfos[b]
                        textureId = materialInfo['textureId']
                        textureType = materialInfo['textureType']

                        if textureId == -1:
                            continue

                        textureName = self.textureIdToName[textureId]

                        if textureType == 241:
                            if b == 0:
                                material.setTexture(textureName)
                            else:
                                # TODO: set toon texture here
                                pass
                        elif textureType == 242:
                            material.setNormalTexture(textureName)
                        elif textureType == 243:
                            material.setSpecularTexture(textureName)
                        elif textureType == 247:
                            # TODO: not implemented texture type
                            pass
                        elif textureType == 1017:
                            material.setEnvTexture(textureName)
                        else:
                            print('Not implemented texture type: ' + str(textureType))

                    material.setDiffuseColor(diffColour)
                    material.setSpecularColor([specColour[0], specColour[1], specColour[2], specPower])
                    self.matList.append(material)
                    materialNames.append(matType + '_' + matName)

                # for j in range(section.materialCount):
                #     section.materialSections.append(MaterialSection(bs))

            for mesh in section.meshes:
                # faceSections
                bs.setOffset(sectionOffset + mesh.meshFaceHeaderStart)
                for k in range(mesh.meshFaceSectionCount):
                    mesh.faceSections.append(FaceSection(bs))

                # vertices
                if(mesh.vertexStart > 0):
                    bs.setOffset(sectionOffset + mesh.vertexStart)
                    vertices = bs.readBytes(mesh.vertexCount * 12) # 3f
                    rapi.rpgBindPositionBufferOfs(vertices, noesis.RPGEODATA_FLOAT, 12, 0)

                # normals
                if(mesh.normalStart > 0):
                    bs.setOffset(sectionOffset + mesh.normalStart)
                    normals = bs.readBytes(mesh.vertexCount * 12) # 3f
                    rapi.rpgBindNormalBufferOfs(normals, noesis.RPGEODATA_FLOAT, 12, 0)

                # vertex colors
                if(mesh.vertexColorStart > 0):
                    bs.setOffset(sectionOffset + mesh.vertexColorStart)
                    # TODO : do something with this
                    vertexColors = bs.readBytes(mesh.vertexCount * 16) # 4f rgba

                # uvs
                if(mesh.uvStart > 0):
                    bs.setOffset(sectionOffset + mesh.uvStart)
                    uvs = bs.readBytes(mesh.vertexCount * 8) # 2f
                    rapi.rpgBindUV1BufferOfs(uvs, noesis.RPGEODATA_FLOAT, 8, 0)

                # stageStructs1
                if(mesh.stageStruct1Start > 0):
                    bs.setOffset(sectionOffset + mesh.stageStruct1Start)
                    # TODO : do something with this
                    stageStructs1 = bs.readBytes(mesh.vertexCount * 16) # 4f

                # stageStructs2
                if(mesh.stageStruct2Start > 0):
                    bs.setOffset(sectionOffset + mesh.stageStruct2Start)
                    # TODO : do something with this
                    stageStructs1 = bs.readBytes(mesh.vertexCount * 8) # 2f

                # weights
                if(mesh.weightStart > 0):
                    bs.setOffset(sectionOffset + mesh.weightStart)
                    # TODO : do something with this
                    weights = bs.readBytes(mesh.vertexCount * 16) # 4f

                # boneIds
                if(mesh.boneIdStart > 0):
                    bs.setOffset(sectionOffset + mesh.boneIdStart)
                    # TODO : do something with this
                    boneIds = bs.readBytes(mesh.vertexCount * 16) # 4f

                # faces
                for faceSection in mesh.faceSections:
                    # faces
                    if(faceSection.faceOffset1 > 0):
                        bs.setOffset(sectionOffset + faceSection.faceOffset1)
                        # TODO : do something with this
                        faces = bs.readBytes(faceSection.faceCount1 * 2) # 2H

                    # faces
                    if(faceSection.faceOffset2 > 0):
                      bs.setOffset(sectionOffset + faceSection.faceOffset2)
                      faces = bs.readBytes(faceSection.faceCount2 * 2) # 2H
                      rapi.rpgSetMaterial(materialNames[faceSection.matNumber])
                      rapi.rpgCommitTriangles(faces, noesis.RPGEODATA_USHORT, faceSection.faceCount2, noesis.RPGEO_TRIANGLE_STRIP, 1)

            # sectionNames
            if(nameSectionOffset > 0):
                bs.setOffset(nameSectionOffset)
                section.name = bs.readString()

            # boneSections
            if(boneSectionOffset > 0):
                bs.setOffset(boneSectionOffset)
                section.boneSection = BoneSection(bs)

            # boneParents
            boneSection = section.boneSection
            boneCount = boneSection.boneCount
            if(boneSectionOffset > 0 and boneSection.boneParentsStart > 0):
                bs.setOffset(boneSection.boneParentsStart)
                boneSection.boneParents = bs.read(str(boneCount) + 'i')

            # bone matrices
            if(boneSectionOffset > 0 and boneSection.boneMatricesStart > 0):
                bs.setOffset(boneSection.boneMatricesStart)
                for j in range(boneCount):
                    boneMatrix = BoneMatrix(bs)
                    boneSection.boneMatrices.append(boneMatrix)

            # bone names
            boneNameOffsetsStart = boneSection.boneNameOffsetsStart
            if(boneSectionOffset > 0 and boneNameOffsetsStart > 0 and boneCount > 0):

                bs.setOffset(boneNameOffsetsStart)
                boneNameOffsets = bs.read(str(boneCount) + 'i')

                for boneNameOffset in boneNameOffsets:
                    bs.setOffset(boneNameOffset)
                    boneName = bs.readString()
                    boneSection.boneNames.append(boneName)

    def load_binTex(self):
        data = rapi.loadIntoByteArray(rapi.getDirForFilePath(rapi.getLastCheckedName()) + self.baseName + '_tex.bin')
        bs = NoeBitStream(data)

        # header
        idString = bs.readInt() # TXP3
        texCount = bs.readInt()
        unk1 = bs.readInt()
        texOffsets = bs.read(str(texCount) + 'i')

        for i in range(texCount):
            texOffset = texOffsets[i]
            bs.setOffset(texOffset)

            # mipMapInfo
            txpType2 = bs.readInt() # TXP4 or TXP5
            numMips = bs.readInt()
            unk2 = bs.readInt()
            mipsOffsets = bs.read(str(numMips) + 'i')

            # read all mipmaps
            # for j in range(numMips):

            # read first mipmap
            for j in range(1):
                mipsOffset = mipsOffsets[j]
                bs.setOffset(texOffset + mipsOffset)

                # texInfo
                txpType3 = bs.readInt()
                width = bs.readInt()
                height = bs.readInt()
                ddsType = bs.readInt()
                null = bs.readInt()
                size = bs.readInt()
                txpData = bs.readBytes(size)

                texFmt = 0

                if ddsType == 1:
                    texFmt = noesis.NOESISTEX_RGB24
                elif ddsType == 2:
                    texFmt = noesis.NOESISTEX_RGBA32
                elif ddsType == 6:
                    texFmt = noesis.NOESISTEX_DXT1
                elif ddsType == 7:
                    texFmt = noesis.NOESISTEX_DXT3
                elif ddsType == 9:
                    texFmt = noesis.NOESISTEX_DXT5
                elif ddsType == 11:
                    txpData = rapi.imageDecodeDXT(txpData, width, height, noesis.FOURCC_ATI2)
                    texFmt = noesis.NOESISTEX_RGBA32
                else:
                    print('Not implemented DDS type: ' + str(ddsType))

                name = self.textureIdToName[self.texNameIds[i]]
                texture = NoeTexture(name, width, height, txpData, texFmt)
                self.texList.append(texture)
