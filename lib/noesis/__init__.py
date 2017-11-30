from Handler import Handler
from NoeModule import NoeModule
from AllocType import AllocType
from numbers import Number
import sys
import logger

# constants

BITSTREAMFL_DESCENDINGBITS = 'BITSTREAMFL_DESCENDINGBITS'
BLITFLAG_ALPHABLEND = 'BLITFLAG_ALPHABLEND'
FOURCC_ATI1 = 'FOURCC_ATI1'
FOURCC_ATI2 = 'FOURCC_ATI2'
FOURCC_DXT1 = 'FOURCC_DXT1'
FOURCC_DXT1NORMAL = 'FOURCC_DXT1NORMAL'
g_flDegToRad = 0.0174532925
g_flRadToDeg = 57.2957795
NFORMATFLAG_IMGREAD = 'NFORMATFLAG_IMGREAD'
NFORMATFLAG_MODELREAD = 'NFORMATFLAG_MODELREAD'
NMATFLAG_ENV_FLIP = 'NMATFLAG_ENV_FLIP'
NMATFLAG_PBR_METAL = 'NMATFLAG_PBR_METAL'
NMATFLAG_PBR_ROUGHNESS_NRMALPHA = 'NMATFLAG_PBR_ROUGHNESS_NRMALPHA'
NMATFLAG_PBR_SPEC_IR_RG = 'NMATFLAG_PBR_SPEC_IR_RG'
NMATFLAG_TWOSIDED = 'NMATFLAG_TWOSIDED'
NOE_ENCODEDXT_BC1 = 'NOE_ENCODEDXT_BC1'
NOEKF_INTERPOLATE_LINEAR = 'NOEKF_INTERPOLATE_LINEAR'
NOEKF_ROTATION_QUATERNION_4 = 'NOEKF_ROTATION_QUATERNION_4'
NOEKF_SCALE_SCALAR_1 = 'NOEKF_SCALE_SCALAR_1'
NOEKF_TRANSLATION_VECTOR_3 = 'NOEKF_TRANSLATION_VECTOR_3'
NOESISTEX_DXT1 = 'NOESISTEX_DXT1'
NOESISTEX_DXT3 = 'NOESISTEX_DXT3'
NOESISTEX_DXT5 = 'NOESISTEX_DXT5'
NOESISTEX_RGB24 = 'NOESISTEX_RGB24'
NOESISTEX_RGBA32 = 'NOESISTEX_RGBA32'
NOESISTEX_UNKNOWN = 'NOESISTEX_UNKNOWN'
NOESPLINEFLAG_CLOSED = 'NOESPLINEFLAG_CLOSED'
NOEUSERVAL_SAVEFILEPATH = 'NOEUSERVAL_SAVEFILEPATH'
NOEUSERVAL_STRING = 'NOEUSERVAL_STRING'
NTEXFLAG_CUBEMAP = 'NTEXFLAG_CUBEMAP'
NTEXFLAG_FILTER_NEAREST = 'NTEXFLAG_FILTER_NEAREST'
NTEXFLAG_WRAP_CLAMP = 'NTEXFLAG_WRAP_CLAMP'
NTOOLFLAG_CONTEXTITEM = 'NTOOLFLAG_CONTEXTITEM'
OPTFLAG_WANTARG = 'OPTFLAG_WANTARG'
PVRTC_DECODE_LINEARORDER = 'PVRTC_DECODE_LINEARORDER'
PVRTC_DECODE_PVRTC2 = 'PVRTC_DECODE_PVRTC2'
PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA = 'PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA'
RPGEO_QUAD_ABC_ACD = 'RPGEO_QUAD_ABC_ACD'
RPGEO_TRIANGLE = 'RPGEO_TRIANGLE'
RPGEO_TRIANGLE_STRIP = 'RPGEO_TRIANGLE_STRIP'
RPGEODATA_BYTE = 1
RPGEODATA_FLOAT = 4
RPGEODATA_HALFFLOAT = 2
RPGEODATA_INT = 4
RPGEODATA_SHORT = 2
RPGEODATA_UBYTE = 1
RPGEODATA_UINT = 4
RPGEODATA_USHORT = 2
RPGOPT_BIGENDIAN = 'RPGOPT_BIGENDIAN'
RPGOPT_SWAPHANDEDNESS = 'RPGOPT_SWAPHANDEDNESS'
RPGOPT_TANMATROTATE = 'RPGOPT_TANMATROTATE'
RPGOPT_TRIWINDBACKWARD = 'RPGOPT_TRIWINDBACKWARD'

