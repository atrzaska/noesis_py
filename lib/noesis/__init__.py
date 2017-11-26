from Handler import Handler
from NoeModule import NoeModule
from AllocType import AllocType
from numbers import Number
import sys

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
    # TODO: implement me
    print("Not implemented method called: freeModule")

def getCharSplineSet():
    # TODO: implement me
    print("Not implemented method called: getCharSplineSet")

def getFormatExtensionFlags():
    # TODO: implement me
    print("Not implemented method called: getFormatExtensionFlags")

def getMFFP(uint):
    # TODO: implement me
    print("Not implemented method called: getMFFP")

def getScenesPath():
    # TODO: implement me
    print("Not implemented method called: getScenesPath")

def getSelectedDirectory():
    # TODO: implement me
    print("Not implemented method called: getSelectedDirectory")

def getSelectedFile():
    # TODO: implement me
    print("Not implemented method called: getSelectedFile")

def getWindowHandle():
    # TODO: implement me
    print("Not implemented method called: getWindowHandle")

def instantiateModule():
    module = NoeModule()
    this.modules.append(module)
    return module

def isPreviewModuleRAPIValid():
    # TODO: implement me
    print("Not implemented method called: isPreviewModuleRAPIValid")

def loadImageRGBA():
    # TODO: implement me
    print("Not implemented method called: loadImageRGBA")

def logPopup():
    # this should open the debug window
    pass

def messagePrompt():
    # TODO: implement me
    print("Not implemented method called: messagePrompt")

def openAndRemoveTempFile():
    # TODO: implement me
    print("Not implemented method called: openAndRemoveTempFile")

def openFile():
    # TODO: implement me
    print("Not implemented method called: openFile")

def optGetArg():
    # TODO: implement me
    print("Not implemented method called: optGetArg")

def optWasInvoked():
    # TODO: implement me
    print("Not implemented method called: optWasInvoked")

# TODO: fileType can be semicolon separated '.obj;.obc'
def register(name, fileType):
    handler = Handler(name, fileType)
    this.plugins.append(handler)
    return handler

def registerCleanupFunction():
    # TODO: implement me
    print("Not implemented method called: registerCleanupFunction")

def registerTool():
    # TODO: implement me
    print("Not implemented method called: registerTool")

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
    # TODO: implement me
    print("Not implemented method called: setModuleRAPI")

def setPreviewModuleRAPI():
    # TODO: implement me
    print("Not implemented method called: setPreviewModuleRAPI")

def setToolFlags():
    # TODO: implement me
    print("Not implemented method called: setToolFlags")

def setToolVisibleCallback():
    # TODO: implement me
    print("Not implemented method called: setToolVisibleCallback")

def userPrompt():
    # TODO: implement me
    print("Not implemented method called: userPrompt")

# inc_noesis methods

def allocType(name, data = None):
    return AllocType(name, data)

def anglesALerp(noeAngles, other, degrees):
    # TODO: implement me
    print("Not implemented method called: anglesALerp")

def anglesAngleVectors(noeAngles):
    # TODO: implement me
    print("Not implemented method called: anglesAngleVectors")

def anglesMod(noeAngles, f):
    # TODO: implement me
    print("Not implemented method called: anglesMod")

def anglesNormalize180(noeAngles):
    # TODO: implement me
    print("Not implemented method called: anglesNormalize180")

def anglesNormalize360(noeAngles):
    # TODO: implement me
    print("Not implemented method called: anglesNormalize360")

def anglesToMat43_XYZ(noeAngles, yFlip):
    # TODO: implement me
    print("Not implemented method called: anglesToMat43_XYZ")

def anglesToMat43(noeAngles):
    # TODO: implement me
    print("Not implemented method called: anglesToMat43")

def anglesToQuat(noeAngles):
    # TODO: implement me
    print("Not implemented method called: anglesToQuat")

def anglesToVec3(noeAngles):
    # TODO: implement me
    print("Not implemented method called: anglesToVec3")

def anglesValidate(noeAngles):
    # TODO: implement me
    print("Not implemented method called: anglesValidate")

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
    # TODO: implement me
    print("Not implemented method called: cubicBezier3D")

def doException(name):
    raise ValueError(name)

def encodeFloat16(val):
    # TODO: implement me
    print("Not implemented method called: encodeFloat16")

def getFloat16(ushort):
    # TODO: implement me
    print("Not implemented method called: getFloat16")

def mat43Add(noeMat43, other):
    # TODO: implement me
    print("Not implemented method called: mat43Add")

def mat43FromBytes(otherBytes, bigEnd):
    # TODO: implement me
    print("Not implemented method called: mat43FromBytes")

