import os
import struct
import itertools
import sys
import pvr
import noesis
import inc_noesis
from Context import Context
from util import logNotImplementedMethod

# state

this = sys.modules[__name__]
this.context = None
this.lastCheckedName = None

UNPACK_TYPES = {
    noesis.RPGEODATA_BYTE: 'b',
    noesis.RPGEODATA_FLOAT: 'f',
    noesis.RPGEODATA_HALFFLOAT: 'H', # half float is converted to float
    noesis.RPGEODATA_INT: 'i',
    noesis.RPGEODATA_SHORT: 'h',
    noesis.RPGEODATA_UBYTE: 'B',
    noesis.RPGEODATA_UINT: 'I',
    noesis.RPGEODATA_USHORT: 'H',
    noesis.RPGEODATA_DOUBLE: 'd',
}

UNPACK_SIZES = {
    noesis.RPGEODATA_BYTE: 1,
    noesis.RPGEODATA_FLOAT: 4,
    noesis.RPGEODATA_HALFFLOAT: 2,
    noesis.RPGEODATA_INT: 4,
    noesis.RPGEODATA_SHORT: 2,
    noesis.RPGEODATA_UBYTE: 1,
    noesis.RPGEODATA_UINT: 4,
    noesis.RPGEODATA_USHORT: 2,
    noesis.RPGEODATA_DOUBLE: 8,
}

def callExtensionMethod(method, *args):
    logNotImplementedMethod('callExtensionMethod', locals())

def checkFileExists(path):
    return os.path.isfile(path)

def checkFileExt(*args):
    logNotImplementedMethod('checkFileExt', locals())

def compressDeflate(*args):
    logNotImplementedMethod('compressDeflate', locals())

def createBoneMap(*args):
    logNotImplementedMethod('createBoneMap', locals())

def createPCMWaveHeader(size, bitrate, samplerate, channelcount):
    logNotImplementedMethod('createPCMWaveHeader', locals())

def createProceduralAnim(bones, animations, numFrames):
    logNotImplementedMethod('createProceduralAnim', locals())

def createTriStrip(*args):
    logNotImplementedMethod('createTriStrip', locals())

def dataToFloatList(*args):
    logNotImplementedMethod('dataToFloatList', locals())

def dataToIntList(data, size, rpgeodataType, endianess):
    logNotImplementedMethod('dataToIntList', locals())

def decodeADPCMBlock(data, bitsPerSample, numSamplesToDecode, lshift, filter, filterTable0, filterTable1, listOf2PreviousSamples, bitOffset, bitStride, sampleScale):
    logNotImplementedMethod('decodeADPCMBlock', locals())

def decodeNormals32(normals, stride, xBits, yBits, zBits, endianness):
    logNotImplementedMethod('decodeNormals32', locals())

def decodePSPVert(*args):
    logNotImplementedMethod('decodePSPVert', locals())

def decodeTangents32(*args):
    logNotImplementedMethod('decodeTangents32', locals())

def decompBlast(*args):
    logNotImplementedMethod('decompBlast', locals())

def decompFPK(*args):
    logNotImplementedMethod('decompFPK', locals())

def decompInflate(sourceBytes, destinationSize, windowSize = 0):
    logNotImplementedMethod('decompInflate', locals())

def decompLZ4(*args):
    logNotImplementedMethod('decompLZ4', locals())

def decompLZHMelt(data, size):
    logNotImplementedMethod('decompLZHMelt', locals())

def decompLZO(*args):
    logNotImplementedMethod('decompLZO', locals())

def decompLZO2(*args):
    logNotImplementedMethod('decompLZO2', locals())

def decompLZS01(*args):
    logNotImplementedMethod('decompLZS01', locals())

def decompPRS(data, size):
    logNotImplementedMethod('decompPRS', locals())

def decompPuff(*args):
    logNotImplementedMethod('decompPuff', locals())

def decompressEdgeIndices(*args):
    logNotImplementedMethod('decompressEdgeIndices', locals())

def decompXMemLZX(*args):
    logNotImplementedMethod('decompXMemLZX', locals())

def decryptAES(data, key):
    logNotImplementedMethod('decryptAES', locals())

def exportArchiveFile(filename, data):
    logNotImplementedMethod('exportArchiveFile', locals())

def exportArchiveFileCheck(*args):
    logNotImplementedMethod('exportArchiveFileCheck', locals())