# state

this = sys.modules[__name__]
this.plugins = []
this.this.modules = []

# methods

def addOption(handle, option, description, flags):
    return handle.addOption(option, description, flags)

def allocBytes(size):
    return bytearray(size)

def freeModule(module):
    logger.logNotImplementedMethod('freeModule', locals())

def getCharSplineSet():
    logger.logNotImplementedMethod('getCharSplineSet', locals())

def getFormatExtensionFlags():
    logger.logNotImplementedMethod('getFormatExtensionFlags', locals())

def getMFFP(uint):
    logger.logNotImplementedMethod('getMFFP', locals())

def getScenesPath():
    logger.logNotImplementedMethod('getScenesPath', locals())

def getSelectedDirectory():
    logger.logNotImplementedMethod('getSelectedDirectory', locals())

def getSelectedFile():
    logger.logNotImplementedMethod('getSelectedFile', locals())

def getWindowHandle():
    logger.logNotImplementedMethod('getWindowHandle', locals())

def instantiateModule():
    module = NoeModule()
    this.modules.append(module)
    return module

def isPreviewModuleRAPIValid():
    logger.logNotImplementedMethod('isPreviewModuleRAPIValid', locals())

def loadImageRGBA():
    logger.logNotImplementedMethod('loadImageRGBA', locals())

def logPopup():
    # this should open the debug window
    pass

def messagePrompt():
    logger.logNotImplementedMethod('messagePrompt', locals())

def openAndRemoveTempFile():
    logger.logNotImplementedMethod('openAndRemoveTempFile', locals())

def openFile():
    logger.logNotImplementedMethod('openFile', locals())

def optGetArg():
    logger.logNotImplementedMethod('optGetArg', locals())

def optWasInvoked():
    logger.logNotImplementedMethod('optWasInvoked', locals())

# TODO: fileType can be semicolon separated '.obj;.obc'
def register(name, fileType):
    handler = Handler(name, fileType)
    this.plugins.append(handler)
    return handler

def registerCleanupFunction():
    logger.logNotImplementedMethod('registerCleanupFunction', locals())

def registerTool():
    logger.logNotImplementedMethod('registerTool', locals())

def setHandlerExtractArc(handle, value):
    handle.grpExtractArc = value

def setHandlerLoadModel(handle, value):
    handle.noepyLoadModel = value

def setHandlerLoadRGBA(handle, value):
    handle.txdLoadRGBA = value

def setHandlerTypeCheck(handle, value):
    handle.noepyCheckType = value

def setHandlerWriteModel(handle, value):
    handle.noepyWriteModel = value

def setHandlerWriteRGBA(handle, value):
    handle.walWriteRGBA = value

def setHandlerWriteAnim(handle, value):
    handle.noepyWriteAnim = value

def setModuleRAPI():
    logger.logNotImplementedMethod('setModuleRAPI', locals())

def setPreviewModuleRAPI():
    logger.logNotImplementedMethod('setPreviewModuleRAPI', locals())

def setToolFlags():
    logger.logNotImplementedMethod('setToolFlags', locals())

def setToolVisibleCallback():
    logger.logNotImplementedMethod('setToolVisibleCallback', locals())

def userPrompt():
    logger.logNotImplementedMethod('userPrompt', locals())

# inc_noesis methods

def allocType(name, data = None):
    return AllocType(name, data)

def anglesALerp(noeAngles, other, degrees):
    logger.logNotImplementedMethod('anglesALerp', locals())

def anglesAngleVectors(noeAngles):
    logger.logNotImplementedMethod('anglesAngleVectors', locals())

def anglesMod(noeAngles, f):
    logger.logNotImplementedMethod('anglesMod', locals())

def anglesNormalize180(noeAngles):
    logger.logNotImplementedMethod('anglesNormalize180', locals())

def anglesNormalize360(noeAngles):
    logger.logNotImplementedMethod('anglesNormalize360', locals())

def anglesToMat43_XYZ(noeAngles, yFlip):
    logger.logNotImplementedMethod('anglesToMat43_XYZ', locals())
    return inc_noesis.NoeMat43()

