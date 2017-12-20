from RapiModel import RapiModel
from RapiContext import RapiContext
from FaceBuffer import FaceBuffer
from ImageDecodePVRTC import ImageDecodePVRTC
import os
import struct
import itertools
import sys
from util import logNotImplementedMethod, last

# state

this = sys.modules[__name__]
this.contexts = []
this.lastCheckedName = None

INTEGER_TYPES = {
    1: 'B',
    2: 'H',
    4: 'I',
}

FLOAT_TYPES = {
    4: 'f',
    8: 'd',
}

def rpgCreateContext():
    context = RapiContext()
    this.contexts.append(context)
    return context

def rpgConstructModel():
    model = RapiModel()
    currentContext().models.append(model)
    return model

def rpgConstructModelSlim():
    return rpgConstructModel()

def rpgBindPositionBufferOfs(buff, typeSize, structSize, structOffset):
    splitted = splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
    fmt = str(3) + FLOAT_TYPES[typeSize]
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    currentContext().vertexBuffers.append(mapped)

def rpgBindNormalBufferOfs(buff, typeSize, structSize, structOffset):
    splitted = splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
    fmt = str(3) + FLOAT_TYPES[typeSize]
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    currentContext().normalBuffers.append(mapped)

def rpgBindUV1BufferOfs(buff, typeSize, structSize, structOffset):
    splitted = splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * 2], splitted)
    fmt = str(2) + FLOAT_TYPES[typeSize]
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    currentContext().uvBuffers.append(mapped)

def rpgSetMaterial(material):
    currentContext().materials.append(material)

def rpgCommitTriangles(buff, typeSize, numIdx, shape, usePlotMap):
    fmt = str(numIdx) + INTEGER_TYPES[typeSize]
    unpacked = struct.unpack(fmt, buff)
    faceBuffer = FaceBuffer(unpacked, typeSize, numIdx, shape, usePlotMap, currentContext().currentMaterial())
    currentContext().faceBuffers.append(faceBuffer)
    currentContext().commit()

def imageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags = 0):
    return ImageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags).call()

def imageFlipRGBA32(r, width, height, unk0, unk1):
    logNotImplementedMethod('imageFlipRGBA32', locals())

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
    handle = open(path, "rb")
    data = handle.read()
    handle.close()
    return data

def rpgClearBufferBinds():
    logNotImplementedMethod('rpgClearBufferBinds', locals())

def setPreviewOption(key, value):
    logNotImplementedMethod('setPreviewOption', locals())

def rpgSetName(name):
    currentContext().names.append(name)

def rpgSetUVScaleBias(vec1, vec2):
    currentContext().uvScaleBiases.append({ "vec1": vec1, "vec2": vec2 })

def imageDecodeDXT(data, width, height, format):
    logNotImplementedMethod('imageDecodeDXT', locals())

def rpgBindColorBufferOfs(buff, typeSize, structSize, structOffset, count):
    splitted = splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * count], splitted)
    fmt = str(count) + FLOAT_TYPES[typeSize]
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    currentContext().colorBuffers.append(mapped)

def rpgBindBoneWeightBufferOfs(buff, typeSize, structSize, structOffset, count):
    splitted = splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * count], splitted)
    fmt = str(count) + FLOAT_TYPES[typeSize]
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    currentContext().boneWeightBuffers.append(mapped)

def rpgBindBoneIndexBufferOfs(buff, typeSize, structSize, structOffset, count):
    splitted = splitBuffer(buff, structSize)
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * count], splitted)
    fmt = str(count) + INTEGER_TYPES[typeSize]
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    currentContext().boneIndexBuffers.append(mapped)

def checkFileExists(path):
    logNotImplementedMethod('checkFileExists', locals())

def callExtensionMethod(method, *args):
    logNotImplementedMethod('callExtensionMethod', locals())

def createPCMWaveHeader(size, bitrate, samplerate, channelcount):
    logNotImplementedMethod('createPCMWaveHeader', locals())

def createProceduralAnim(bones, animations, numFrames):
    logNotImplementedMethod('createProceduralAnim', locals())

def dataToIntList(data, size, rpgeodataType, endianess):
    logNotImplementedMethod('dataToIntList', locals())

def decodeADPCMBlock(data, bitsPerSample, numSamplesToDecode, lshift, filter, filterTable0, filterTable1, listOf2PreviousSamples, bitOffset, bitStride, sampleScale):
    logNotImplementedMethod('decodeADPCMBlock', locals())

def decodeNormals32(normals, stride, xBits, yBits, zBits, endianness):
    logNotImplementedMethod('decodeNormals32', locals())

def decompInflate(sourceBytes, destinationSize, windowSize = 0):
    logNotImplementedMethod('decompInflate', locals())

def decompLZHMelt(data, size):
    logNotImplementedMethod('decompLZHMelt', locals())

def decompPRS(data, size):
    logNotImplementedMethod('decompPRS', locals())

def decryptAES(data, key):
    logNotImplementedMethod('decryptAES', locals())

def exportArchiveFile(filename, data):
    logNotImplementedMethod('exportArchiveFile', locals())

def getDeferredAnims():
    logNotImplementedMethod('getDeferredAnims', locals())

def getInputName():
    logNotImplementedMethod('getInputName', locals())

def getOutputName():
    logNotImplementedMethod('getOutputName', locals())

def immBegin(shape):
    logNotImplementedMethod('immBegin', locals())

def immBoneIndex(boneIndex):
    logNotImplementedMethod('immBoneIndex', locals())

def immBoneWeight(boneWeight):
    logNotImplementedMethod('immBoneWeight', locals())

def immColor4(color):
    logNotImplementedMethod('immColor4', locals())

def immEnd():
    logNotImplementedMethod('immEnd', locals())

def immLMUV2(lmuv):
    logNotImplementedMethod('immLMUV2', locals())

def immNormal3(normal):
    logNotImplementedMethod('immNormal3', locals())

def immUV2(uv):
    logNotImplementedMethod('immUV2', locals())

def immVertex3(vertex):
    logNotImplementedMethod('immVertex3', locals())

def immVertex3f(positions, offset = 0):
    logNotImplementedMethod('immVertex3f', locals())

def isGeometryTarget():
    logNotImplementedMethod('isGeometryTarget', locals())

def imageApplyPalette(data, width, height, palette, numberOfPaletteEntries):
    logNotImplementedMethod('imageApplyPalette', locals())

def imageBlit32(destinationData, destinationWidth, destinationHeight, destinationXOffset, destinationYOffset, sourceData, sourceEidth, sourceHeight, sourceXOoffset, sourceYOffset, destStride = 0, sourceStride = 0):
    logNotImplementedMethod('imageBlit32', locals())

def rpgCreatePlaneSpaceUVs():
    logNotImplementedMethod('rpgCreatePlaneSpaceUVs', locals())

def rpgFlatNormals():
    logNotImplementedMethod('rpgFlatNormals', locals())

def rpgGetVertexCount():
    logNotImplementedMethod('rpgGetVertexCount', locals())

def rpgOptimize():
    logNotImplementedMethod('rpgOptimize', locals())

def rpgReset():
    logNotImplementedMethod('rpgReset', locals())

def rpgSetLightmap(name):
    currentContext().lightMaps.append(name)

def rpgSetBoneMap(boneMap):
    currentContext().boneMaps.append(boneMap)

def setPreviewOption(key, value):
    logNotImplementedMethod('setPreviewOption', locals())

def rpgSetOption(key, value):
    logNotImplementedMethod('rpgSetOption', locals())

# private

def currentContext():
    return last(this.contexts)

def splitBuffer(buff, structSize):
    return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]