def getDeferredAnims():
    logNotImplementedMethod('getDeferredAnims', locals())

def getDirForFilePath(path):
    return os.path.dirname(os.path.abspath(path)) + "/"

def getExtensionlessName(path):
    return os.path.splitext(path)[0]

def getFlatWeights(*args):
    logNotImplementedMethod('getFlatWeights', locals())

def getInflatedSize(*args):
    logNotImplementedMethod('getInflatedSize', locals())

def getInputName():
    logNotImplementedMethod('getInputName', locals())

def getLastCheckedName():
    return this.lastCheckedName

def getLocalFileName(path):
    return os.path.basename(path)

def getLZHMeltSize(*args):
    logNotImplementedMethod('getLZHMeltSize', locals())

def getOutputName():
    logNotImplementedMethod('getOutputName', locals())

def getPRSSize(*args):
    logNotImplementedMethod('getPRSSize', locals())

def imageApplyPalette(data, width, height, palette, numberOfPaletteEntries):
    logNotImplementedMethod('imageApplyPalette', locals())

def imageBlit32(destinationData, destinationWidth, destinationHeight, destinationXOffset, destinationYOffset, sourceData, sourceEidth, sourceHeight, sourceXOoffset, sourceYOffset, destStride = 0, sourceStride = 0):
    logNotImplementedMethod('imageBlit32', locals())

def imageDecodeDXT(data, width, height, format):
    logNotImplementedMethod('imageDecodeDXT', locals())

def imageDecodePVRTC(data, width, height, bitsPerPixel, decodeFlags = 0):
    # TODO: not working fully yet
    return pvr.decode(data, width, height, bitsPerPixel)

def imageDecodeRaw(data, width, height, paletteFormat):
    logNotImplementedMethod('imageDecodeRaw', locals())

def imageDecodeRawPal(data, palette, width, height, unk8, paletteFormat):
    logNotImplementedMethod('imageDecodeRawPal', locals())

def imageDXTRemoveFlatFractionBlocks(*args):
    logNotImplementedMethod('imageDXTRemoveFlatFractionBlocks', locals())

def imageEncodeDXT(data, unk4, width, height, encodeFormat):
    logNotImplementedMethod('imageEncodeDXT', locals())

def imageEncodeRaw(data, width, height, paletteFormat):
    logNotImplementedMethod('imageEncodeRaw', locals())

def imageFlipRGBA32(data, width, height, unk0, unk1):
    logNotImplementedMethod('imageFlipRGBA32', locals())

def imageFromMortonOrder(data, width, height, dxtBlockBytes):
    logNotImplementedMethod('imageFromMortonOrder', locals())

def imageGaussianBlur(data, width, height, unk_2_0):
    logNotImplementedMethod('imageGaussianBlur', locals())

def imageGetDDSFromDXT(data, width, height, mipCount, dxtFourccFormat):
    logNotImplementedMethod('imageGetDDSFromDXT', locals())

def imageGetPalette(data, exportWidth, exportHeight, unk_16, null_0, null_1):
    logNotImplementedMethod('imageGetPalette', locals())

def imageGetTexRGBA(srcTex):
    logNotImplementedMethod('imageGetTexRGBA', locals())

def imageGetTGAFromRGBA32(*args):
    logNotImplementedMethod('imageGetTGAFromRGBA32', locals())

def imageInterpolatedSample(*args):
    logNotImplementedMethod('imageInterpolatedSample', locals())

def imageKernelProcess(destinationImage, width, height, bytesPerPixel, kernelMethod):
    logNotImplementedMethod('imageKernelProcess', locals())

def imageMedianCut(*args):
    logNotImplementedMethod('imageMedianCut', locals())

def imageNormalMapFromHeightMap(data, width, height, unk_2_0, unk_1_0):
    logNotImplementedMethod('imageNormalMapFromHeightMap', locals())

def imageNormalSwizzle(*args):
    logNotImplementedMethod('imageNormalSwizzle', locals())

def imageResample(data, width, height, exportWidth, exportHeight):
    logNotImplementedMethod('imageResample', locals())

def imageResampleBox(mipPix, lastMipW, lastMipH, mipW, mipH):
    logNotImplementedMethod('imageResampleBox', locals())