def anglesToMat43(noeAngles):
    logger.logNotImplementedMethod('anglesToMat43', locals())

def anglesToQuat(noeAngles):
    logger.logNotImplementedMethod('anglesToQuat', locals())

def anglesToVec3(noeAngles):
    logger.logNotImplementedMethod('anglesToVec3', locals())

def anglesValidate(noeAngles):
    vec3Validate(noeAngles)

def bsGetBuffer(handle):
    return handle.bsGetBuffer()

def bsGetBufferSlice(handle, startOfs, endOfs):
    return handle.bsGetBufferSlice(startOfs, endOfs)

def bsGetFlags(handle):
    return handle.bsGetFlags()

def bsGetOfs(handle):
    return handle.bsGetOfs()

def bsGetSize(handle):
    return handle.bsGetSize()

def bsReadBits(handle, numBits):
    return handle.bsReadBits(numBits)

def bsReadBool(handle):
    return handle.bsReadBool()

def bsReadByte(handle):
    return handle.bsReadByte()

def bsReadBytes(handle, numBytes):
    return handle.bsReadBytes(numBytes)

def bsReadDouble(handle):
    return handle.bsReadDouble()

def bsReadFloat(handle):
    return handle.bsReadFloat()

def bsReadInt(handle):
    return handle.bsReadInt()

def bsReadInt64(handle):
    return handle.bsReadInt64()

def bsReadLine(handle):
    return handle.bsReadLine()

def bsReadShort(handle):
    return handle.bsReadShort()

def bsReadString(handle):
    return handle.bsReadString()

def bsReadUByte(handle):
    return handle.bsReadUByte()

def bsReadUInt(handle):
    return handle.bsReadUInt()

def bsReadUInt64(handle):
    return handle.bsReadUInt64()

def bsReadUShort(handle):
    return handle.bsReadUShort()

def bsSetEndian(handle, bigEndian):
    return handle.bsSetEndian(bigEndian)

def bsSetFlags(handle, flags):
    return handle.bsSetFlags(flags)

def bsSetOfs(handle, ofs):
    return handle.bsSetOfs(ofs)

def bsWriteBits(handle, val, numBits):
    return handle.bsWriteBits(val, numBits)

def bsWriteBool(handle, val):
    return handle.bsWriteBool(val)

def bsWriteByte(handle, val):
    return handle.bsWriteByte(val)

def bsWriteBytes(handle, data):
    return handle.bsWriteBytes(data)

def bsWriteDouble(handle, val):
    return handle.bsWriteDouble(val)

def bsWriteFloat(handle, val):
    return handle.bsWriteFloat(val)

def bsWriteInt(handle, val):
    return handle.bsWriteInt(val)

def bsWriteInt64(handle, val):
    return handle.bsWriteInt64(val)

def bsWriteShort(handle, val):
    return handle.bsWriteShort(val)

def bsWriteString(handle, str, writeTerminator):
    return handle.bsWriteString(str, writeTerminator)

def bsWriteUByte(handle, val):
    return handle.bsWriteUByte(val)

def bsWriteUInt(handle, val):
    return handle.bsWriteUInt(val)

def bsWriteUInt64(handle, val):
    return handle.bsWriteUInt64(val)

def bsWriteUShort(handle, val):
    return handle.bsWriteUShort(val)

def cubicBezier3D(points, frac):
    logger.logNotImplementedMethod('cubicBezier3D', locals())

def doException(name):
    raise ValueError(name)

def encodeFloat16(val):
    logger.logNotImplementedMethod('encodeFloat16', locals())

def getFloat16(ushort):
    logger.logNotImplementedMethod('getFloat16', locals())

def mat43Add(noeMat43, other):
    logger.logNotImplementedMethod('mat43Add', locals())

def mat43FromBytes(otherBytes, bigEnd):
    logger.logNotImplementedMethod('mat43FromBytes', locals())

def mat43Inverse(noeMat43):
    logger.logNotImplementedMethod('mat43Inverse', locals())

def mat43IsSkewed(noeMat43):
    logger.logNotImplementedMethod('mat43IsSkewed', locals())

def mat43Lerp(noeMat43, other, fraction):
    logger.logNotImplementedMethod('mat43Lerp', locals())