def mat43Inverse(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43Inverse")

def mat43IsSkewed(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43IsSkewed")

def mat43Lerp(noeMat43, other, fraction):
    # TODO: implement me
    print("Not implemented method called: mat43Lerp")

def mat43Mul(noeMat43, other):
    # TODO: implement me
    print("Not implemented method called: mat43Mul")

def mat43Orthogonalize(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43Orthogonalize")

def mat43Rotate(noeMat43, degrees, rotAngles, transposeRot):
    # TODO: implement me
    print("Not implemented method called: mat43Rotate")

def mat43SLerp(noeMat43, other, fraction):
    # TODO: implement me
    print("Not implemented method called: mat43SLerp")

def mat43Sub(noeMat43, other):
    # TODO: implement me
    print("Not implemented method called: mat43Sub")

def mat43SwapHandedness(noeMat43, axis):
    # TODO: implement me
    print("Not implemented method called: mat43SwapHandedness")

def mat43ToAngles(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43ToAngles")

def mat43ToBytes(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43ToBytes")

def mat43ToMat44(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43ToMat44")

def mat43ToQuat(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43ToQuat")

def mat43TransformNormal(noeMat43, other):
    # TODO: implement me
    print("Not implemented method called: mat43TransformNormal")

def mat43TransformPoint(noeMat43, other):
    # TODO: implement me
    print("Not implemented method called: mat43TransformPoint")

def mat43TransformVec4(noeMat43, other):
    # TODO: implement me
    print("Not implemented method called: mat43TransformVec4")

def mat43Translate(noeMat43, trnVector):
    # TODO: implement me
    print("Not implemented method called: mat43Translate")

def mat43Transpose(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43Transpose")

def mat43Validate(noeMat43):
    # TODO: implement me
    print("Not implemented method called: mat43Validate")

def mat44Add(noeMat44, other):
    # TODO: implement me
    print("Not implemented method called: mat44Add")

def mat44FromBytes(otherBytes, bigEnd):
    # TODO: implement me
    print("Not implemented method called: mat44FromBytes")

def mat44Inverse(noeMat44):
    # TODO: implement me
    print("Not implemented method called: mat44Inverse")

def mat44Mul(noeMat44, other):
    # TODO: implement me
    print("Not implemented method called: mat44Mul")

def mat44Rotate(noeMat44, degrees, rotAngles):
    # TODO: implement me
    print("Not implemented method called: mat44Rotate")

def mat44Sub(noeMat44, other):
    # TODO: implement me
    print("Not implemented method called: mat44Sub")

def mat44SwapHandedness(noeMat44, axis):
    # TODO: implement me
    print("Not implemented method called: mat44SwapHandedness")

def mat44ToBytes(noeMat44):
    # TODO: implement me
    print("Not implemented method called: mat44ToBytes")

def mat44ToMat43(noeMat44):
    # TODO: implement me
    print("Not implemented method called: mat44ToMat43")

def mat44TransformVec4(noeMat44, other):
    # TODO: implement me
    print("Not implemented method called: mat44TransformVec4")

def mat44Translate(noeMat44, trnVector):
    # TODO: implement me
    print("Not implemented method called: mat44Translate")

def mat44Transpose(noeMat44):
    # TODO: implement me
    print("Not implemented method called: mat44Transpose")

def mat44Validate(noeMat44):
    # TODO: implement me
    print("Not implemented method called: mat44Validate")

def quat3FromBytes(otherBytes, bigEnd):
    # TODO: implement me
    print("Not implemented method called: quat3FromBytes")

def quat3ToBytes(noeQuat3):
    # TODO: implement me
    print("Not implemented method called: quat3ToBytes")

def quat3ToQuat(noeQuat3):
    # TODO: implement me
    print("Not implemented method called: quat3ToQuat")

def quat3Validate(noeQuat3):
    # TODO: implement me
    print("Not implemented method called: quat3Validate")

def quatAdd(noeQuat, other):
    # TODO: implement me
    print("Not implemented method called: quatAdd")

def quatFromBytes(otherBytes, bigEnd):
    # TODO: implement me
    print("Not implemented method called: quatFromBytes")

def quatLen(noeQuat):
    # TODO: implement me
    print("Not implemented method called: quatLen")

def quatLerp(noeQuat, other, fraction):
    # TODO: implement me
    print("Not implemented method called: quatLerp")

def quatMul(noeQuat, other):
    # TODO: implement me
    print("Not implemented method called: quatMul")

def quatNormalize(noeQuat):
    # TODO: implement me
    print("Not implemented method called: quatNormalize")

def quatSLerp(noeQuat, other, fraction):
    # TODO: implement me
    print("Not implemented method called: quatSLerp")

def quatSub(noeQuat, other):
    # TODO: implement me
    print("Not implemented method called: quatSub")

def quatToAngles(noeQuat):
    # TODO: implement me
    print("Not implemented method called: quatToAngles")

def quatToBytes(noeQuat):
    # TODO: implement me
    print("Not implemented method called: quatToBytes")

def quatToMat43(noeQuat, transposed):
    # TODO: implement me
    print("Not implemented method called: quatToMat43")

def quatToQuat3(noeQuat):
    # TODO: implement me
    print("Not implemented method called: quatToQuat3")

def quatTransformNormal(noeQuat, other):
    # TODO: implement me
    print("Not implemented method called: quatTransformNormal")

def quatTransformPoint(noeQuat, other):
    # TODO: implement me
    print("Not implemented method called: quatTransformPoint")

def quatTranspose(noeQuat):
    # TODO: implement me
    print("Not implemented method called: quatTranspose")

def quatValidate(noeQuat):
    # TODO: implement me
    print("Not implemented method called: quatValidate")

def validateListType(list, types):
    # TODO: implement me
    print("Not implemented method called: validateListType")

def vec3Add(noeVec3, other):
    # TODO: implement me
    print("Not implemented method called: vec3Add")

def vec3Cross(noeVec3, other):
    # TODO: implement me
    print("Not implemented method called: vec3Cross")

def vec3Div(noeVec3, other):
    # TODO: implement me
    print("Not implemented method called: vec3Div")

def vec3FromBytes(otherBytes, bigEnd):
    # TODO: implement me
    print("Not implemented method called: vec3FromBytes")

def vec3Len(noeVec3):
    # TODO: implement me
    print("Not implemented method called: vec3Len")

def vec3LenSq(noeVec3):
    # TODO: implement me
    print("Not implemented method called: vec3LenSq")

def vec3Lerp(noeVec3, other, fraction):
    # TODO: implement me
    print("Not implemented method called: vec3Lerp")

def vec3Mul(noeVec3, other):
    # TODO: implement me
    print("Not implemented method called: vec3Mul")

def vec3Norm(noeVec3):
    # TODO: implement me
    print("Not implemented method called: vec3Norm")

def vec3Sub(noeVec3, other):
    # TODO: implement me
    print("Not implemented method called: vec3Sub")

def vec3ToAngles(noeVec3):
    # TODO: implement me
    print("Not implemented method called: vec3ToAngles")

def vec3ToBytes(noeVec3):
    # TODO: implement me
    print("Not implemented method called: vec3ToBytes")

def vec3ToMat43(noeVec3):
    # TODO: implement me
    print("Not implemented method called: vec3ToMat43")

def vec3ToVec4(noeVec3):
    # TODO: implement me
    print("Not implemented method called: vec3ToVec4")

def vec3Validate(noeVec3):
    vec3 = noeVec3.vec3

    if len(vec3) != 3:
        doException("Vector not valid")
    if not isinstance(vec3[0], Number):
        doException("Vector not valid")
    if not isinstance(vec3[1], Number):
        doException("Vector not valid")
    if not isinstance(vec3[2], Number):
        doException("Vector not valid")

def vec4Add(noeVec4, other):
    # TODO: implement me
    print("Not implemented method called: vec4Add")

def vec4Div(noeVec4, other):
    # TODO: implement me
    print("Not implemented method called: vec4Div")

def vec4Dot(noeVec4, other):
    # TODO: implement me
    print("Not implemented method called: vec4Dot")

def vec4FromBytes(otherBytes, bigEnd):
    # TODO: implement me
    print("Not implemented method called: vec4FromBytes")

def vec4Len(noeVec4):
    # TODO: implement me
    print("Not implemented method called: vec4Len")

def vec4LenSq(noeVec4):
    # TODO: implement me
    print("Not implemented method called: vec4LenSq")

def vec4Lerp(noeVec4, other, fraction):
    # TODO: implement me
    print("Not implemented method called: vec4Lerp")

def vec4Mul(noeVec4, other):
    # TODO: implement me
    print("Not implemented method called: vec4Mul")

def vec4Norm(noeVec4):
    # TODO: implement me
    print("Not implemented method called: vec4Norm")

def vec4Sub(noeVec4, other):
    # TODO: implement me
    print("Not implemented method called: vec4Sub")

def vec4ToBytes(noeVec4):
    # TODO: implement me
    print("Not implemented method called: vec4ToBytes")

def vec4ToVec3(noeVec4):
    # TODO: implement me
    print("Not implemented method called: vec4ToVec3")

def vec4Validate(noeVec4):
    vec4 = noeVec4.vec4

    if len(vec4) != 4:
        doException("Vector not valid")
    if not isinstance(vec4[0], Number):
        doException("Vector not valid")
    if not isinstance(vec4[1], Number):
        doException("Vector not valid")
    if not isinstance(vec4[2], Number):
        doException("Vector not valid")
    if not isinstance(vec4[3], Number):
        doException("Vector not valid")