def imageScaleRGBA32(data, colorScale, width, height, unk):
    logNotImplementedMethod('imageScaleRGBA32', locals())

def imageToMortonOrder(sourceImageArray, width, height, bytesPerPixel = None, length = None, additionalFlags = None):
    logNotImplementedMethod('imageToMortonOrder', locals())

def imageTwiddlePS2(*args):
    logNotImplementedMethod('imageTwiddlePS2', locals())

def imageUntile360DXT(data, width, height, unk):
    logNotImplementedMethod('imageUntile360DXT', locals())

def imageUntile360Raw(data, width, height, unk_4):
    logNotImplementedMethod('imageUntile360Raw', locals())

def imageUntwiddlePS2(*args):
    logNotImplementedMethod('imageUntwiddlePS2', locals())

def imageUntwiddlePSP(*args):
    logNotImplementedMethod('imageUntwiddlePSP', locals())

def immBegin(shape):
    logNotImplementedMethod('immBegin', locals())

def immBoneIndex(boneIndex):
    logNotImplementedMethod('immBoneIndex', locals())

def immBoneIndexb(*args):
    logNotImplementedMethod('immBoneIndexb', locals())

def immBoneIndexi(*args):
    logNotImplementedMethod('immBoneIndexi', locals())

def immBoneIndexs(*args):
    logNotImplementedMethod('immBoneIndexs', locals())

def immBoneIndexub(*args):
    logNotImplementedMethod('immBoneIndexub', locals())

def immBoneIndexui(*args):
    logNotImplementedMethod('immBoneIndexui', locals())

def immBoneIndexus(*args):
    logNotImplementedMethod('immBoneIndexus', locals())

def immBoneIndexX(*args):
    logNotImplementedMethod('immBoneIndexX', locals())

def immBoneWeight(boneWeight):
    logNotImplementedMethod('immBoneWeight', locals())

def immBoneWeightf(*args):
    logNotImplementedMethod('immBoneWeightf', locals())

def immBoneWeighthf(*args):
    logNotImplementedMethod('immBoneWeighthf', locals())

def immBoneWeightub(*args):
    logNotImplementedMethod('immBoneWeightub', locals())

def immBoneWeightus(*args):
    logNotImplementedMethod('immBoneWeightus', locals())

def immBoneWeightX(*args):
    logNotImplementedMethod('immBoneWeightX', locals())

def immColor3(*args):
    logNotImplementedMethod('immColor3', locals())

def immColor3f(*args):
    logNotImplementedMethod('immColor3f', locals())

def immColor3hf(*args):
    logNotImplementedMethod('immColor3hf', locals())

def immColor3s(*args):
    logNotImplementedMethod('immColor3s', locals())

def immColor3us(*args):
    logNotImplementedMethod('immColor3us', locals())

def immColor4(color):
    logNotImplementedMethod('immColor4', locals())

def immColor4f(*args):
    logNotImplementedMethod('immColor4f', locals())

def immColor4hf(*args):
    logNotImplementedMethod('immColor4hf', locals())

def immColor4s(*args):
    logNotImplementedMethod('immColor4s', locals())

def immColor4us(*args):
    logNotImplementedMethod('immColor4us', locals())

def immColorX(*args):
    logNotImplementedMethod('immColorX', locals())

def immEnd():
    logNotImplementedMethod('immEnd', locals())

def immLMUV2(lmuv):
    logNotImplementedMethod('immLMUV2', locals())

def immLMUV2f(*args):
    logNotImplementedMethod('immLMUV2f', locals())

def immLMUV2hf(*args):
    logNotImplementedMethod('immLMUV2hf', locals())

def immLMUV2s(*args):
    logNotImplementedMethod('immLMUV2s', locals())

def immLMUV2us(*args):
    logNotImplementedMethod('immLMUV2us', locals())

def immLMUVX(*args):
    logNotImplementedMethod('immLMUVX', locals())

def immNormal3(normal):
    logNotImplementedMethod('immNormal3', locals())

def immNormal3f(*args):
    logNotImplementedMethod('immNormal3f', locals())

def immNormal3hf(*args):
    logNotImplementedMethod('immNormal3hf', locals())

def immNormal3s(*args):
    logNotImplementedMethod('immNormal3s', locals())

def immNormal3us(*args):
    logNotImplementedMethod('immNormal3us', locals())

def immNormalX(*args):
    logNotImplementedMethod('immNormalX', locals())

