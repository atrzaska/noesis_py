# https://gist.github.com/felixjones/f8a06bd48f9da9a4539f
# https://gist.github.com/felixjones/8ad4a1e50bbced75b46b
# TODO: implement pmx 2.1 softBodies

from inc_noesis import *
import noesis
import rapi

ENCODINGS = {
    0: 'UTF16',
    1: 'UTF8'
}

WEIGHT_TYPES = {
    0: 'BDEF1',
    1: 'BDEF2',
    2: 'BDEF4',
    4: 'SDEF'
}

INDEX_TYPES = {
    'vertex': { 1: 'B', 2: 'H', 4: 'I' },
    'bone': { 1: 'b', 2: 'h', 4: 'i' },
    'texture': { 1: 'b', 2: 'h', 4: 'i' },
    'material': { 1: 'b', 2: 'h', 4: 'i' },
    'morph': { 1: 'b', 2: 'h', 4: 'i' },
    'rigidbody': { 1: 'b', 2: 'h', 4: 'i' },
}

INDICES_TYPES = {
    1: noesis.RPGEODATA_UBYTE,
    2: noesis.RPGEODATA_USHORT,
    4: noesis.RPGEODATA_INT,
}

BONEFLAG_TAILPOS_IS_BONE = 0x0001
BONEFLAG_CAN_ROTATE = 0x0002
BONEFLAG_CAN_TRANSLATE = 0x0004
BONEFLAG_IS_VISIBLE = 0x0008
BONEFLAG_CAN_MANIPULATE = 0x0010
BONEFLAG_IS_IK = 0x0020
BONEFLAG_IS_UNK1 = 0x0040
BONEFLAG_IS_UNK2 = 0x0080
BONEFLAG_IS_EXTERNAL_ROTATION = 0x0100
BONEFLAG_IS_EXTERNAL_TRANSLATION = 0x0200
BONEFLAG_HAS_FIXED_AXIS = 0x0400
BONEFLAG_HAS_LOCAL_COORDINATE = 0x0800
BONEFLAG_IS_AFTER_PHYSICS_DEFORM = 0x1000
BONEFLAG_IS_EXTERNAL_PARENT_DEFORM = 0x2000

def registerNoesisTypes():
    handle = noesis.register('Miku Miku Dance PMX', '.pmx')
    noesis.setHandlerTypeCheck(handle, checkType)
    noesis.setHandlerLoadModel(handle, loadModel)
    return 1

def checkType(data):
    bs = NoeBitStream(data)
    signature = bs.readUInt()

    if len(data) < 4:
        return 0
    if signature != 542657872:
        return 0
    return 1

def loadModel(data, mdlList):
    loader = PmxLoader(data, mdlList)
    loader.load()
    return 1

def readFixedString(bs, length):
    return bs.readBytes(length).decode('ASCII').rstrip('\0')

def hasFlag(flags, flag):
    return (flags & flag) != 0

