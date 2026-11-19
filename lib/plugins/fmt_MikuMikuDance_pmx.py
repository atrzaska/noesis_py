# https://gist.github.com/felixjones/f8a06bd48f9da9a4539f
# https://gist.github.com/felixjones/8ad4a1e50bbced75b46b
# TODO: implement pmx 2.1 softBodies

from inc_noesis import *
import math
import os
import struct
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
    noesis.addOption(handle, "-pmxvmd", "VMD motion to load with the PMX model (without it, a prompt asks for one).", noesis.OPTFLAG_WANTARG)
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
        # per bone, for VMD motions: name, parent, position, flags, layer, append, IK
        self.mmdBones = []
        self.baseName = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))

    def load(self):
        ctx = rapi.rpgCreateContext()
        # MMD is left-handed (models face -Z): negate Z so the model faces +Z
        rapi.rpgSetTransform(NoeMat43((NoeVec3((1.0, 0.0, 0.0)), NoeVec3((0.0, 1.0, 0.0)), NoeVec3((0.0, 0.0, -1.0)), NoeVec3((0.0, 0.0, 0.0)))))

        self.loadModel()
        self.loadMotion()

        mdl = rapi.rpgConstructModel()
        mdl.setModelMaterials(NoeModelMaterials(self.texList, self.matList))
        mdl.setBones(self.boneList)
        mdl.setAnims(self.animList)
        self.mdlList.append(mdl)

    def vmdPath(self):
        """The VMD to load: -pmxvmd PATH, else asked for (cancel or empty: none)."""
        if noesis.optWasInvoked("-pmxvmd"):
            return noesis.optGetArg("-pmxvmd")
        path = noesis.userPrompt(noesis.NOEUSERVAL_FILEPATH, "VMD motion",
                                 "VMD motion for " + self.baseName + " (empty for none)", "", None)
        return path or ""

    def loadMotion(self):
        if not self.mmdBones:
            return
        path = self.vmdPath()
        if not path:
            return
        if not os.path.isfile(path):
            print("pmx: VMD motion not found: " + path)
            return
        with open(path, "rb") as f:
            vmd = VmdMotion(f.read())
        baker = MmdMotionBaker(self.mmdBones, vmd)
        name = os.path.splitext(os.path.basename(path))[0]
        anim = baker.bake(name, self.boneList)
        if anim is not None:
            self.animList.append(anim)
            print("pmx: motion %s: %d frames, %d of %d bones keyed by name" % (name, baker.frameCount, baker.keyedBones, len(self.mmdBones)))

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
        vertices = b''
        normals = b''
        uvs = b''

        weightIndices = bytearray()
        weightValues = bytearray()

        vertexCount = bs.readInt()

        for i in range(vertexCount):
            position = bs.readBytes(12)
            normal = bs.readBytes(12)
            uv = bs.readBytes(8)
            appendixUV = bs.readBytes(16 * self.appendixUVSize) # each additional UV is a float4
            weightTypeId = bs.readByte()

            # 0 = BDEF1, 1 = BDEF2, 2 = BDEF4, 3 = SDEF, 4 = QDEF (2.1)
            # bone index -1 means none; SDEF is skinned as BDEF2, QDEF as BDEF4
            if weightTypeId == 0:
                boneIndices = [self.readBoneIndex()]
                boneWeights = [1.0]
            elif weightTypeId in (1, 3):
                boneIndices = [self.readBoneIndex(), self.readBoneIndex()]
                weight = bs.readFloat()
                boneWeights = [weight, 1.0 - weight]
                if weightTypeId == 3:
                    bs.readBytes(36) # SDEF C, R0, R1
            elif weightTypeId in (2, 4):
                boneIndices = [self.readBoneIndex() for j in range(4)]
                boneWeights = [bs.readFloat() for j in range(4)]
            else:
                noesis.doException("unknown weight type id: " + str(weightTypeId))
            boneIndices += [-1] * (4 - len(boneIndices))
            boneWeights += [0.0] * (4 - len(boneWeights))
            for j in range(4):
                if boneIndices[j] < 0:
                    boneIndices[j], boneWeights[j] = 0, 0.0
            weightIndices += struct.pack('<4i', *boneIndices)
            weightValues += struct.pack('<4f', *boneWeights)

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
            rapi.rpgBindBoneIndexBufferOfs(bytes(weightIndices), noesis.RPGEODATA_INT, 16, 0, 4)
            rapi.rpgBindBoneWeightBufferOfs(bytes(weightValues), noesis.RPGEODATA_FLOAT, 16, 0, 4)
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
            # model space position, Z negated like the geometry (rpgSetTransform); no rotation
            boneMat = NoeMat43()
            boneMat[3] = NoeVec3((position[0], position[1], -position[2]))
            self.boneList.append(NoeBone(i, boneName, boneMat, None, parentBoneIndex))
            layer = bs.readInt()
            flags = bs.readShort()

            indexedTailPosition = hasFlag(flags, BONEFLAG_TAILPOS_IS_BONE)

            if indexedTailPosition:
                tailPosition = self.readBoneIndex()
            else:
                tailPosition = self.readVec3()

            externalTranslation = hasFlag(flags, BONEFLAG_IS_EXTERNAL_TRANSLATION)
            externalRotation = hasFlag(flags, BONEFLAG_IS_EXTERNAL_ROTATION)

            appendParent, appendRatio = -1, 0.0
            if externalTranslation or externalRotation:
                appendParent = self.readBoneIndex()
                appendRatio = bs.readFloat()

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

            ikData = None
            if ik:
                targetIndex = self.readBoneIndex()
                loopCount = bs.readInt()
                limitRadian = bs.readFloat()
                linkCount = bs.readInt()
                links = []

                for j in range(linkCount):
                    boneIndex = self.readBoneIndex()
                    hasLimits = bs.readByte()
                    angleLimitMin = angleLimitMax = None

                    if hasLimits == 1:
                        angleLimitMin = self.readVec3()
                        angleLimitMax = self.readVec3()
                    links.append((boneIndex, angleLimitMin, angleLimitMax))
                ikData = (targetIndex, loopCount, limitRadian, links)

            self.mmdBones.append(MmdBone(boneName, parentBoneIndex, position, flags, layer,
                                         appendParent if appendParent < boneCount else -1, appendRatio, ikData))

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