def immTangent4(*args):
    logNotImplementedMethod('immTangent4', locals())

def immTangent4f(*args):
    logNotImplementedMethod('immTangent4f', locals())

def immTangent4hf(*args):
    logNotImplementedMethod('immTangent4hf', locals())

def immTangent4s(*args):
    logNotImplementedMethod('immTangent4s', locals())

def immTangent4us(*args):
    logNotImplementedMethod('immTangent4us', locals())

def immTangentX(*args):
    logNotImplementedMethod('immTangentX', locals())

def immUserData(*args):
    logNotImplementedMethod('immUserData', locals())

def immUV2(uv):
    logNotImplementedMethod('immUV2', locals())

def immUV2f(*args):
    logNotImplementedMethod('immUV2f', locals())

def immUV2hf(*args):
    logNotImplementedMethod('immUV2hf', locals())

def immUV2s(*args):
    logNotImplementedMethod('immUV2s', locals())

def immUV2us(*args):
    logNotImplementedMethod('immUV2us', locals())

def immUVX(*args):
    logNotImplementedMethod('immUVX', locals())

def immVertex3(vertex):
    logNotImplementedMethod('immVertex3', locals())

def immVertex3f(positions, offset = 0):
    logNotImplementedMethod('immVertex3f', locals())

def immVertex3hf(*args):
    logNotImplementedMethod('immVertex3hf', locals())

def immVertex3s(*args):
    logNotImplementedMethod('immVertex3s', locals())

def immVertex3us(*args):
    logNotImplementedMethod('immVertex3us', locals())

def immVertexX(*args):
    logNotImplementedMethod('immVertexX', locals())

def immVertMorphIndex(*args):
    logNotImplementedMethod('immVertMorphIndex', locals())

def isGeometryTarget():
    logNotImplementedMethod('isGeometryTarget', locals())

def loadExternalTex(texName):
    logNotImplementedMethod('loadExternalTex', locals())

def loadFileOnTexturePaths(*args):
    logNotImplementedMethod('loadFileOnTexturePaths', locals())

def loadIntoByteArray(path):
    handle = open(path, "rb")
    data = handle.read()
    handle.close()
    return data

def loadMdlTextures(*args):
    logNotImplementedMethod('loadMdlTextures', locals())

def loadPairedFile(name, extension):
    logNotImplementedMethod('loadPairedFile', locals())

def loadPairedFileGetPath(*args):
    logNotImplementedMethod('loadPairedFileGetPath', locals())

def loadPairedFileOptional(*args):
    logNotImplementedMethod('loadPairedFileOptional', locals())

def loadTexByHandler(data, type):
    logNotImplementedMethod('loadTexByHandler', locals())

def mergeKeyFramedFloats(xyz):
    logNotImplementedMethod('mergeKeyFramedFloats', locals())

def multiplyBones(bones):
    logNotImplementedMethod('multiplyBones', locals())

def noesisIsExporting(*args):
    logNotImplementedMethod('noesisIsExporting', locals())

def processCommands(*args):
    logNotImplementedMethod('processCommands', locals())

def rpgBindBoneIndexBuffer(data, type, stride, count):
    return rpgBindBoneIndexBufferOfs(data, type, stride, 0, count)

def rpgBindBoneIndexBufferOfs(data, type, stride, offset, count):
    unpackedBuffer = unpackBuffer(data, type, stride, offset, count)
    this.context.boneIndexBuffer = unpackedBuffer

def rpgBindBoneWeightBuffer(data, type, stride, count):
    return rpgBindBoneWeightBufferOfs(data, type, stride, 0, count)

def rpgBindBoneWeightBufferOfs(data, type, stride, offset, count):
    unpackedBuffer = unpackBuffer(data, type, stride, offset, count)
    this.context.boneWeightBuffer = unpackedBuffer

def rpgBindColorBuffer(data, type, stride, count):
    return rpgBindColorBufferOfs(data, type, stride, 0, count)

def rpgBindColorBufferOfs(data, type, stride, offset, count):
    if count >= 1 and count <= 4:
        doException('rpgBindColorBufferOfs, count argument must be one of 1, 2, 3, 4')

    unpackedBuffer = unpackBuffer(data, type, stride, offset, count)
    this.context.colorBuffer = unpackedBuffer

