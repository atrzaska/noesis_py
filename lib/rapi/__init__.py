from Rpg import Rpg

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

# TODO: remove this non official api
def rpgLog():
    return rpg.rpgLog()

def imageDecodePVRTC(buff, width, height, bpp):
    # TODO: implement me
    pass

def imageFlipRGBA32(r, width, height, unk0, unk1):
    # TODO: implement me
    pass
