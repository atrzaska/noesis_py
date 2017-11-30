from RapiModel import RapiModel
from RapiContext import RapiContext
from FaceInfo import FaceInfo
from ImageDecodePVRTC import ImageDecodePVRTC
import os
import struct
import itertools
import sys
import logger

# state

this = sys.modules[__name__]
this.contexts = []
this.lastCheckedName = None

def rpgCreateContext():
    context = RapiContext()
    this.contexts.append(context)
    return context

def rpgConstructModel():
    model = RapiModel()
    __currentContext().models.append(model)
    return model

def rpgConstructModelSlim():
    return rpg.rpgConstructModel()

def rpgBindPositionBufferOfs(buff, typeSize, structSize, structOffset):
    splitted = __splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
    mapped = map(lambda x: struct.unpack('3f', x), mapped) # TODO: make format dynamic
    __currentContext().vertexBuffers.append(mapped)

def rpgBindNormalBufferOfs(buff, typeSize, structSize, structOffset):
    splitted = __splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
    mapped = map(lambda x: struct.unpack('3f', x), mapped) # TODO: make format dynamic
    __currentContext().normalBuffers.append(mapped)

def rpgBindUV1BufferOfs(buff, typeSize, structSize, structOffset):
    splitted = __splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * 2], splitted)
    mapped = map(lambda x: struct.unpack('2f', x), mapped) # TODO: make format dynamic
    __currentContext().uvBuffers.append(mapped)

def rpgSetMaterial(material):
    __currentContext().currentMaterial = material

def rpgCommitTriangles(buff, typeSize, numIdx, shape, usePlotMap):
    fmt = "{numIdx}H".format(**locals()) # TODO: make format dynamic
    unpacked = struct.unpack(fmt, buff)

    faceBuffer = FaceInfo(unpacked, typeSize, numIdx, shape, usePlotMap, __currentContext().currentMaterial)
    __currentContext().faceBuffers.append(faceBuffer)

def imageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags = 0):
    return ImageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags).call()

def imageFlipRGBA32(r, width, height, unk0, unk1):
    logger.logNotImplementedMethod('imageFlipRGBA32', locals())

def getExtensionlessName(path):
    return os.path.splitext(path)[0]

def getLocalFileName(path):
    return os.path.basename(path)

def getLastCheckedName():
    return this.lastCheckedName

# unofficial method
def setLastCheckedName(name):
    this.lastCheckedName = name

def getDirForFilePath(path):
    return os.path.dirname(os.path.abspath(path)) + "/"

def loadIntoByteArray(path):
    return open(path, "rb").read()

def rpgClearBufferBinds():
    logger.logNotImplementedMethod('rpgClearBufferBinds', locals())

def setPreviewOption(key, value):
    logger.logNotImplementedMethod('setPreviewOption', locals())

def rpgSetName(name):
    logger.logNotImplementedMethod('rpgSetName', locals())

def rpgSetUVScaleBias(vec1, vec_2):
    logger.logNotImplementedMethod('rpgSetUVScaleBias', locals())

def rpgSetBoneMap(boneMap):
    logger.logNotImplementedMethod('rpgSetBoneMap', locals())

def imageDecodeDXT(data, width, height, format):
    logger.logNotImplementedMethod('imageDecodeDXT', locals())

def rpgBindColorBufferOfs(buff, typeSize, structSize, structOffset, unk_4):
    logger.logNotImplementedMethod('rpgBindColorBufferOfs', locals())

def rpgBindBoneWeightBufferOfs(buff, typeSize, structSize, structOffset, unk_4):
    logger.logNotImplementedMethod('rpgBindBoneWeightBufferOfs', locals())

def rpgBindBoneIndexBufferOfs(boneBuff, typeSize, structSize, structOffset, unk_4):
    logger.logNotImplementedMethod('rpgBindBoneIndexBufferOfs', locals())

def checkFileExists(path):
    logger.logNotImplementedMethod('checkFileExists', locals())

def callExtensionMethod(method, *args):
    logger.logNotImplementedMethod('callExtensionMethod', locals())