def rpgBindNormalBuffer(data, type, stride):
    return rpgBindNormalBufferOfs(data, type, stride, 0)

def rpgBindNormalBufferOfs(data, type, stride, offset):
    unpackedBuffer = unpackBuffer(data, type, stride, offset, 3)
    this.context.normalBuffer = unpackedBuffer

def rpgBindPositionBuffer(data, type, stride):
    return rpgBindPositionBufferOfs(data, type, stride, 0)

def rpgBindPositionBufferOfs(data, type, stride, offset):
    unpackedBuffer = unpackBuffer(data, type, stride, offset, 3)
    this.context.vertexBuffer = unpackedBuffer

def rpgBindTangentBuffer(data, type, stride):
    return rpgBindTangentBufferOfs(data, type, stride, 0)

def rpgBindTangentBufferOfs(data, type, stride, offset):
    logNotImplementedMethod('rpgBindTangentBufferOfs', locals())

def rpgBindUserDataBuffer(data, type, stride):
    return rpgBindUserDataBufferOfs(data, type, stride, 0)

def rpgBindUserDataBufferOfs(data, type, stride, offset):
    logNotImplementedMethod('rpgBindUserDataBufferOfs', locals())

def rpgBindUV1Buffer(data, type, stride):
    return rpgBindUV1BufferOfs(data, type, stride, 0)

def rpgBindUV1BufferOfs(data, type, stride, offset):
    unpackedBuffer = unpackBuffer(data, type, stride, offset, 2)
    this.context.uvBuffer = unpackedBuffer

def rpgBindUV2Buffer(data, type, stride):
    return rpgBindUV2BufferOfs(data, type, stride, 0)

def rpgBindUV2BufferOfs(data, type, stride, offset):
    unpackedBuffer = unpackBuffer(data, type, stride, offset, 2)
    this.context.uv2Buffer = unpackedBuffer

def rpgClearBufferBinds():
    this.context.clearBuffers()

def rpgClearMaterials(*args):
    logNotImplementedMethod('rpgClearMaterials', locals())

def rpgClearMorphs(*args):
    logNotImplementedMethod('rpgClearMorphs', locals())

def rpgClearNames(*args):
    logNotImplementedMethod('rpgClearNames', locals())

def rpgCommitMorphFrame(numMFPos):
    logNotImplementedMethod('rpgCommitMorphFrame', locals())

def rpgCommitMorphFrameSet():
    logNotImplementedMethod('rpgCommitMorphFrameSet', locals())

def rpgCommitTriangles(data, type, numIdx, shape, usePlotMap):
    fmt = str(numIdx) + UNPACK_TYPES[type]
    unpackedBuffer = struct.unpack(fmt, data)
    this.context.commit(unpackedBuffer, type, numIdx, shape, usePlotMap)

def rpgConstructModel():
    meshes = this.context.meshes
    model = inc_noesis.NoeModel(meshes)
    return model

def rpgConstructModelSlim():
    return rpgConstructModel()

def rpgCreateContext():
    context = Context()
    this.context = context
    return context

def rpgCreatePlaneSpaceUVs():
    logNotImplementedMethod('rpgCreatePlaneSpaceUVs', locals())

def rpgFeedMorphTargetNormals(morphNrmAr, type, stride):
    logNotImplementedMethod('rpgFeedMorphTargetNormals', locals())

def rpgFeedMorphTargetNormalsOfs(morphNrmAr, type, stride, offset):
    logNotImplementedMethod('rpgFeedMorphTargetNormalsOfs', locals())

def rpgFeedMorphTargetPositions(morphPosAr, type, stride):
    logNotImplementedMethod('rpgFeedMorphTargetPositions', locals())

def rpgFeedMorphTargetPositionsOfs(morphPosAr, type, stride, offset):
    logNotImplementedMethod('rpgFeedMorphTargetPositionsOfs', locals())

def rpgFlatNormals():
    logNotImplementedMethod('rpgFlatNormals', locals())

def rpgGetMorphBase(*args):
    logNotImplementedMethod('rpgGetMorphBase', locals())

def rpgGetOption(*args):
    logNotImplementedMethod('rpgGetOption', locals())

def rpgGetStripEnder(*args):
    logNotImplementedMethod('rpgGetStripEnder', locals())

def rpgGetTriangleCount(*args):
    logNotImplementedMethod('rpgGetTriangleCount', locals())