def mat43Mul(noeMat43, other):
    noeMat44 = noeMat43.toMat44()
    otherMat44 = other.toMat44()
    return (noeMat44 * otherMat44).toMat43()

def mat43Orthogonalize(noeMat43):
    logger.logNotImplementedMethod('mat43Orthogonalize', locals())

def mat43Rotate(noeMat43, degrees, rotAngles, transposeRot):
    logger.logNotImplementedMethod('mat43Rotate', locals())

def mat43SLerp(noeMat43, other, fraction):
    logger.logNotImplementedMethod('mat43SLerp', locals())

def mat43Sub(noeMat43, other):
    logger.logNotImplementedMethod('mat43Sub', locals())

def mat43SwapHandedness(noeMat43, axis):
    logger.logNotImplementedMethod('mat43SwapHandedness', locals())

def mat43ToAngles(noeMat43):
    logger.logNotImplementedMethod('mat43ToAngles', locals())

def mat43ToBytes(noeMat43):
    logger.logNotImplementedMethod('mat43ToBytes', locals())

def mat43ToMat44(noeMat43):
    tmp = inc_noesis.NoeMat44()

    tmp[0][0] = noeMat43[0][0]
    tmp[0][1] = noeMat43[0][1]
    tmp[0][2] = noeMat43[0][2]
    tmp[1][0] = noeMat43[1][0]
    tmp[1][1] = noeMat43[1][1]
    tmp[1][2] = noeMat43[1][2]
    tmp[2][0] = noeMat43[2][0]
    tmp[2][1] = noeMat43[2][1]
    tmp[2][2] = noeMat43[2][2]
    tmp[3][0] = noeMat43[3][0]
    tmp[3][1] = noeMat43[3][1]
    tmp[3][2] = noeMat43[3][2]

    return tmp

def mat43ToQuat(noeMat43):
    logger.logNotImplementedMethod('mat43ToQuat', locals())

def mat43TransformNormal(noeMat43, other):
    logger.logNotImplementedMethod('mat43TransformNormal', locals())

def mat43TransformPoint(noeMat43, other):
    logger.logNotImplementedMethod('mat43TransformPoint', locals())

def mat43TransformVec4(noeMat43, other):
    logger.logNotImplementedMethod('mat43TransformVec4', locals())

def mat43Translate(noeMat43, trnVector):
    logger.logNotImplementedMethod('mat43Translate', locals())

def mat43Transpose(noeMat43):
    logger.logNotImplementedMethod('mat43Transpose', locals())

def mat43Validate(noeMat43):
    mat43 = noeMat43.mat43

    if len(mat43) != 4:
        doException("mat43Validate: validate failed")

    for vec in mat43:
        vec3Validate(vec)

def mat44Add(noeMat44, other):
    logger.logNotImplementedMethod('mat44Add', locals())

def mat44FromBytes(otherBytes, bigEnd):
    logger.logNotImplementedMethod('mat44FromBytes', locals())