# ---- VMD motions ----
# All MMD math is done in the file's own (left-handed) space; the baked local transforms are
# mirrored to the model's (Z negated) at the end. Semantics follow MMD as reimplemented by
# saba (MMDNode/MMDIkSolver) and three.js' MMDLoader: bezier key interpolation, append
# ("grant") rotation/translation, and CCD IK with per-link angle limits (a link limited on one
# axis only, such as a knee, is solved as a hinge). Physics, morphs and cameras are not used.

VMD_FPS = 30.0
IDENTITY_Q = (0.0, 0.0, 0.0, 1.0)


class MmdBone:
    def __init__(self, name, parent, position, flags, layer, appendParent, appendRatio, ik):
        self.name = name
        self.parent = parent
        self.position = tuple(position)
        self.flags = flags
        self.layer = layer
        self.afterPhysics = hasFlag(flags, BONEFLAG_IS_AFTER_PHYSICS_DEFORM)
        self.appendParent = appendParent
        self.appendRatio = appendRatio
        self.appendRotate = hasFlag(flags, BONEFLAG_IS_EXTERNAL_ROTATION) and appendParent >= 0
        self.appendTranslate = hasFlag(flags, BONEFLAG_IS_EXTERNAL_TRANSLATION) and appendParent >= 0
        self.appendLocal = hasFlag(flags, BONEFLAG_IS_UNK2) # 0x80: local append
        self.ik = ik # (target, loops, limit angle, [(link, min, max)]) or None


def vmdName(raw):
    """A VMD name field: bytes up to the first NUL (Shift-JIS, possibly cut mid-character)."""
    end = raw.find(b'\0')
    return raw if end < 0 else raw[:end]


def sjisName(name, size):
    """A PMX name as a VMD stores it: Shift-JIS, cut to the field size."""
    try:
        data = name.encode('cp932')
    except (UnicodeError, LookupError):
        data = name.encode('utf-8', 'replace')
    return data[:size]


