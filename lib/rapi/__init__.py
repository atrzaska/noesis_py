from RapiModel import RapiModel
from RapiContext import RapiContext
from FaceInfo import FaceInfo
from ImageDecodePVRTC import ImageDecodePVRTC
import os
import struct
import itertools
import sys

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
    # TODO: implement me
    print("Not implemented method called: imageFlipRGBA32")

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
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: rpgClearBufferBinds")

def setPreviewOption(key, value):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: setPreviewOption")

def rpgSetName(name):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: rpgSetName")

def rpgSetUVScaleBias(vec1, vec_2):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: rpgSetUVScaleBias")

def rpgSetBoneMap(boneMap):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: rpgSetBoneMap")

def imageDecodeDXT(data, width, height, format):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: imageDecodeDXT")

def rpgBindColorBufferOfs(buff, typeSize, structSize, structOffset, unk_4):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: rpgBindColorBufferOfs")

def rpgBindBoneWeightBufferOfs(buff, typeSize, structSize, structOffset, unk_4):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: rpgBindBoneWeightBufferOfs")

def rpgBindBoneIndexBufferOfs(boneBuff, typeSize, structSize, structOffset, unk_4):
    # TODO: implement me, needed for dreamy theater
    print("Not implemented method called: rpgBindBoneIndexBufferOfs")

def checkFileExists(path):
    # TODO: implement me
    print("Not implemented method called: checkFileExists")

def callExtensionMethod(method, *args):
    # TODO: implement me
    print("Not implemented method called: callExtensionMethod")

def createPCMWaveHeader(size, bitrate, samplerate, channelcount):
    # TODO: implement me
    print("Not implemented method called: createPCMWaveHeader")

def createProceduralAnim(bones, animations, numFrames):
    # TODO: implement me
    print("Not implemented method called: createProceduralAnim")

def dataToIntList(data, size, rpgeodataType, endianess):
    # TODO: implement me
    print("Not implemented method called: dataToIntList")

def decodeADPCMBlock(data, bitsPerSample, numSamplesToDecode, lshift, filter, filterTable0, filterTable1, listOf2PreviousSamples, bitOffset, bitStride, sampleScale):
    # TODO: implement me
    print("Not implemented method called: decodeADPCMBlock")

def decodeNormals32(normals, stride, xBits, yBits, zBits, endianness):
    # TODO: implement me
    print("Not implemented method called: decodeNormals32")

def decompInflate(sourceBytes, destinationSize, windowSize = 0):
    # TODO: implement me
    print("Not implemented method called: decompInflate")

def decompLZHMelt(data, size):
    # TODO: implement me
    print("Not implemented method called: decompLZHMelt")

def decompPRS(data, size):
    # TODO: implement me
    print("Not implemented method called: decompPRS")

def decryptAES(data, key):
    # TODO: implement me
    print("Not implemented method called: decryptAES")

def exportArchiveFile(filename, data):
    # TODO: implement me
    print("Not implemented method called: exportArchiveFile")

def getDeferredAnims():
    # TODO: implement me
    print("Not implemented method called: getDeferredAnims")

def getInputName():
    # TODO: implement me
    print("Not implemented method called: getInputName")

def getOutputName():
    # TODO: implement me
    print("Not implemented method called: getOutputName")

def immBegin(shape):
    # TODO: implement me
    print("Not implemented method called: immBegin")

def immBoneIndex(boneIndex):
    # TODO: implement me
    print("Not implemented method called: immBoneIndex")

def immBoneWeight(boneWeight):
    # TODO: implement me
    print("Not implemented method called: immBoneWeight")

def immColor4(color):
    # TODO: implement me
    print("Not implemented method called: immColor4")

def immEnd():
    # TODO: implement me
    print("Not implemented method called: immEnd")

def immLMUV2(lmuv):
    # TODO: implement me
    print("Not implemented method called: immLMUV2")

def immNormal3(normal):
    # TODO: implement me
    print("Not implemented method called: immNormal3")

def immUV2(uv):
    # TODO: implement me
    print("Not implemented method called: immUV2")

def immVertex3(vertex):
    # TODO: implement me
    print("Not implemented method called: immVertex3")

def immVertex3f(positions, offset = 0):
    # TODO: implement me
    print("Not implemented method called: immVertex3f")

def isGeometryTarget():
    # TODO: implement me
    print("Not implemented method called: isGeometryTarget")

def imageApplyPalette(data, width, height, palette, numberOfPaletteEntries):
    # TODO: implement me
    print("Not implemented method called: imageApplyPalette")

def imageBlit32(destinationData, destinationWidth, destinationHeight, destinationXOffset, destinationYOffset, sourceData, sourceEidth, sourceHeight, sourceXOoffset, sourceYOffset, destStride = 0, sourceStride = 0):
    # TODO: implement me
    print("Not implemented method called: imageBlit32")

def rpgCreatePlaneSpaceUVs():
    # TODO: implement me
    print("Not implemented method called: rpgCreatePlaneSpaceUVs")

def rpgFlatNormals():
    # TODO: implement me
    print("Not implemented method called: rpgFlatNormals")

def rpgGetVertexCount():
    # TODO: implement me
    print("Not implemented method called: rpgGetVertexCount")

def rpgOptimize():
    # TODO: implement me
    print("Not implemented method called: rpgOptimize")

def rpgReset():
    # TODO: implement me
    print("Not implemented method called: rpgReset")

def rpgSetLightmap(name):
    # TODO: implement me
    print("Not implemented method called: rpgSetLightmap")

def rpgSetBoneMap(boneMap):
    # TODO: implement me
    print("Not implemented method called: rpgSetBoneMap")

def setPreviewOption(key, value):
    # TODO: implement me
    print("Not implemented method called: setPreviewOption")

def rpgSetOption(key, value):
    # TODO: implement me
    print("Not implemented method called: rpgSetOption")

# private

def __currentContext():
    return this.contexts[-1]

def __splitBuffer(buff, structSize):
    return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]