def mat44Inverse(mtx):
    tmp = inc_noesis.NoeMat44()

    det = (
          (mtx[0][0] * mtx[1][1] - mtx[1][0] * mtx[0][1])
        * (mtx[2][2] * mtx[3][3] - mtx[3][2] * mtx[2][3])
        - (mtx[0][0] * mtx[2][1] - mtx[2][0] * mtx[0][1])
        * (mtx[1][2] * mtx[3][3] - mtx[3][2] * mtx[1][3])
        + (mtx[0][0] * mtx[3][1] - mtx[3][0] * mtx[0][1])
        * (mtx[1][2] * mtx[2][3] - mtx[2][2] * mtx[1][3])
        + (mtx[1][0] * mtx[2][1] - mtx[2][0] * mtx[1][1])
        * (mtx[0][2] * mtx[3][3] - mtx[3][2] * mtx[0][3])
        - (mtx[1][0] * mtx[3][1] - mtx[3][0] * mtx[1][1])
        * (mtx[0][2] * mtx[2][3] - mtx[2][2] * mtx[0][3])
        + (mtx[2][0] * mtx[3][1] - mtx[3][0] * mtx[2][1])
        * (mtx[0][2] * mtx[1][3] - mtx[1][2] * mtx[0][3])
    )

    if (det == 0.0):
        return tmp
    else:
        det = 1.0 / det

        tmp[0][0] = det * (mtx[1][1] * (mtx[2][2] * mtx[3][3] - mtx[3][2] * mtx[2][3]) + mtx[2][1] * (mtx[3][2] * mtx[1][3] - mtx[1][2] * mtx[3][3]) + mtx[3][1] * (mtx[1][2] * mtx[2][3] - mtx[2][2] * mtx[1][3]))
        tmp[1][0] = det * (mtx[1][2] * (mtx[2][0] * mtx[3][3] - mtx[3][0] * mtx[2][3]) + mtx[2][2] * (mtx[3][0] * mtx[1][3] - mtx[1][0] * mtx[3][3]) + mtx[3][2] * (mtx[1][0] * mtx[2][3] - mtx[2][0] * mtx[1][3]))
        tmp[2][0] = det * (mtx[1][3] * (mtx[2][0] * mtx[3][1] - mtx[3][0] * mtx[2][1]) + mtx[2][3] * (mtx[3][0] * mtx[1][1] - mtx[1][0] * mtx[3][1]) + mtx[3][3] * (mtx[1][0] * mtx[2][1] - mtx[2][0] * mtx[1][1]))
        tmp[3][0] = det * (mtx[1][0] * (mtx[3][1] * mtx[2][2] - mtx[2][1] * mtx[3][2]) + mtx[2][0] * (mtx[1][1] * mtx[3][2] - mtx[3][1] * mtx[1][2]) + mtx[3][0] * (mtx[2][1] * mtx[1][2] - mtx[1][1] * mtx[2][2]))

        tmp[0][1] = det * (mtx[2][1] * (mtx[0][2] * mtx[3][3] - mtx[3][2] * mtx[0][3]) + mtx[3][1] * (mtx[2][2] * mtx[0][3] - mtx[0][2] * mtx[2][3]) + mtx[0][1] * (mtx[3][2] * mtx[2][3] - mtx[2][2] * mtx[3][3]))
        tmp[1][1] = det * (mtx[2][2] * (mtx[0][0] * mtx[3][3] - mtx[3][0] * mtx[0][3]) + mtx[3][2] * (mtx[2][0] * mtx[0][3] - mtx[0][0] * mtx[2][3]) + mtx[0][2] * (mtx[3][0] * mtx[2][3] - mtx[2][0] * mtx[3][3]))
        tmp[2][1] = det * (mtx[2][3] * (mtx[0][0] * mtx[3][1] - mtx[3][0] * mtx[0][1]) + mtx[3][3] * (mtx[2][0] * mtx[0][1] - mtx[0][0] * mtx[2][1]) + mtx[0][3] * (mtx[3][0] * mtx[2][1] - mtx[2][0] * mtx[3][1]))
        tmp[3][1] = det * (mtx[2][0] * (mtx[3][1] * mtx[0][2] - mtx[0][1] * mtx[3][2]) + mtx[3][0] * (mtx[0][1] * mtx[2][2] - mtx[2][1] * mtx[0][2]) + mtx[0][0] * (mtx[2][1] * mtx[3][2] - mtx[3][1] * mtx[2][2]))

        tmp[0][2] = det * (mtx[3][1] * (mtx[0][2] * mtx[1][3] - mtx[1][2] * mtx[0][3]) + mtx[0][1] * (mtx[1][2] * mtx[3][3] - mtx[3][2] * mtx[1][3]) + mtx[1][1] * (mtx[3][2] * mtx[0][3] - mtx[0][2] * mtx[3][3]))
        tmp[1][2] = det * (mtx[3][2] * (mtx[0][0] * mtx[1][3] - mtx[1][0] * mtx[0][3]) + mtx[0][2] * (mtx[1][0] * mtx[3][3] - mtx[3][0] * mtx[1][3]) + mtx[1][2] * (mtx[3][0] * mtx[0][3] - mtx[0][0] * mtx[3][3]))
        tmp[2][2] = det * (mtx[3][3] * (mtx[0][0] * mtx[1][1] - mtx[1][0] * mtx[0][1]) + mtx[0][3] * (mtx[1][0] * mtx[3][1] - mtx[3][0] * mtx[1][1]) + mtx[1][3] * (mtx[3][0] * mtx[0][1] - mtx[0][0] * mtx[3][1]))
        tmp[3][2] = det * (mtx[3][0] * (mtx[1][1] * mtx[0][2] - mtx[0][1] * mtx[1][2]) + mtx[0][0] * (mtx[3][1] * mtx[1][2] - mtx[1][1] * mtx[3][2]) + mtx[1][0] * (mtx[0][1] * mtx[3][2] - mtx[3][1] * mtx[0][2]))

        tmp[0][3] = det * (mtx[0][1] * (mtx[2][2] * mtx[1][3] - mtx[1][2] * mtx[2][3]) + mtx[1][1] * (mtx[0][2] * mtx[2][3] - mtx[2][2] * mtx[0][3]) + mtx[2][1] * (mtx[1][2] * mtx[0][3] - mtx[0][2] * mtx[1][3]))
        tmp[1][3] = det * (mtx[0][2] * (mtx[2][0] * mtx[1][3] - mtx[1][0] * mtx[2][3]) + mtx[1][2] * (mtx[0][0] * mtx[2][3] - mtx[2][0] * mtx[0][3]) + mtx[2][2] * (mtx[1][0] * mtx[0][3] - mtx[0][0] * mtx[1][3]))
        tmp[2][3] = det * (mtx[0][3] * (mtx[2][0] * mtx[1][1] - mtx[1][0] * mtx[2][1]) + mtx[1][3] * (mtx[0][0] * mtx[2][1] - mtx[2][0] * mtx[0][1]) + mtx[2][3] * (mtx[1][0] * mtx[0][1] - mtx[0][0] * mtx[1][1]))
        tmp[3][3] = det * (mtx[0][0] * (mtx[1][1] * mtx[2][2] - mtx[2][1] * mtx[1][2]) + mtx[1][0] * (mtx[2][1] * mtx[0][2] - mtx[0][1] * mtx[2][2]) + mtx[2][0] * (mtx[0][1] * mtx[1][2] - mtx[1][1] * mtx[0][2]))

        return tmp

