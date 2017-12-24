from RapiModel import RapiModel
from RapiContext import RapiContext
from FaceBuffer import FaceBuffer
import os
import struct
import itertools
import sys
from util import logNotImplementedMethod, last, halfFloatsToFloats
from pvr import pvr_decode

# state

this = sys.modules[__name__]
this.contexts = []
this.lastCheckedName = None
this.options = {}

UNPACK_TYPES = {
    'RPGEODATA_BYTE': 'b',
    'RPGEODATA_FLOAT': 'f',
    'RPGEODATA_HALFFLOAT': 'H', # need to convert half float to float
    'RPGEODATA_INT': 'i',
    'RPGEODATA_SHORT': 'h',
    'RPGEODATA_UBYTE': 'B',
    'RPGEODATA_UINT': 'I',
    'RPGEODATA_USHORT': 'H',
    'RPGEODATA_DOUBLE': 'd',
}

UNPACK_SIZES = {
    'RPGEODATA_BYTE': 1,
    'RPGEODATA_FLOAT': 4,
    'RPGEODATA_HALFFLOAT': 2,
    'RPGEODATA_INT': 4,
    'RPGEODATA_SHORT': 2,
    'RPGEODATA_UBYTE': 1,
    'RPGEODATA_UINT': 4,
    'RPGEODATA_USHORT': 2,
    'RPGEODATA_DOUBLE': 8,
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

def rpgBindPositionBufferOfs(buff, type, structSize, structOffset):
    unpackedBuffer = unpackBuffer(buff, type, structSize, structOffset, 3)
    currentContext().vertexBuffers.append(unpackedBuffer)

def rpgBindNormalBufferOfs(buff, type, structSize, structOffset):
    unpackedBuffer = unpackBuffer(buff, type, structSize, structOffset, 3)
    currentContext().normalBuffers.append(unpackedBuffer)

def rpgBindUV1BufferOfs(buff, type, structSize, structOffset):
    unpackedBuffer = unpackBuffer(buff, type, structSize, structOffset, 2)
    currentContext().uvBuffers.append(unpackedBuffer)

def rpgBindUV2BufferOfs(buff, type, structSize, structOffset):
    unpackedBuffer = unpackBuffer(buff, type, structSize, structOffset, 2)
    currentContext().uvBuffers.append(unpackedBuffer)

def rpgBindColorBufferOfs(buff, type, structSize, structOffset, count):
    unpackedBuffer = unpackBuffer(buff, type, structSize, structOffset, count)
    currentContext().colorBuffers.append(unpackedBuffer)

def rpgBindBoneWeightBufferOfs(buff, type, structSize, structOffset, count):
    unpackedBuffer = unpackBuffer(buff, type, structSize, structOffset, count)
    currentContext().boneWeightBuffers.append(unpackedBuffer)

def rpgBindBoneIndexBufferOfs(buff, type, structSize, structOffset, count):
    unpackedBuffer = unpackBuffer(buff, type, structSize, structOffset, count)
    currentContext().boneIndexBuffers.append(unpackedBuffer)

def rpgCommitTriangles(buff, type, numIdx, shape, usePlotMap):
    fmt = str(numIdx) + UNPACK_TYPES[type]
    unpacked = struct.unpack(fmt, buff)
    faceBuffer = FaceBuffer(unpacked, type, numIdx, shape, usePlotMap, currentContext().currentMaterial())
    currentContext().faceBuffers.append(faceBuffer)
    currentContext().commit()

def rpgSetMaterial(material):
    currentContext().materials.append(material)

# TODO: not working fully yet
def imageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags = 0):
    return pvr_decode(data, width, height, bitsPerPixel)

def imageFlipRGBA32(r, width, height, unk0, unk1):
    logNotImplementedMethod('imageFlipRGBA32', locals())

def getExtensionlessName(path):
    return os.path.splitext(path)[0]

def getLocalFileName(path):
    return os.path.basename(path)

def getLastCheckedName():
    return this.lastCheckedName

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

def checkFileExists(path):
    return os.path.isfile(path)

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
    options[key] = value
    logNotImplementedMethod('rpgSetOption', locals())

# unofficial method
def setLastCheckedName(name):
    this.lastCheckedName = name

# private

def currentContext():
    return last(this.contexts)

def splitBuffer(buff, structSize):
    return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]

def unpackBuffer(buff, type, structSize, structOffset, count):
    splitted = splitBuffer(buff, structSize)
    typeSize = UNPACK_SIZES[type]
    mapped = map(lambda x: x[structOffset:structOffset + typeSize * count], splitted)
    fmt = str(count) + UNPACK_TYPES[type]
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    mapped = fixHalfFloats(mapped, type)
    return mapped

# half float needs to mapped to normal float in python
def fixHalfFloats(values, type):
    if not type == 'RPGEODATA_HALFFLOAT':
        return values

    return map(lambda x: halfFloatsToFloats(x), values)