class VmdMotion:
    def __init__(self, data):
        bs = NoeBitStream(data)
        header = bs.readBytes(30)
        nameSize = 10 if header.startswith(b'Vocaloid Motion Data file') else 20
        bs.readBytes(nameSize)
        self.boneKeys = {} # raw name -> [(frame, pos, rot, interp)]
        self.ikKeys = {} # raw name (20 bytes) -> [(frame, enabled)]
        count = bs.readUInt()
        for i in range(count):
            name = vmdName(bs.readBytes(15))
            frame = bs.readUInt()
            pos = struct.unpack('<3f', bs.readBytes(12))
            rot = struct.unpack('<4f', bs.readBytes(16))
            interp = bs.readBytes(64)
            self.boneKeys.setdefault(name, []).append((frame, pos, rot, interp))
        for keys in self.boneKeys.values():
            keys.sort(key=lambda k: k[0])
        if not self.skip(bs, 23): # morphs
            return
        if not self.skip(bs, 61): # camera
            return
        if not self.skip(bs, 28): # light
            return
        if not self.skip(bs, 9): # self shadow
            return
        if bs.tell() + 4 > len(data):
            return
        count = bs.readUInt()
        for i in range(count):
            frame = bs.readUInt()
            bs.readUByte() # show
            ikCount = bs.readUInt()
            for j in range(ikCount):
                name = vmdName(bs.readBytes(20))
                enabled = bs.readUByte() != 0
                self.ikKeys.setdefault(name, []).append((frame, enabled))
        for keys in self.ikKeys.values():
            keys.sort(key=lambda k: k[0])

    def skip(self, bs, size):
        """Skips a counted section of fixed-size records; False when the file ends first."""
        if bs.tell() + 4 > bs.getSize():
            return False
        count = bs.readUInt()
        if bs.tell() + count * size > bs.getSize():
            return False
        bs.seek(count * size, NOESEEK_REL)
        return True


def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def qinv(q):
    return (-q[0], -q[1], -q[2], q[3])


def qrot(q, v):
    x, y, z, w = q
    tx = 2.0 * (y * v[2] - z * v[1])
    ty = 2.0 * (z * v[0] - x * v[2])
    tz = 2.0 * (x * v[1] - y * v[0])
    return (v[0] + w * tx + y * tz - z * ty,
            v[1] + w * ty + z * tx - x * tz,
            v[2] + w * tz + x * ty - y * tx)


def qnormalize(q):
    l = math.sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3])
    if l < 1e-12:
        return IDENTITY_Q
    return (q[0] / l, q[1] / l, q[2] / l, q[3] / l)