def mat44Mul(mtx, rhs):
    tmp = inc_noesis.NoeMat44()

    # Row 1
    tmp[0][0] = (mtx[0][0] * rhs[0][0]) + (mtx[0][1] * rhs[1][0]) + (mtx[0][2] * rhs[2][0]) + (mtx[0][3] * rhs[3][0])
    tmp[0][1] = (mtx[0][0] * rhs[0][1]) + (mtx[0][1] * rhs[1][1]) + (mtx[0][2] * rhs[2][1]) + (mtx[0][3] * rhs[3][1])
    tmp[0][2] = (mtx[0][0] * rhs[0][2]) + (mtx[0][1] * rhs[1][2]) + (mtx[0][2] * rhs[2][2]) + (mtx[0][3] * rhs[3][2])
    tmp[0][3] = (mtx[0][0] * rhs[0][3]) + (mtx[0][1] * rhs[1][3]) + (mtx[0][2] * rhs[2][3]) + (mtx[0][3] * rhs[3][3])

    # Row 2
    tmp[1][0] = (mtx[1][0] * rhs[0][0]) + (mtx[1][1] * rhs[1][0]) + (mtx[1][2] * rhs[2][0]) + (mtx[1][3] * rhs[3][0])
    tmp[1][1] = (mtx[1][0] * rhs[0][1]) + (mtx[1][1] * rhs[1][1]) + (mtx[1][2] * rhs[2][1]) + (mtx[1][3] * rhs[3][1])
    tmp[1][2] = (mtx[1][0] * rhs[0][2]) + (mtx[1][1] * rhs[1][2]) + (mtx[1][2] * rhs[2][2]) + (mtx[1][3] * rhs[3][2])
    tmp[1][3] = (mtx[1][0] * rhs[0][3]) + (mtx[1][1] * rhs[1][3]) + (mtx[1][2] * rhs[2][3]) + (mtx[1][3] * rhs[3][3])

    # Row 3
    tmp[2][0] = (mtx[2][0] * rhs[0][0]) + (mtx[2][1] * rhs[1][0]) + (mtx[2][2] * rhs[2][0]) + (mtx[2][3] * rhs[3][0])
    tmp[2][1] = (mtx[2][0] * rhs[0][1]) + (mtx[2][1] * rhs[1][1]) + (mtx[2][2] * rhs[2][1]) + (mtx[2][3] * rhs[3][1])
    tmp[2][2] = (mtx[2][0] * rhs[0][2]) + (mtx[2][1] * rhs[1][2]) + (mtx[2][2] * rhs[2][2]) + (mtx[2][3] * rhs[3][2])
    tmp[2][3] = (mtx[2][0] * rhs[0][3]) + (mtx[2][1] * rhs[1][3]) + (mtx[2][2] * rhs[2][3]) + (mtx[2][3] * rhs[3][3])

    # Row 4
    tmp[3][0] = (mtx[3][0] * rhs[0][0]) + (mtx[3][1] * rhs[1][0]) + (mtx[3][2] * rhs[2][0]) + (mtx[3][3] * rhs[3][0])
    tmp[3][1] = (mtx[3][0] * rhs[0][1]) + (mtx[3][1] * rhs[1][1]) + (mtx[3][2] * rhs[2][1]) + (mtx[3][3] * rhs[3][1])
    tmp[3][2] = (mtx[3][0] * rhs[0][2]) + (mtx[3][1] * rhs[1][2]) + (mtx[3][2] * rhs[2][2]) + (mtx[3][3] * rhs[3][2])
    tmp[3][3] = (mtx[3][0] * rhs[0][3]) + (mtx[3][1] * rhs[1][3]) + (mtx[3][2] * rhs[2][3]) + (mtx[3][3] * rhs[3][3])

    return tmp