def rpgGetVertexCount():
    logNotImplementedMethod('rpgGetVertexCount', locals())

def rpgOptimize():
    logNotImplementedMethod('rpgOptimize', locals())

def rpgReset():
    logNotImplementedMethod('rpgReset', locals())

def rpgSetActiveContext(*args):
    logNotImplementedMethod('rpgSetActiveContext', locals())

def rpgSetBoneMap(boneMap):
    this.context.boneMap = boneMap

def rpgSetEndian(bigEndian):
    logNotImplementedMethod('rpgSetEndian', locals())

def rpgSetLightmap(name):
    this.context.lightMap = name

def rpgSetMaterial(material):
    this.context.material = material

def rpgSetMorphBase(*args):
    logNotImplementedMethod('rpgSetMorphBase', locals())

def rpgSetName(name):
    this.context.name = name

def rpgSetOption(key, value):
    logNotImplementedMethod('rpgSetOption', locals())

def rpgSetPosScaleBias(*args):
    logNotImplementedMethod('rpgSetPosScaleBias', locals())

def rpgSetStripEnder(*args):
    logNotImplementedMethod('rpgSetStripEnder', locals())

def rpgSetTransform(*args):
    logNotImplementedMethod('rpgSetTransform', locals())

def rpgSetTriWinding(*args):
    logNotImplementedMethod('rpgSetTriWinding', locals())

def rpgSetUVScaleBias(scale, bias):
    this.context.uvScaleBias = { "scale": scale, "bias": bias }

def rpgSkinPreconstructedVertsToBones(bindCorrectionBones, numPreCommitVerts, numVertsToSkin):
    logNotImplementedMethod('rpgSkinPreconstructedVertsToBones', locals())

def rpgSmoothNormals(*args):
    logNotImplementedMethod('rpgSmoothNormals', locals())

def rpgSmoothTangents():
    logNotImplementedMethod('rpgSmoothTangents', locals())

def rpgUnifyBinormals(unk_1):
    logNotImplementedMethod('rpgUnifyBinormals', locals())

def setDeferredAnims(anims):
    logNotImplementedMethod('setDeferredAnims', locals())

def setPreviewOption(key, value):
    logNotImplementedMethod('setPreviewOption', locals())

def simulateDragAndDrop(fileName):
    logNotImplementedMethod('simulateDragAndDrop', locals())

def splineToMeshBuffers(spline, tmat, unk_1, unk_0_05, unk_3_0, unk_2):
    logNotImplementedMethod('splineToMeshBuffers', locals())

def swapEndianArray(bytes, unk2):
    logNotImplementedMethod('swapEndianArray', locals())

def toolExportGData(savePath, unk_empty):
    logNotImplementedMethod('toolExportGData', locals())

def toolFreeGData():
    logNotImplementedMethod('toolFreeGData', locals())

def toolGetLoadedModel(*args):
    logNotImplementedMethod('toolGetLoadedModel', locals())

def toolGetLoadedModelCount(*args):
    logNotImplementedMethod('toolGetLoadedModelCount', locals())

def toolLoadGData(*args):
    logNotImplementedMethod('toolLoadGData', locals())

def toolSetGData(models):
    logNotImplementedMethod('toolSetGData', locals())

def unpackPS2VIF(*args):
    logNotImplementedMethod('unpackPS2VIF', locals())

def writePCMWaveFile(*args):
    logNotImplementedMethod('writePCMWaveFile', locals())

# private

def setLastCheckedName(name):
    this.lastCheckedName = name

def splitBuffer(data, stride):
    return [data[i:i + stride] for i in range(0, len(data), stride)]

def unpackBuffer(data, type, stride, offset, count):
    splitted = splitBuffer(data, stride)
    typeSize = UNPACK_SIZES[type]
    unpackType = UNPACK_TYPES[type]
    fmt = str(count) + unpackType
    mapped = map(lambda x: x[offset:offset + typeSize * count], splitted)
    mapped = map(lambda x: struct.unpack(fmt, x), mapped)
    mapped = fixHalfFloats(mapped, type)
    return mapped

# half float needs to mapped to normal float in python
def fixHalfFloats(values, type):
    if not type == noesis.RPGEODATA_HALFFLOAT:
        return values

    return map(lambda touple: map(lambda y: noesis.getFloat16(y), touple), values)