def createPCMWaveHeader(size, bitrate, samplerate, channelcount):
    logger.logNotImplementedMethod('createPCMWaveHeader', locals())

def createProceduralAnim(bones, animations, numFrames):
    logger.logNotImplementedMethod('createProceduralAnim', locals())

def dataToIntList(data, size, rpgeodataType, endianess):
    logger.logNotImplementedMethod('dataToIntList', locals())

def decodeADPCMBlock(data, bitsPerSample, numSamplesToDecode, lshift, filter, filterTable0, filterTable1, listOf2PreviousSamples, bitOffset, bitStride, sampleScale):
    logger.logNotImplementedMethod('decodeADPCMBlock', locals())

def decodeNormals32(normals, stride, xBits, yBits, zBits, endianness):
    logger.logNotImplementedMethod('decodeNormals32', locals())

def decompInflate(sourceBytes, destinationSize, windowSize = 0):
    logger.logNotImplementedMethod('decompInflate', locals())

def decompLZHMelt(data, size):
    logger.logNotImplementedMethod('decompLZHMelt', locals())

def decompPRS(data, size):
    logger.logNotImplementedMethod('decompPRS', locals())

def decryptAES(data, key):
    logger.logNotImplementedMethod('decryptAES', locals())

def exportArchiveFile(filename, data):
    logger.logNotImplementedMethod('exportArchiveFile', locals())

def getDeferredAnims():
    logger.logNotImplementedMethod('getDeferredAnims', locals())

def getInputName():
    logger.logNotImplementedMethod('getInputName', locals())

def getOutputName():
    logger.logNotImplementedMethod('getOutputName', locals())

def immBegin(shape):
    logger.logNotImplementedMethod('immBegin', locals())

def immBoneIndex(boneIndex):
    logger.logNotImplementedMethod('immBoneIndex', locals())

def immBoneWeight(boneWeight):
    logger.logNotImplementedMethod('immBoneWeight', locals())

def immColor4(color):
    logger.logNotImplementedMethod('immColor4', locals())

def immEnd():
    logger.logNotImplementedMethod('immEnd', locals())

def immLMUV2(lmuv):
    logger.logNotImplementedMethod('immLMUV2', locals())

def immNormal3(normal):
    logger.logNotImplementedMethod('immNormal3', locals())

def immUV2(uv):
    logger.logNotImplementedMethod('immUV2', locals())

def immVertex3(vertex):
    logger.logNotImplementedMethod('immVertex3', locals())

def immVertex3f(positions, offset = 0):
    logger.logNotImplementedMethod('immVertex3f', locals())

def isGeometryTarget():
    logger.logNotImplementedMethod('isGeometryTarget', locals())

def imageApplyPalette(data, width, height, palette, numberOfPaletteEntries):
    logger.logNotImplementedMethod('imageApplyPalette', locals())

def imageBlit32(destinationData, destinationWidth, destinationHeight, destinationXOffset, destinationYOffset, sourceData, sourceEidth, sourceHeight, sourceXOoffset, sourceYOffset, destStride = 0, sourceStride = 0):
    logger.logNotImplementedMethod('imageBlit32', locals())

def rpgCreatePlaneSpaceUVs():
    logger.logNotImplementedMethod('rpgCreatePlaneSpaceUVs', locals())

def rpgFlatNormals():
    logger.logNotImplementedMethod('rpgFlatNormals', locals())

def rpgGetVertexCount():
    logger.logNotImplementedMethod('rpgGetVertexCount', locals())

def rpgOptimize():
    logger.logNotImplementedMethod('rpgOptimize', locals())

def rpgReset():
    logger.logNotImplementedMethod('rpgReset', locals())

def rpgSetLightmap(name):
    logger.logNotImplementedMethod('rpgSetLightmap', locals())

def rpgSetBoneMap(boneMap):
    logger.logNotImplementedMethod('rpgSetBoneMap', locals())

def setPreviewOption(key, value):
    logger.logNotImplementedMethod('setPreviewOption', locals())

def rpgSetOption(key, value):
    logger.logNotImplementedMethod('rpgSetOption', locals())

# private

def __currentContext():
    return this.contexts[-1]

def __splitBuffer(buff, structSize):
    return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]