def mat44Rotate(noeMat44, degrees, rotAngles):
    logger.logNotImplementedMethod('mat44Rotate', locals())

def mat44Sub(noeMat44, other):
    logger.logNotImplementedMethod('mat44Sub', locals())

def mat44SwapHandedness(noeMat44, axis):
    logger.logNotImplementedMethod('mat44SwapHandedness', locals())

def mat44ToBytes(noeMat44):
    logger.logNotImplementedMethod('mat44ToBytes', locals())

def mat44ToMat43(noeMat44):
    tmp = inc_noesis.NoeMat43()

    tmp[0][0] = noeMat44[0][0]
    tmp[0][1] = noeMat44[0][1]
    tmp[0][2] = noeMat44[0][2]
    tmp[1][0] = noeMat44[1][0]
    tmp[1][1] = noeMat44[1][1]
    tmp[1][2] = noeMat44[1][2]
    tmp[2][0] = noeMat44[2][0]
    tmp[2][1] = noeMat44[2][1]
    tmp[2][2] = noeMat44[2][2]
    tmp[3][0] = noeMat44[3][0]
    tmp[3][1] = noeMat44[3][1]
    tmp[3][2] = noeMat44[3][2]

    return tmp

def mat44TransformVec4(noeMat44, other):
    logger.logNotImplementedMethod('mat44TransformVec4', locals())

def mat44Translate(noeMat44, trnVector):
    logger.logNotImplementedMethod('mat44Translate', locals())

def mat44Transpose(noeMat44):
    logger.logNotImplementedMethod('mat44Transpose', locals())

def mat44Validate(noeMat44):
    mat44 = noeMat44.mat44

    if len(mat44) != 4:
        doException("mat44Validate: validate failed")

    for vec in mat44:
        vec4Validate(vec)

def quat3FromBytes(otherBytes, bigEnd):
    logger.logNotImplementedMethod('quat3FromBytes', locals())

def quat3ToBytes(noeQuat3):
    logger.logNotImplementedMethod('quat3ToBytes', locals())

def quat3ToQuat(noeQuat3):
    logger.logNotImplementedMethod('quat3ToQuat', locals())

def quat3Validate(noeQuat3):
    vec3Validate(noeQuat3)

def quatAdd(noeQuat, other):
    logger.logNotImplementedMethod('quatAdd', locals())

def quatFromBytes(otherBytes, bigEnd):
    logger.logNotImplementedMethod('quatFromBytes', locals())

def quatLen(noeQuat):
    logger.logNotImplementedMethod('quatLen', locals())

def quatLerp(noeQuat, other, fraction):
    logger.logNotImplementedMethod('quatLerp', locals())

def quatMul(noeQuat, other):
    logger.logNotImplementedMethod('quatMul', locals())

def quatNormalize(noeQuat):
    logger.logNotImplementedMethod('quatNormalize', locals())

def quatSLerp(noeQuat, other, fraction):
    logger.logNotImplementedMethod('quatSLerp', locals())

def quatSub(noeQuat, other):
    logger.logNotImplementedMethod('quatSub', locals())