def qslerp(a, b, t):
    d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]
    if d < 0.0:
        b = (-b[0], -b[1], -b[2], -b[3])
        d = -d
    if d > 0.9999:
        return qnormalize(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    angle = math.acos(min(d, 1.0))
    s = math.sin(angle)
    wa = math.sin((1.0 - t) * angle) / s
    wb = math.sin(t * angle) / s
    return (a[0] * wa + b[0] * wb, a[1] * wa + b[1] * wb, a[2] * wa + b[2] * wb, a[3] * wa + b[3] * wb)


def qaxis(axis, angle):
    s = math.sin(angle * 0.5)
    return (axis[0] * s, axis[1] * s, axis[2] * s, math.cos(angle * 0.5))


AXES = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def qeulerxyz(e):
    """Rx * Ry * Rz (saba's glm::rotate order)."""
    return qmul(qmul(qaxis(AXES[0], e[0]), qaxis(AXES[1], e[1])), qaxis(AXES[2], e[2]))


def normalizeAngle(a):
    twoPi = 2.0 * math.pi
    a = math.fmod(a, twoPi)
    return a + twoPi if a < 0.0 else a


def diffAngle(a, b):
    d = normalizeAngle(a) - normalizeAngle(b)
    if d > math.pi:
        return d - 2.0 * math.pi
    if d < -math.pi:
        return d + 2.0 * math.pi
    return d


def eulerxyz(q, before):
    """The XYZ Euler angles of q (as qeulerxyz builds it) closest to `before` (saba's Decompose)."""
    x, y, z, w = q
    m02 = 2.0 * (x * z + y * w)
    m12 = 2.0 * (y * z - x * w)
    m22 = 1.0 - 2.0 * (x * x + y * y)
    m01 = 2.0 * (x * y - z * w)
    m00 = 1.0 - 2.0 * (y * y + z * z)
    m10 = 2.0 * (x * y + z * w)
    m11 = 1.0 - 2.0 * (x * x + z * z)
    sy = max(-1.0, min(1.0, m02))
    if 1.0 - abs(sy) < 1e-6:
        r = (0.0, math.asin(sy), math.atan2(m10, m11))
    else:
        r = (math.atan2(-m12, m22), math.asin(sy), math.atan2(-m01, m00))
    pi = math.pi
    best = r
    bestErr = sum(abs(diffAngle(r[i], before[i])) for i in range(3))
    for sx in (pi, -pi):
        for sy2 in (pi, -pi):
            for sz in (pi, -pi):
                t = (r[0] + sx, sy2 - r[1], r[2] + sz)
                err = sum(abs(diffAngle(t[i], before[i])) for i in range(3))
                if err < bestErr:
                    best, bestErr = t, err
    return best


def bezier(x1, x2, y1, y2, x):
    """MMD's interpolation curve (control points (x1, y1), (x2, y2) in 0..1), y at x."""
    c = 0.5
    t = c
    s = 1.0 - t
    sst3 = stt3 = ttt = 0.0
    for i in range(15):
        sst3 = 3.0 * s * s * t
        stt3 = 3.0 * s * t * t
        ttt = t * t * t
        ft = sst3 * x1 + stt3 * x2 + ttt - x
        if abs(ft) < 1e-5:
            break
        c *= 0.5
        t += c if ft < 0 else -c
        s = 1.0 - t
    return sst3 * y1 + stt3 * y2 + ttt


class BoneTrack:
    """A bone's VMD keys, evaluated at increasing frames."""

    def __init__(self, keys):
        self.keys = keys
        self.k = 0

    def curve(self, interp, ch, t):
        x1, y1, x2, y2 = interp[ch], interp[ch + 4], interp[ch + 8], interp[ch + 12]
        if x1 == y1 and x2 == y2:
            return t # linear
        return bezier(x1 / 127.0, x2 / 127.0, y1 / 127.0, y2 / 127.0, t)

    def at(self, frame):
        keys = self.keys
        if frame <= keys[0][0]:
            return keys[0][1], keys[0][2]
        if frame >= keys[-1][0]:
            return keys[-1][1], keys[-1][2]
        while keys[self.k + 1][0] < frame:
            self.k += 1
        f0, p0, r0, i0 = keys[self.k]
        f1, p1, r1, i1 = keys[self.k + 1]
        if f1 == frame:
            return p1, r1
        t = float(frame - f0) / (f1 - f0)
        pos = tuple(p0[c] + (p1[c] - p0[c]) * self.curve(i1, c, t) for c in range(3))
        rot = qslerp(r0, r1, self.curve(i1, 3, t))
        return pos, rot


class MmdMotionBaker:
    def __init__(self, bones, vmd):
        self.bones = bones
        n = len(bones)
        self.offsets = []
        for b in bones:
            p = bones[b.parent].position if 0 <= b.parent < n else (0.0, 0.0, 0.0)
            self.offsets.append((b.position[0] - p[0], b.position[1] - p[1], b.position[2] - p[2]))
        self.parents = [b.parent if 0 <= b.parent < n else -1 for b in bones]
        # VMD keys by bone, matched on the Shift-JIS name cut to the VMD's field size
        self.tracks = {}
        self.ikSwitches = {}
        lastFrame = 0
        for i, b in enumerate(bones):
            keys = vmd.boneKeys.get(sjisName(b.name, 15))
            if keys:
                self.tracks[i] = BoneTrack(keys)
                lastFrame = max(lastFrame, keys[-1][0])
            if b.ik is not None:
                switches = vmd.ikKeys.get(sjisName(b.name, 20))
                if switches:
                    self.ikSwitches[i] = switches
        self.keyedBones = len(self.tracks)
        self.frameCount = lastFrame + 1
        # the order MMD transforms bones in: before physics, then after; by layer, then index
        self.order = sorted(range(n), key=lambda i: (bones[i].afterPhysics, bones[i].layer, i))
        self.ikLinks = set()
        for b in bones:
            if b.ik is not None:
                for link in b.ik[3]:
                    if 0 <= link[0] < n:
                        self.ikLinks.add(link[0])
        appended = set(i for i, b in enumerate(bones) if b.appendRotate or b.appendTranslate)
        self.dynamic = sorted(set(self.tracks) | self.ikLinks | appended)

    def ikEnabled(self, i, frame):
        switches = self.ikSwitches.get(i)
        if not switches:
            return True
        enabled = switches[0][1]
        for f, e in switches:
            if f > frame:
                break
            enabled = e
        return enabled

    # transforms of the frame being solved

    def localRot(self, i):
        return qmul(qmul(self.ikRot.get(i, IDENTITY_Q), self.animRot[i]), self.appRot[i])

    def localPos(self, i):
        o, a, p = self.offsets[i], self.animPos[i], self.appPos[i]
        return (o[0] + a[0] + p[0], o[1] + a[1] + p[1], o[2] + a[2] + p[2])

    def world(self, i):
        g = self.cache.get(i)
        if g is None:
            r, t = self.localRot(i), self.localPos(i)
            p = self.parents[i]
            if p >= 0:
                pr, pt = self.world(p)
                pt2 = qrot(pr, t)
                g = (qmul(pr, r), (pt[0] + pt2[0], pt[1] + pt2[1], pt[2] + pt2[2]))
            else:
                g = (r, t)
            self.cache[i] = g
        return g

    def changed(self):
        self.cache = {}

    def solveAppend(self, i):
        b = self.bones[i]
        a = b.appendParent
        ab = self.bones[a]
        if b.appendRotate:
            if not b.appendLocal and (ab.appendRotate or ab.appendTranslate):
                rot = self.appRot[a]
            else:
                rot = self.animRot[a]
            if a in self.ikLinks:
                rot = qmul(self.ikRot.get(a, IDENTITY_Q), rot)
            self.appRot[i] = qslerp(IDENTITY_Q, rot, b.appendRatio)
        if b.appendTranslate:
            if not b.appendLocal and (ab.appendRotate or ab.appendTranslate):
                pos = self.appPos[a]
            else:
                pos = self.animPos[a]
            self.appPos[i] = (pos[0] * b.appendRatio, pos[1] * b.appendRatio, pos[2] * b.appendRatio)
        self.changed()

    def solveIK(self, i):
        target, loops, limit, links = self.bones[i].ik
        n = len(self.bones)
        if not 0 <= target < n:
            return
        links = [l for l in links if 0 <= l[0] < n]
        for l in links:
            self.ikRot[l[0]] = IDENTITY_Q
        self.changed()
        prev = [[0.0, 0.0, 0.0] for l in links]
        plane = [0.0] * len(links)
        best, saved = None, None
        for it in range(max(loops, 1)):
            self.solveIKStep(i, target, limit, links, it, prev, plane)
            tp = self.world(target)[1]
            ip = self.world(i)[1]
            dist = math.sqrt(sum((tp[c] - ip[c]) ** 2 for c in range(3)))
            if best is None or dist < best:
                best = dist
                saved = [self.ikRot[l[0]] for l in links]
            else:
                for l, r in zip(links, saved):
                    self.ikRot[l[0]] = r
                self.changed()
                break

    def linkVectors(self, link, ikBone, target):
        """Unit vectors from the link to the IK goal and to the effector, in the link's frame."""
        lr, lt = self.world(link)
        inv = qinv(lr)
        ip = self.world(ikBone)[1]
        tp = self.world(target)[1]
        iv = qrot(inv, (ip[0] - lt[0], ip[1] - lt[1], ip[2] - lt[2]))
        tv = qrot(inv, (tp[0] - lt[0], tp[1] - lt[1], tp[2] - lt[2]))
        il = math.sqrt(iv[0] * iv[0] + iv[1] * iv[1] + iv[2] * iv[2])
        tl = math.sqrt(tv[0] * tv[0] + tv[1] * tv[1] + tv[2] * tv[2])
        if il < 1e-9 or tl < 1e-9:
            return None, None
        return (iv[0] / il, iv[1] / il, iv[2] / il), (tv[0] / tl, tv[1] / tl, tv[2] / tl)

    def solveIKStep(self, ikBone, target, limit, links, it, prev, plane):
        for c, (link, mn, mx) in enumerate(links):
            if link == target:
                continue
            if mn is not None:
                hinge = None
                for a in range(3):
                    others = [o for o in range(3) if o != a]
                    if (mn[a] != 0.0 or mx[a] != 0.0) and all(mn[o] == 0.0 or mx[o] == 0.0 for o in others):
                        hinge = a
                        break
                if hinge is not None:
                    self.solvePlane(ikBone, target, limit, link, mn, mx, hinge, it, plane, c)
                    continue
            iv, tv = self.linkVectors(link, ikBone, target)
            if iv is None:
                continue
            d = max(-1.0, min(1.0, iv[0] * tv[0] + iv[1] * tv[1] + iv[2] * tv[2]))
            angle = math.acos(d)
            if math.degrees(angle) < 1e-3:
                continue
            angle = max(-limit, min(limit, angle))
            axis = (tv[1] * iv[2] - tv[2] * iv[1], tv[2] * iv[0] - tv[0] * iv[2], tv[0] * iv[1] - tv[1] * iv[0])
            al = math.sqrt(axis[0] * axis[0] + axis[1] * axis[1] + axis[2] * axis[2])
            if al < 1e-9:
                continue
            axis = (axis[0] / al, axis[1] / al, axis[2] / al)
            anim = self.animRot[link]
            chainRot = qmul(qmul(self.ikRot.get(link, IDENTITY_Q), anim), qaxis(axis, angle))
            if mn is not None:
                e = eulerxyz(chainRot, prev[c])
                e = [max(mn[a], min(mx[a], e[a])) for a in range(3)]
                e = [max(-limit, min(limit, e[a] - prev[c][a])) + prev[c][a] for a in range(3)]
                prev[c] = e
                chainRot = qeulerxyz(e)
            self.ikRot[link] = qmul(chainRot, qinv(anim))
            self.changed()

    def solvePlane(self, ikBone, target, limit, link, mn, mx, a, it, plane, c):
        iv, tv = self.linkVectors(link, ikBone, target)
        if iv is None:
            return
        d = max(-1.0, min(1.0, iv[0] * tv[0] + iv[1] * tv[1] + iv[2] * tv[2]))
        angle = max(-limit, min(limit, math.acos(d)))
        t1 = qrot(qaxis(AXES[a], angle), tv)
        t2 = qrot(qaxis(AXES[a], -angle), tv)
        d1 = t1[0] * iv[0] + t1[1] * iv[1] + t1[2] * iv[2]
        d2 = t2[0] * iv[0] + t2[1] * iv[1] + t2[2] * iv[2]
        newAngle = plane[c] + (angle if d1 > d2 else -angle)
        if it == 0 and (newAngle < mn[a] or newAngle > mx[a]):
            if mn[a] < -newAngle < mx[a]:
                newAngle = -newAngle
            else:
                half = (mn[a] + mx[a]) * 0.5
                if abs(half - newAngle) > abs(half + newAngle):
                    newAngle = -newAngle
        newAngle = max(mn[a], min(mx[a], newAngle))
        plane[c] = newAngle
        self.ikRot[link] = qmul(qaxis(AXES[a], newAngle), qinv(self.animRot[link]))
        self.changed()

    def bake(self, name, noeBones):
        n = len(self.bones)
        if not self.tracks:
            return None
        zero = (0.0, 0.0, 0.0)
        rots = dict((i, []) for i in self.dynamic)
        poss = dict((i, []) for i in self.dynamic)
        for frame in range(self.frameCount):
            self.animRot = [IDENTITY_Q] * n
            self.animPos = [zero] * n
            for i, track in self.tracks.items():
                self.animPos[i], self.animRot[i] = track.at(frame)
            self.appRot = [IDENTITY_Q] * n
            self.appPos = [zero] * n
            self.ikRot = {}
            self.changed()
            for i in self.order:
                b = self.bones[i]
                if b.appendRotate or b.appendTranslate:
                    self.solveAppend(i)
                if b.ik is not None and self.ikEnabled(i, frame):
                    self.solveIK(i)
            for i in self.dynamic:
                rots[i].append(self.localRot(i))
                poss[i].append(self.localPos(i))
        kfBones = []
        last = self.frameCount - 1
        for i in self.dynamic:
            kb = NoeKeyFramedBone(i)
            # to the model's space (Z negated: a mirror, so the rotation is (-x, -y, z, w)), then
            # Noesis' keyframe quaternion, the conjugate of the textbook one: (x, y, -z, w)
            rot = [NoeKeyFramedValue(f / VMD_FPS, NoeQuat((q[0], q[1], -q[2], q[3])))
                   for f, q in keptKeys(rots[i], last)]
            pos = [NoeKeyFramedValue(f / VMD_FPS, NoeVec3((p[0], p[1], -p[2])))
                   for f, p in keptKeys(poss[i], last)]
            kb.setRotation(rot, noesis.NOEKF_ROTATION_QUATERNION_4, noesis.NOEKF_INTERPOLATE_LINEAR)
            kb.setTranslation(pos, noesis.NOEKF_TRANSLATION_VECTOR_3, noesis.NOEKF_INTERPOLATE_LINEAR)
            kfBones.append(kb)
        # frame f at f / 30 s; ROUNDUP + PLUSONE make Noesis count frames 0..last
        return NoeKeyFramedAnim(name, noeBones, kfBones, VMD_FPS, noesis.KFANIMFLAG_PLUSONE | noesis.KFANIMFLAG_ROUNDUP)


def keptKeys(values, last):
    """(frame, value) of the baked frames, without the middle ones of runs of equal values."""
    out = []
    for f, v in enumerate(values):
        if f == 0 or f == last or v != values[f - 1] or v != values[f + 1]:
            out.append((f, v))
    return out
