from Rpg import Rpg
from ImageDecodePVRTC import ImageDecodePVRTC
import os

rpg = Rpg()

def rpgCreateContext():
    return rpg.rpgCreateContext()

def rpgConstructModel():
    return rpg.rpgConstructModel()

def rpgConstructModelSlim():
    return rpg.rpgConstructModel()

def rpgBindPositionBufferOfs(buff, typeSize, structSize, structOffset):
    return rpg.rpgBindPositionBufferOfs(buff, typeSize, structSize, structOffset)

def rpgBindNormalBufferOfs(buff, typeSize, structSize, structOffset):
    return rpg.rpgBindNormalBufferOfs(buff, typeSize, structSize, structOffset)

def rpgBindUV1BufferOfs(buff, typeSize, structSize, structOffset):
    return rpg.rpgBindUV1BufferOfs(buff, typeSize, structSize, structOffset)

def rpgSetMaterial(name):
    return rpg.rpgSetMaterial(name)

def rpgCommitTriangles(buff, dataType, numIdx, shape, usePlotMap):
    return rpg.rpgCommitTriangles(buff, dataType, numIdx, shape, usePlotMap)

def imageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags = 0):
    return ImageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags).call()

def imageFlipRGBA32(r, width, height, unk0, unk1):
    # TODO: implement me
    return r

def getExtensionlessName(path):
    return os.path.splitext(path)[0]

def getLocalFileName(path):
    return os.path.abspath(path)

def getLastCheckedName():
    return rpg.getLastCheckedName()

def setLastCheckedName(name):
    return rpg.setLastCheckedName(name)

def getDirForFilePath(path):
    return os.path.dirname(os.path.abspath(path))

def loadIntoByteArray(path):
    return open(path, "rb")

def rpgClearBufferBinds():
    # TODO: needed for dreamy theater
    pass

def setPreviewOption(key, value):
    # TODO: needed for dreamy theater
    pass

# unofficial API
def rpgSetName(name):
    # TODO: needed for dreamy theater
    pass

def rpgSetUVScaleBias(vec1, vec_2):
    # TODO: needed for dreamy theater
    pass

def rpgSetBoneMap(boneMap):
    # TODO: needed for dreamy theater
    pass

def imageDecodeDXT(data, width, height, format):
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

def checkFileExists(path):
    # TODO: implement me
    pass

def callExtensionMethod(method, *args):
    # TODO: implement me
    pass

def createPCMWaveHeader(size, bitrate, samplerate, channelcount):
    # TODO: implement me
    pass

def createProceduralAnim(bones, animations, numFrames):
    # TODO: implement me
    pass

def dataToIntList(data, size, rpgeodataType, endianess):
    # TODO: implement me
    pass

def decodeADPCMBlock(data, bitsPerSample, numSamplesToDecode, lshift, filter, filterTable0, filterTable1, listOf2PreviousSamples, bitOffset, bitStride, sampleScale):
    # TODO: implement me
    pass

def decodeNormals32(normals, stride, xBits, yBits, zBits, endianness):
    # TODO: implement me
    pass

def decompInflate(sourceBytes, destinationSize, windowSize = 0):
    # TODO: implement me
    pass

def decompLZHMelt(data, size):
    # TODO: implement me
    pass

def decompPRS(data, size):
    # TODO: implement me
    pass

def decryptAES(data, key):
    # TODO: implement me
    pass

def exportArchiveFile(filename, data):
    # TODO: implement me
    pass

def getDeferredAnims():
    # TODO: implement me
    pass

def getInputName():
    # TODO: implement me
    pass

def getOutputName():
    # TODO: implement me
    pass

def immBegin(shape):
    # TODO: implement me
    pass

def immBoneIndex(boneIndex):
    # TODO: implement me
    pass

def immBoneWeight(boneWeight):
    # TODO: implement me
    pass

def immColor4(color):
    # TODO: implement me
    pass

def immEnd():
    # TODO: implement me
    pass

def immLMUV2(lmuv):
    # TODO: implement me
    pass

def immNormal3(normal):
    # TODO: implement me
    pass

def immUV2(uv):
    # TODO: implement me
    pass

def immVertex3(vertex):
    # TODO: implement me
    pass

def immVertex3f(positions, offset = 0):
    # TODO: implement me
    pass

def isGeometryTarget():
    # TODO: implement me
    pass

def imageApplyPalette(data, width, height, palette, numberOfPaletteEntries):
    # TODO: implement me
    pass

def imageBlit32(destinationData, destinationWidth, destinationHeight, destinationXOffset, destinationYOffset, sourceData, sourceEidth, sourceHeight, sourceXOoffset, sourceYOffset, destStride = 0, sourceStride = 0):
    # TODO: implement me
    pass

def rpgCreatePlaneSpaceUVs():
    # TODO: implement me
    pass

def rpgFlatNormals():
    # TODO: implement me
    pass

def rpgGetVertexCount():
    # TODO: implement me
    pass

def rpgOptimize():
    # TODO: implement me
    pass

def rpgReset():
    # TODO: implement me
    pass

def rpgSetLightmap(name):
    # TODO: implement me
    pass

def rpgSetBoneMap(boneMap):
    # TODO: implement me
    pass

def setPreviewOption(key, value):
    # TODO: implement me
    pass

def rpgSetOption(key, value):
    # TODO: implement me
    pass