def quatToAngles(noeQuat):
    logger.logNotImplementedMethod('quatToAngles', locals())

def quatToBytes(noeQuat):
    logger.logNotImplementedMethod('quatToBytes', locals())

def quatToMat43(noeQuat, transposed):
    logger.logNotImplementedMethod('quatToMat43', locals())

def quatToQuat3(noeQuat):
    logger.logNotImplementedMethod('quatToQuat3', locals())

def quatTransformNormal(noeQuat, other):
    logger.logNotImplementedMethod('quatTransformNormal', locals())

def quatTransformPoint(noeQuat, other):
    logger.logNotImplementedMethod('quatTransformPoint', locals())

def quatTranspose(noeQuat):
    logger.logNotImplementedMethod('quatTranspose', locals())

def quatValidate(noeQuat):
    quat = noeVec4.quat

    validateListType(quat, Number)

    if len(quat) != 4:
        doException("quatValidate: validation failed")

def validateListType(list, types):
    for obj in list:
        if not isinstance(obj, types):
            doException("validateListType: validation failed")

def vec3Add(noeVec3, other):
    logger.logNotImplementedMethod('vec3Add', locals())

def vec3Cross(noeVec3, other):
    logger.logNotImplementedMethod('vec3Cross', locals())

def vec3Div(noeVec3, other):
    logger.logNotImplementedMethod('vec3Div', locals())

def vec3FromBytes(otherBytes, bigEnd):
    logger.logNotImplementedMethod('vec3FromBytes', locals())

def vec3Len(noeVec3):
    logger.logNotImplementedMethod('vec3Len', locals())

def vec3LenSq(noeVec3):
    logger.logNotImplementedMethod('vec3LenSq', locals())

def vec3Lerp(noeVec3, other, fraction):
    logger.logNotImplementedMethod('vec3Lerp', locals())

def vec3Mul(noeVec3, other):
    logger.logNotImplementedMethod('vec3Mul', locals())

def vec3Norm(noeVec3):
    logger.logNotImplementedMethod('vec3Norm', locals())

def vec3Sub(noeVec3, other):
    logger.logNotImplementedMethod('vec3Sub', locals())

def vec3ToAngles(noeVec3):
    logger.logNotImplementedMethod('vec3ToAngles', locals())

def vec3ToBytes(noeVec3):
    logger.logNotImplementedMethod('vec3ToBytes', locals())

def vec3ToMat43(noeVec3):
    logger.logNotImplementedMethod('vec3ToMat43', locals())

def vec3ToVec4(noeVec3):
    logger.logNotImplementedMethod('vec3ToVec4', locals())

def vec3Validate(noeVec3):
    vec3 = noeVec3.vec3

    if len(vec3) != 3:
        doException("vec3Validate: validate failed")

    validateListType(vec3, Number)

def vec4Add(noeVec4, other):
    logger.logNotImplementedMethod('vec4Add', locals())

def vec4Div(noeVec4, other):
    logger.logNotImplementedMethod('vec4Div', locals())

def vec4Dot(noeVec4, other):
    logger.logNotImplementedMethod('vec4Dot', locals())

def vec4FromBytes(otherBytes, bigEnd):
    logger.logNotImplementedMethod('vec4FromBytes', locals())

def vec4Len(noeVec4):
    logger.logNotImplementedMethod('vec4Len', locals())

def vec4LenSq(noeVec4):
    logger.logNotImplementedMethod('vec4LenSq', locals())

def vec4Lerp(noeVec4, other, fraction):
    logger.logNotImplementedMethod('vec4Lerp', locals())

def vec4Mul(noeVec4, other):
    logger.logNotImplementedMethod('vec4Mul', locals())

def vec4Norm(noeVec4):
    logger.logNotImplementedMethod('vec4Norm', locals())

def vec4Sub(noeVec4, other):
    logger.logNotImplementedMethod('vec4Sub', locals())

def vec4ToBytes(noeVec4):
    logger.logNotImplementedMethod('vec4ToBytes', locals())

def vec4ToVec3(noeVec4):
    logger.logNotImplementedMethod('vec4ToVec3', locals())

def vec4Validate(noeVec4):
    vec4 = noeVec4.vec4

    validateListType(vec4, Number)

    if len(vec4) != 4:
        doException("vec4Validate: validation failed")

import inc_noesis
