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