class PmxLoader:
    def __init__(self, data, mdlList):
        self.data = data
        self.bs = NoeBitStream(self.data)
        self.mdlList = mdlList
        self.texList = []
        self.matList = []
        self.boneList = []
        self.animList = []
        self.baseName = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))

    def load(self):
        ctx = rapi.rpgCreateContext()

        self.loadModel()

        mdl = rapi.rpgConstructModel()
        mdl.setModelMaterials(NoeModelMaterials(self.texList, self.matList))
        mdl.setBones(self.boneList)
        mdl.setAnims(self.animList)
        self.mdlList.append(mdl)

    def readText(self):
        size = self.bs.readInt()
        data = self.bs.readBytes(size)
        return data.decode(self.encoding)

    def readIndex(self, type, size):
        fmt = INDEX_TYPES[type][size]
        data = self.bs.readBytes(size)
        return struct.unpack(fmt, data)[0]

    def readTextureIndex(self):
        return self.readIndex('texture', self.textureIndexSize)

    def readBoneIndex(self):
        return self.readIndex('bone', self.boneIndexSize)

    def readMorphIndex(self):
        return self.readIndex('morph', self.morphIndexSize)

    def readVertexIndex(self):
        return self.readIndex('vertex', self.vertexIndexSize)

    def readMaterialIndex(self):
        return self.readIndex('material', self.materialIndexSize)

    def readRigidbodyIndex(self):
        return self.readIndex('rigidbody', self.rigidBodyIndexSize)

    def readVec2(self):
        return self.bs.read('2f')

    def readVec3(self):
        return self.bs.read('3f')

    def readVec4(self):
        return self.bs.read('4f')

    def readQuaternion(self):
        return self.bs.read('4f')

    def readRgb(self):
        return self.bs.read('3f')

    def readRgba(self):
        return self.bs.read('4f')

    def loadModel(self):
        bs = self.bs

        # header
        signature = bs.readUInt()
        version = bs.readFloat() # 2.0 or 2.1
        length = bs.readByte() # 8
        encodingId = bs.readByte() # 0 = UTF-16, 1 = UTF-8
        self.encoding = ENCODINGS[encodingId]
        self.appendixUVSize = bs.readByte() # 0-4
        self.vertexIndexSize = bs.readByte() # 1 = ubyte, 2 = ushort, 4 = int
        self.textureIndexSize = bs.readByte() # 1 = byte, 2 = short, 4 = int
        self.materialIndexSize = bs.readByte() # 1 = byte, 2 = short, 4 = int
        self.boneIndexSize = bs.readByte() # 1 = byte, 2 = short, 4 = int
        self.morphIndexSize = bs.readByte() # 1 = byte, 2 = short, 4 = int
        self.rigidBodyIndexSize = bs.readByte() # 1 = byte, 2 = short, 4 = int

        # names
        characterName = self.readText()
        englishCharacterName = self.readText()
        comment = self.readText()
        englishComment = self.readText()

        # vertices
        vertices = ''
        normals = ''
        uvs = ''

        vertexCount = bs.readInt()

        for i in range(vertexCount):
            position = bs.readBytes(12)
            normal = bs.readBytes(12)
            uv = bs.readBytes(8)
            appendixUV = bs.readBytes(4 * self.appendixUVSize)
            weightTypeId = bs.readByte()

            # 0 = BDEF1, 1 = BDEF2, 2 = BDEF4, 4 = SDEF
            # 0 = BDEF1, 1 = BDEF2, 2 = BDEF4, 3 = SDEF, 4 = QDEF
            # bone index -1 should means null
            if weightTypeId == 0:
                bone1Index = self.readBoneIndex()
                boneWeight = 1.0
            elif weightTypeId == 1:
                bone1Index = self.readBoneIndex()
                bone2Index = self.readBoneIndex()
                bone1Weight = bs.readFloat()
                bone2Weight = 1 - bone1Weight
            elif weightTypeId == 2:
                bone1Index = self.readBoneIndex()
                bone2Index = self.readBoneIndex()
                bone3Index = self.readBoneIndex()
                bone4Index = self.readBoneIndex()
                bone1Weight = bs.readFloat()
                bone2Weight = bs.readFloat()
                bone3Weight = bs.readFloat()
                bone4Weight = bs.readFloat()
            elif weightTypeId == 3:
                bone1Index = self.readBoneIndex()
                bone2Index = self.readBoneIndex()
                bone1Weight = bs.readFloat()
                bone2Weight = 1 - bone1Weight
                c = bs.read('3f')
                r0 = bs.read('3f')
                r1 = bs.read('3f')
            elif weightTypeId == 4:
                bone1Index = self.readBoneIndex()
                bone2Index = self.readBoneIndex()
                bone3Index = self.readBoneIndex()
                bone4Index = self.readBoneIndex()
                bone1Weight = bs.readFloat()
                bone2Weight = bs.readFloat()
                bone3Weight = bs.readFloat()
                bone4Weight = bs.readFloat()
            else:
                noesis.doException("unknown weight type id: " + str(weightTypeId))

            edgeScale = bs.readFloat()

            vertices += position
            normals += normal
            uvs += uv

        # faces
        faceCount = bs.readInt()
        facesData = bs.readBytes(self.vertexIndexSize * faceCount)

        # textures
        textureCount = bs.readInt()
        textures = []
        for i in range(textureCount):
            fileName = self.readText().replace('\\', '/')
            textures.append(fileName)

        # materials
        materialCount = bs.readInt()
        startOffset = 0
        endOffset = 0
        for i in range(materialCount):
            name = self.readText()
            englishName = self.readText()
            diffuseColorRGBA = self.readRgba()
            specularColorRGB = self.readRgb()
            specularity = bs.readFloat()
            ambientColorRGB = self.readRgb()
            drawingModeFlag = bs.readByte() # 0x01 = Double-Sided, 0x02 = Shadow, 0x04 = Self shadow mapl 0x08 = Self shadow, 0x10 = Draw edges
            edgeColorRGBA = self.readRgba()
            edgeSize = bs.readFloat()
            textureIndex = self.readTextureIndex()
            sphereIndex = self.readTextureIndex()
            sphereMode = bs.readByte()
            toonFlag = bs.readByte()

            if toonFlag == 0:
                toonIndex = self.readTextureIndex()
            elif toonFlag == 1:
                toonIndex = bs.readByte()

            memo = self.readText()
            matFaceCount = bs.readInt()

            material = NoeMaterial(name, textures[textureIndex])
            self.matList.append(material)
            dataSize = self.vertexIndexSize * matFaceCount
            endOffset = startOffset + dataSize
            currentFaces = facesData[startOffset:endOffset]
            rapi.rpgBindPositionBufferOfs(vertices, noesis.RPGEODATA_FLOAT, 12, 0)
            rapi.rpgBindNormalBufferOfs(normals, noesis.RPGEODATA_FLOAT, 12, 0)
            rapi.rpgBindUV1BufferOfs(uvs, noesis.RPGEODATA_FLOAT, 8, 0)
            rapi.rpgSetMaterial(name)
            rapi.rpgCommitTriangles(currentFaces, INDICES_TYPES[self.vertexIndexSize], matFaceCount, noesis.RPGEO_TRIANGLE, 1)
            startOffset += self.vertexIndexSize * matFaceCount

        # bones
        boneCount = bs.readInt()
        for i in range(boneCount):
            boneName = self.readText()
            boneEnglishName = self.readText()
            position = self.readVec3()
            parentBoneIndex = self.readBoneIndex()
            layer = bs.readInt()
            flags = bs.readShort()

            indexedTailPosition = hasFlag(flags, BONEFLAG_TAILPOS_IS_BONE)

            if indexedTailPosition:
                tailPosition = self.readBoneIndex()
            else:
                tailPosition = self.readVec3()

            externalTranslation = hasFlag(flags, BONEFLAG_IS_EXTERNAL_TRANSLATION)
            externalRotation = hasFlag(flags, BONEFLAG_IS_EXTERNAL_ROTATION)

            if externalTranslation or externalRotation:
                parentIndex = self.readBoneIndex()
                parentInfluence = bs.readFloat()

            fixedAxis = hasFlag(flags, BONEFLAG_HAS_FIXED_AXIS)

            if fixedAxis:
                axisDirection = self.readVec3()

            localCoordinate = hasFlag(flags, BONEFLAG_HAS_LOCAL_COORDINATE)

            if localCoordinate:
                localXVector = self.readVec3()
                localZVector = self.readVec3()

            externalParentDeform = hasFlag(flags, BONEFLAG_IS_EXTERNAL_PARENT_DEFORM)

            if externalParentDeform:
                externalKey = bs.readInt()

            ik = hasFlag(flags, BONEFLAG_IS_IK)

            if ik:
                targetIndex = self.readBoneIndex()
                loopCount = bs.readInt()
                limitRadian = bs.readFloat()
                linkCount = bs.readInt()

                for j in range(linkCount):
                    boneIndex = self.readBoneIndex()
                    hasLimits = bs.readByte()

                    if hasLimits == 1:
                        angleLimitMin = self.readVec3()
                        angleLimitMax = self.readVec3()

        # morphs
        morphCount = bs.readInt()
        for i in range(morphCount):
            name = self.readText()
            englishName = self.readText()
            panel = bs.readByte()
            morphType = bs.readByte()
            offsetSize = bs.readInt()

            if morphType == 0:
                # group
                for j in range(offsetSize):
                    morphIndex = self.readMorphIndex()
                    morphValue = bs.readFloat()
            elif morphType == 1:
                # vertex
                for j in range(offsetSize):
                    vertexIndex = self.readVertexIndex()
                    positionOffset = self.readVec3()
            elif morphType == 2:
                # bone
                for j in range(offsetSize):
                    boneIndex = self.readBoneIndex()
                    position = self.readVec3()
                    rotation = self.readQuaternion()
            elif morphType == 3:
                # uv
                for j in range(offsetSize):
                    vertexIndex = self.readVertexIndex()
                    uv = self.readVec4()
            elif morphType == 4:
                # uv extended1
                for j in range(offsetSize):
                    vertexIndex = self.readVertexIndex()
                    uv = self.readVec4()
            elif morphType == 5:
                # uv extended2
                for j in range(offsetSize):
                    vertexIndex = self.readVertexIndex()
                    uv = self.readVec4()
            elif morphType == 6:
                # uv extended3
                for j in range(offsetSize):
                    vertexIndex = self.readVertexIndex()
                    uv = self.readVec4()
            elif morphType == 7:
                # uv extended4
                for j in range(offsetSize):
                    vertexIndex = self.readVertexIndex()
                    uv = self.readVec4()
            elif morphType == 8:
                # material
                for j in range(offsetSize):
                    materialIndex = self.readMaterialIndex()
                    calcMode = bs.readByte()
                    diffuse = self.readRgba()
                    specular = self.readRgb()
                    specularFactor = bs.readFloat()
                    ambient = self.readRgb()
                    edgeColor = self.readRgba()
                    edgeSize = bs.readFloat()
                    textureFactor = self.readRgba()
                    sphereTextureFactor = self.readRgba()
                    toonTextureFactor = self.readRgba()
            else:
                noesis.doException("unknown morph type: " + str(morphType))

        # displaySlots
        displaySlotCount = bs.readInt()
        for i in range(displaySlotCount):
            displayName = self.readText()
            englishDisplayName = self.readText()
            specialFlag = bs.readByte()
            frameCount = bs.readInt()
            references = []
            for j in range(frameCount):
                displayType = bs.readByte()
                if displayType == 0: # Bone
                    references.append((displayType, self.readBoneIndex()))
                elif displayType == 1: # Morph
                    references.append((displayType, self.readMorphIndex()))
                else:
                    noesis.doException("unknown displayType: " + str(displayType))

        # rigidBodies
        rigidBodyCount = bs.readInt()
        for i in range(rigidBodyCount):
            name = self.readText()
            englishName = self.readText()
            boneIndex = self.readBoneIndex()
            collisionGroup = bs.readByte()
            noCollisionGroup = bs.readShort()
            shapeType = bs.readByte()
            shapeSize = self.readVec3()
            shapePosition = self.readVec3()
            shapeRotation = self.readVec3()
            mass = bs.readFloat()
            linearDamping = bs.readFloat()
            angularDamping = bs.readFloat()
            restitution = bs.readFloat()
            friction = bs.readFloat()
            mode = bs.readByte()

        # joints
        jointCount = bs.readInt()
        for i in range(jointCount):
            name = self.readText()
            english_name = self.readText()
            joint_type = bs.readByte()
            rigidbody_index_a = self.readRigidbodyIndex()
            rigidbody_index_b = self.readRigidbodyIndex()
            position = self.readVec3()
            rotation = self.readVec3()
            translation_limit_min = self.readVec3()
            translation_limit_max = self.readVec3()
            rotation_limit_min = self.readVec3()
            rotation_limit_max = self.readVec3()
            spring_constant_translation = self.readVec3()
            spring_constant_rotation = self.readVec3()

        # softBodies
        if version >= 2.1:
            softBodyCount = bs.readInt()
            for i in range(softBodyCount):
                # TODO: read soft bodies
                pass
