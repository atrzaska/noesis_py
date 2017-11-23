from Rpg import Rpg
from ImageDecodePVRTC import ImageDecodePVRTC

rpg = Rpg()

def rpgCreateContext():
    return rpg.rpgCreateContext()

def rpgConstructModel():
    return rpg.rpgConstructModel()

def rpgBindPositionBufferOfs(buff, typeSize, structSize, structOffset):
    return rpg.rpgBindPositionBufferOfs(buff, typeSize, structSize, structOffset)

def rpgBindNormalBufferOfs(buff, typeSize, structSize, structOffset):
    return rpg.rpgBindNormalBufferOfs(buff, typeSize, structSize, structOffset)

def rpgBindUV1BufferOfs(buff, typeSize, structSize, structOffset):
    return rpg.rpgBindUV1BufferOfs(buff, typeSize, structSize, structOffset)

def rpgSetMaterial(matName):
    return rpg.rpgSetMaterial(matName)

def rpgCommitTriangles(buff, type, numIdx, shape, unk1):
    return rpg.rpgCommitTriangles(buff, type, numIdx, shape, unk1)

def imageDecodePVRTC(buff, width, height, bpp):
    return ImageDecodePVRTC(buff, width, height, bpp).call()

def imageFlipRGBA32(r, width, height, unk0, unk1):
    # TODO: implement me
    return r

def getExtensionlessName(arg):
    # TODO: needed for dreamy theater
    pass

def getLocalFileName(arg):
    # TODO: needed for dreamy theater
    pass

def getLastCheckedName():
    # TODO: needed for dreamy theater
    pass

def getDirForFilePath(path):
    # TODO: needed for dreamy theater
    pass

def loadIntoByteArray(path):
    # TODO: needed for dreamy theater
    pass

def rpgClearBufferBinds():
    # TODO: needed for dreamy theater
    pass

def setPreviewOption(key, value):
    # TODO: needed for dreamy theater
    pass

def rpgSetName(name):
    # TODO: needed for dreamy theater
    pass

def rpgSetUVScaleBias(vec1, vec_2):
    # TODO: needed for dreamy theater
    pass

def rpgSetBoneMap(boneMap):
    # TODO: needed for dreamy theater
    pass

def imageDecodeDXT(buff, width, height, type):
    # TODO: needed for dreamy theater
    pass

def rpgBindColorBufferOfs(buff, typeSize, structSize, structOffset, unk_4):
    # TODO: needed for dreamy theater
    pass

def rpgBindBoneWeightBufferOfs(buff, typeSize, structSize, structOffset, unk_4):
    # TODO: needed for dreamy theater
    pass

def rpgBindBoneIndexBufferOfs(boneBuff, typeSize, structSize, structOffset, unk_4):
    # TODO: needed for dreamy theater
    pass
