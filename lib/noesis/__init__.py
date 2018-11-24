import sys
import struct
import math
from Handler import Handler
from NoeModule import NoeModule
from AllocType import AllocType
from numbers import Number
from util import logNotImplementedMethod

# constants

BITSTREAMFL_BIGENDIAN = 65536
BITSTREAMFL_DESCENDINGBITS = 131072
BITSTREAMFL_USERFLAG1 = 16777216
BITSTREAMFL_USERFLAG2 = 33554432
BITSTREAMFL_USERFLAG3 = 67108864
BITSTREAMFL_USERFLAG4 = 134217728
BITSTREAMFL_USERFLAG5 = 268435456
BITSTREAMFL_USERFLAG6 = 536870912
BITSTREAMFL_USERFLAG7 = 1073741824
BITSTREAMFL_USERFLAG8 = -2147483648
BLITFLAG_ALPHABLEND = 1
BONEFLAG_DECOMPLERP = 8
BONEFLAG_DIRECTLERP = 2
BONEFLAG_NOLERP = 4
BONEFLAG_ORTHOLERP = 1
DECODEFLAG_PS2SHIFT = 1
FOURCC_ATI1 = 826889281
FOURCC_ATI2 = 843666497
FOURCC_BC1 = 827611204
FOURCC_BC2 = 861165636
FOURCC_BC3 = 894720068
FOURCC_BC4 = 826889281
FOURCC_BC5 = 843666497
FOURCC_BC6H = 1211515714
FOURCC_BC6S = 1396065090
FOURCC_BC7 = 1480016706
FOURCC_DX10 = 808540228
FOURCC_DXT1 = 827611204
FOURCC_DXT1NORMAL = 1311855684
FOURCC_DXT3 = 861165636
FOURCC_DXT5 = 894720068
g_flDegToRad = 0.01745329238474369
g_flPI = 3.1415927410125732
g_flRadToDeg = 57.2957763671875
MAX_NOESIS_PATH = 4096
NANIMFLAG_FORCENAMEMATCH = 1
NANIMFLAG_INVALIDHIERARCHY = 2
NFORMATFLAG_ANIMWRITE = 32
NFORMATFLAG_ARCREAD = 1
NFORMATFLAG_IMGREAD = 2
NFORMATFLAG_IMGWRITE = 4
NFORMATFLAG_MODELREAD = 8
NFORMATFLAG_MODELWRITE = 16
NMATFLAG_BLENDEDNORMALS = 16
NMATFLAG_ENV_FLIP = 1048576
NMATFLAG_GAMMACORRECT = 8192
NMATFLAG_KAJIYAKAY = 32
NMATFLAG_NMAPSWAPRA = 1
NMATFLAG_NORMAL_UV1 = 33554432
NMATFLAG_NORMALMAP_FLIPY = 131072
NMATFLAG_NORMALMAP_NODERZ = 262144
NMATFLAG_PBR_ALBEDOENERGYCON = 4194304
NMATFLAG_PBR_COMPENERGYCON = 8388608
NMATFLAG_PBR_METAL = 65536
NMATFLAG_PBR_ROUGHNESS_NRMALPHA = 536870912
NMATFLAG_PBR_SPEC = 32768
NMATFLAG_PBR_SPEC_IR_RG = 524288
NMATFLAG_PREVIEWLOAD = 4
NMATFLAG_SORT01 = 64
NMATFLAG_SPEC_UV1 = 67108864
NMATFLAG_SPRITE_FACINGXY = 16777216
NMATFLAG_TWOSIDED = 2
NMATFLAG_USELMUVS = 8
NMATFLAG_VCOLORSUBTRACT = 16384
NMSHAREDFL_BONEPALETTE = 1024
NMSHAREDFL_FLATWEIGHTS = 8
NMSHAREDFL_FLATWEIGHTS_FORCE4 = 16
NMSHAREDFL_REVERSEWINDING = 32
NMSHAREDFL_UNIQUEVERTS = 256
NMSHAREDFL_WANTGLOBALARRAY = 2
NMSHAREDFL_WANTNEIGHBORS = 1
NMSHAREDFL_WANTTANGENTS = 4
NMSHAREDFL_WANTTANGENTS4 = 64
NMSHAREDFL_WANTTANGENTS4R = 128
NOE_ENCODEDXT_BC1 = 0
NOE_ENCODEDXT_BC3 = 1
NOE_ENCODEDXT_BC4 = 2
NOEBLEND_DST_ALPHA = 7
NOEBLEND_DST_COLOR = 9
NOEBLEND_NONE = 0
NOEBLEND_ONE = 2
NOEBLEND_ONE_MINUS_DST_ALPHA = 8
NOEBLEND_ONE_MINUS_DST_COLOR = 10
NOEBLEND_ONE_MINUS_SRC_ALPHA = 6
NOEBLEND_ONE_MINUS_SRC_COLOR = 4
NOEBLEND_SRC_ALPHA = 5
NOEBLEND_SRC_ALPHA_SATURATE = 11
NOEBLEND_SRC_COLOR = 3
NOEBLEND_ZERO = 1
NOEFSMODE_READBINARY = 0
NOEFSMODE_READWRITEBINARY = 2
NOEFSMODE_WRITEBINARY = 1
NOEKF_INTERPOLATE_LINEAR = 0
NOEKF_INTERPOLATE_NEAREST = 1
NOEKF_ROTATION_QUATERNION_4 = 0
NOEKF_SCALE_SCALAR_1 = 0
NOEKF_SCALE_SINGLE = 1
NOEKF_SCALE_TRANSPOSED_VECTOR_3 = 3
NOEKF_SCALE_VECTOR_3 = 2
NOEKF_TRANSLATION_SINGLE = 1
NOEKF_TRANSLATION_VECTOR_3 = 0
NOESIS_PLUGIN_VERSION = 3
NOESIS_PLUGINAPI_VERSION = 73
NOESISTEX_DXT1 = 3
NOESISTEX_DXT3 = 4
NOESISTEX_DXT5 = 5
NOESISTEX_RGB24 = 2
NOESISTEX_RGBA32 = 1
NOESISTEX_UNKNOWN = 0
NOESPLINEFLAG_CLOSED = 1
NOEUSERVAL_BOOL = 4
NOEUSERVAL_FILEPATH = 5
NOEUSERVAL_FLOAT = 2
NOEUSERVAL_FOLDERPATH = 6
NOEUSERVAL_INT = 3
NOEUSERVAL_NONE = 0
NOEUSERVAL_SAVEFILEPATH = 7
NOEUSERVAL_STRING = 1
NSEQFLAG_NONLOOPING = 1
NSEQFLAG_REVERSE = 2
NTEXFLAG_CUBEMAP = 256
NTEXFLAG_FILTER_NEAREST = 16
NTEXFLAG_HDRISLINEAR = 2048
NTEXFLAG_ISLINEAR = 1024
NTEXFLAG_ISNORMALMAP = 1
NTEXFLAG_PREVIEWLOAD = 128
NTEXFLAG_SEGMENTED = 2
NTEXFLAG_STEREO = 4
NTEXFLAG_STEREO_SWAP = 8
NTEXFLAG_WANTSEAMLESS = 4096
NTEXFLAG_WRAP_CLAMP = 32
NTEXFLAG_WRAP_MIRROR_CLAMP = 16384
NTEXFLAG_WRAP_MIRROR_REPEAT = 8192
NTEXFLAG_WRAP_REPEAT = 0
NTOOLFLAG_CONTEXTITEM = 1
NTOOLFLAG_USERBITS = -268435456
NUM_NOE_BLENDS = 12
NUM_NOEKF_INTERPOLATION_TYPES = 2
NUM_NOEKF_ROTATION_TYPES = 1
NUM_NOEKF_SCALE_TYPES = 4
NUM_NOEKF_TRANSLATION_TYPES = 2
NUM_RPGEO_DATATYPES = 9
NUM_RPGEO_TYPES = 12
OPTFLAG_WANTARG = 1
PS2_VIFCODE_BASE = 3
PS2_VIFCODE_DIRECT = 80
PS2_VIFCODE_DIRECTHL = 81
PS2_VIFCODE_FLUSH = 17
PS2_VIFCODE_FLUSHA = 19
PS2_VIFCODE_FLUSHE = 16
PS2_VIFCODE_ITOP = 4
PS2_VIFCODE_MARK = 7
PS2_VIFCODE_MPG = 74
PS2_VIFCODE_MSCAL = 20
PS2_VIFCODE_MSCALF = 21
PS2_VIFCODE_MSCNT = 23
PS2_VIFCODE_MSKPATH3 = 6
PS2_VIFCODE_NOP = 0
PS2_VIFCODE_OFFSET = 2
PS2_VIFCODE_STCOL = 49
PS2_VIFCODE_STCYCL = 1
PS2_VIFCODE_STMASK = 32
PS2_VIFCODE_STMOD = 5
PS2_VIFCODE_STROW = 48
PVRTC_DECODE_BICUBIC = 4
PVRTC_DECODE_LINEARORDER = 2
PVRTC_DECODE_PVRTC2 = 1
PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA = 16
PVRTC_DECODE_PVRTC2_ROTATE_BLOCK_PAL = 8
RPGEO_NONE = 0
RPGEO_POINTS = 1
RPGEO_POLYGON = 5
RPGEO_QUAD = 4
RPGEO_QUAD_ABC_ACD = 10
RPGEO_QUAD_ABC_BCD = 9
RPGEO_QUAD_ABC_DCA = 11
RPGEO_QUAD_STRIP = 7
RPGEO_TRIANGLE = 2
RPGEO_TRIANGLE_FAN = 6
RPGEO_TRIANGLE_STRIP = 3
RPGEO_TRIANGLE_STRIP_FLIPPED = 8
RPGEODATA_BYTE = 7
RPGEODATA_DOUBLE = 6
RPGEODATA_FLOAT = 0
RPGEODATA_HALFFLOAT = 5
RPGEODATA_INT = 1
RPGEODATA_SHORT = 3
RPGEODATA_UBYTE = 8
RPGEODATA_UINT = 2
RPGEODATA_USHORT = 4
RPGOPT_BIGENDIAN = 1
RPGOPT_DERIVEBONEORIS = 8
RPGOPT_FILLINWEIGHTS = 16
RPGOPT_MORPH_RELATIVENORMALS = 256
RPGOPT_MORPH_RELATIVEPOSITIONS = 128
RPGOPT_SWAPHANDEDNESS = 32
RPGOPT_TANMATROTATE = 4
RPGOPT_TRIWINDBACKWARD = 2
RPGOPT_UNSAFE = 64
RPGVUFLAG_NOREUSE = 2
RPGVUFLAG_PERINSTANCE = 1
SHAREDSTRIP_LIST = 0
SHAREDSTRIP_STRIP = 1

# state

this = sys.modules[__name__]
this.plugins = []
this.this.modules = []

def addOption(handle, option, description, flags):
    return handle.addOption(option, description, flags)

def allocBytes(size):
    return bytearray(size)

def allocType(name, data = None):
    return AllocType(name, data)

def anglesALerp(noeAngles, other, degrees):
    logNotImplementedMethod('anglesALerp', locals())

def anglesAngleVectors(noeAngles):
    logNotImplementedMethod('anglesAngleVectors', locals())
    return inc_noesis.NoeMat43()

def anglesMod(noeAngles, f):
    logNotImplementedMethod('anglesMod', locals())

def anglesNormalize180(noeAngles):
    x = noeAngles[0] % 180
    y = noeAngles[1] % 180
    z = noeAngles[2] % 180
    return inc_noesis.NoeAngles((x, y, z))

def anglesNormalize360(noeAngles):
    x = noeAngles[0] % 360
    y = noeAngles[1] % 360
    z = noeAngles[2] % 360
    return inc_noesis.NoeAngles((x, y, z))

def anglesToMat43(noeAngles):
    logNotImplementedMethod('anglesToMat43', locals())
    return inc_noesis.NoeMat43()

def anglesToMat43_XYZ(noeAngles, yFlip):
    logNotImplementedMethod('anglesToMat43_XYZ', locals())
    return inc_noesis.NoeMat43()

def anglesToQuat(noeAngles):
    logNotImplementedMethod('anglesToQuat', locals())
    return inc_noesis.NoeQuat()

def anglesToVec3(noeAngles):
    logNotImplementedMethod('anglesToVec3', locals())
    return inc_noesis.NoeVec3()

def anglesValidate(noeAngles):
    vec3Validate(noeAngles)

def bezier3D(*args):
    logNotImplementedMethod('bezier3D', locals())

def bezierTangent3D(*args):
    logNotImplementedMethod('bezierTangent3D', locals())

def bilinLerp(*args):
    logNotImplementedMethod('bilinLerp', locals())

def bsGetBuffer(handle):
    return handle.bsGetBuffer()

def bsGetBufferSlice(handle, start, end):
    return handle.bsGetBufferSlice(start, end)

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

def checkToolMenuItem(*args):
    logNotImplementedMethod('checkToolMenuItem', locals())

def constLerp(*args):
    logNotImplementedMethod('constLerp', locals())

def cubicBezier3D(points, frac):
    logNotImplementedMethod('cubicBezier3D', locals())

def cubicLerp(*args):
    logNotImplementedMethod('cubicLerp', locals())

def deinterleaveBytes(*args):
    logNotImplementedMethod('deinterleaveBytes', locals())

def disableFormatByDescription(*args):
    logNotImplementedMethod('disableFormatByDescription', locals())

def doException(name):
    raise ValueError(name)

def encodeFloat16(val):
    F16_EXPONENT_BITS = 0x1F
    F16_EXPONENT_SHIFT = 10
    F16_EXPONENT_BIAS = 15
    F16_MANTISSA_BITS = 0x3ff
    F16_MANTISSA_SHIFT =  (23 - F16_EXPONENT_SHIFT)
    F16_MAX_EXPONENT =  (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

    a = struct.pack('>f', val)
    b = binascii.hexlify(a)
    f32 = int(b, 16)
    f16 = 0
    sign = (f32 >> 16) & 0x8000
    exponent = ((f32 >> 23) & 0xff) - 127
    mantissa = f32 & 0x007fffff

    if exponent == 128:
        f16 = sign | F16_MAX_EXPONENT
        if mantissa:
            f16 |= (mantissa & F16_MANTISSA_BITS)
    elif exponent > 15:
        f16 = sign | F16_MAX_EXPONENT
    elif exponent > -15:
        exponent += F16_EXPONENT_BIAS
        mantissa >>= F16_MANTISSA_SHIFT
        f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
    else:
        f16 = sign
    return f16

def encodeMFFP(*args):
    logNotImplementedMethod('encodeMFFP', locals())

def fileIsLoadable(*args):
    logNotImplementedMethod('fileIsLoadable', locals())

def freeModule(module):
    logNotImplementedMethod('freeModule', locals())

def getAPIVersion(*args):
    logNotImplementedMethod('getAPIVersion', locals())

def getCharSplineSet(char):
    logNotImplementedMethod('getCharSplineSet', locals())

def getFloat16(ushort):
    s = int((ushort >> 15) & 0x00000001)    # sign
    e = int((ushort >> 10) & 0x0000001f)    # exponent
    f = int(ushort & 0x000003ff)            # fraction

    if e == 0:
        if f == 0:
            return int(s << 31)
        else:
            while not (f & 0x00000400):
                f = f << 1
                e -= 1
            e += 1
            f &= ~0x00000400
    elif e == 31:
        if f == 0:
            return int((s << 31) | 0x7f800000)
        else:
            return int((s << 31) | 0x7f800000 | (f << 13))

    e = e + (127 -15)
    f = f << 13
    temp = int((s << 31) | (e << 23) | f)
    packed = struct.pack('I', temp)
    return struct.unpack('f', packed)[0]

def getFormatExtensionFlags(extension):
    logNotImplementedMethod('getFormatExtensionFlags', locals())

def getMainPath(*args):
    logNotImplementedMethod('getMainPath', locals())

def getMFFP(uint):
    logNotImplementedMethod('getMFFP', locals())

def getOpenPreviewFile(*args):
    logNotImplementedMethod('getOpenPreviewFile', locals())

def getPluginsPath(*args):
    logNotImplementedMethod('getPluginsPath', locals())

def getScenesPath():
    logNotImplementedMethod('getScenesPath', locals())

def getSelectedDirectory():
    logNotImplementedMethod('getSelectedDirectory', locals())

def getSelectedFile():
    logNotImplementedMethod('getSelectedFile', locals())

def getToolFlags(*args):
    logNotImplementedMethod('getToolFlags', locals())

def getWindowHandle():
    logNotImplementedMethod('getWindowHandle', locals())

def hermiteLerp(*args):
    logNotImplementedMethod('hermiteLerp', locals())

def instantiateModule():
    module = NoeModule()
    this.modules.append(module)
    return module

def isPreviewModuleRAPIValid():
    logNotImplementedMethod('isPreviewModuleRAPIValid', locals())

def linLerp(*args):
    logNotImplementedMethod('linLerp', locals())

def loadImageRGBA(path):
    logNotImplementedMethod('loadImageRGBA', locals())

def logError(*args):
    logNotImplementedMethod('logError', locals())

def logFlush(*args):
    logNotImplementedMethod('logFlush', locals())

def logOutput(*args):
    logNotImplementedMethod('logOutput', locals())

def logPopup():
    # this should open the debug window, but we're just using console output
    pass

def mat43Add(noeMat43, other):
    m00 = noeMat43[0][0] + other[0][0]
    m01 = noeMat43[0][1] + other[0][1]
    m02 = noeMat43[0][2] + other[0][2]
    m10 = noeMat43[1][0] + other[1][0]
    m11 = noeMat43[1][1] + other[1][1]
    m12 = noeMat43[1][2] + other[1][2]
    m20 = noeMat43[2][0] + other[2][0]
    m21 = noeMat43[2][1] + other[2][1]
    m22 = noeMat43[2][2] + other[2][2]
    m30 = noeMat43[3][0] + other[3][0]
    m31 = noeMat43[3][1] + other[3][1]
    m32 = noeMat43[3][2] + other[3][2]

    return inc_noesis.NoeMat43((
        inc_noesis.NoeVec3((m00, m01, m02)),
        inc_noesis.NoeVec3((m10, m11, m12)),
        inc_noesis.NoeVec3((m20, m21, m22)),
        inc_noesis.NoeVec3((m30, m31, m32))
    ))

def mat43FromBytes(data, bigEnd):
    logNotImplementedMethod('mat43FromBytes', locals())
    return inc_noesis.NoeMat43()

def mat43Inverse(noeMat43):
    # TODO: this logic gives wrong results
    return noeMat43.toMat44().inverse().toMat43()

def mat43IsSkewed(noeMat43):
    logNotImplementedMethod('mat43IsSkewed', locals())
    return 9999 # should be 0 or 1

def mat43Lerp(noeMat43, other, fraction):
    logNotImplementedMethod('mat43Lerp', locals())

def mat43Mul(noeMat43, other):
    return (noeMat43.toMat44() * other.toMat44()).toMat43()

def mat43Orthogonalize(noeMat43):
    logNotImplementedMethod('mat43Orthogonalize', locals())
    return noeMat43

def mat43Rotate(noeMat43, degrees, rotAngles, transposeRot):
    logNotImplementedMethod('mat43Rotate', locals())

def mat43SLerp(noeMat43, other, fraction):
    logNotImplementedMethod('mat43SLerp', locals())

def mat43Sub(noeMat43, other):
    m00 = noeMat43[0][0] - other[0][0]
    m01 = noeMat43[0][1] - other[0][1]
    m02 = noeMat43[0][2] - other[0][2]
    m10 = noeMat43[1][0] - other[1][0]
    m11 = noeMat43[1][1] - other[1][1]
    m12 = noeMat43[1][2] - other[1][2]
    m20 = noeMat43[2][0] - other[2][0]
    m21 = noeMat43[2][1] - other[2][1]
    m22 = noeMat43[2][2] - other[2][2]
    m30 = noeMat43[3][0] - other[3][0]
    m31 = noeMat43[3][1] - other[3][1]
    m32 = noeMat43[3][2] - other[3][2]

    return inc_noesis.NoeMat43((
        inc_noesis.NoeVec3((m00, m01, m02)),
        inc_noesis.NoeVec3((m10, m11, m12)),
        inc_noesis.NoeVec3((m20, m21, m22)),
        inc_noesis.NoeVec3((m30, m31, m32))
    ))

def mat43SwapHandedness(noeMat43, axis):
    logNotImplementedMethod('mat43SwapHandedness', locals())

def mat43ToAngles(noeMat43):
    logNotImplementedMethod('mat43ToAngles', locals())
    return inc_noesis.NoeAngles()

def mat43ToBytes(noeMat43):
    logNotImplementedMethod('mat43ToBytes', locals())

def mat43ToMat44(noeMat43):
    m00 = noeMat43[0][0]
    m01 = noeMat43[1][0]
    m02 = noeMat43[2][0]
    m03 = 0.0
    m10 = noeMat43[0][1]
    m11 = noeMat43[1][1]
    m12 = noeMat43[2][1]
    m13 = 0.0
    m20 = noeMat43[0][2]
    m21 = noeMat43[1][2]
    m22 = noeMat43[2][2]
    m23 = 0.0
    m30 = noeMat43[3][0]
    m31 = noeMat43[3][1]
    m32 = noeMat43[3][2]
    m33 = 1.0

    return inc_noesis.NoeMat44((
        inc_noesis.NoeVec4((m00, m01, m02, m03)),
        inc_noesis.NoeVec4((m10, m11, m12, m13)),
        inc_noesis.NoeVec4((m20, m21, m22, m23)),
        inc_noesis.NoeVec4((m30, m31, m32, m33))
    ))

def mat43ToQuat(noeMat43):
    logNotImplementedMethod('mat43ToQuat', locals())
    return inc_noesis.NoeQuat()

def mat43TransformNormal(noeMat43, other):
    logNotImplementedMethod('mat43TransformNormal', locals())

def mat43TransformPoint(noeMat43, other):
    logNotImplementedMethod('mat43TransformPoint', locals())

def mat43TransformVec4(noeMat43, other):
    logNotImplementedMethod('mat43TransformVec4', locals())

def mat43Translate(noeMat43, trnVector):
    logNotImplementedMethod('mat43Translate', locals())

def mat43Transpose(noeMat43):
    m00 = noeMat43[0][0]
    m01 = noeMat43[1][0]
    m02 = noeMat43[2][0]
    m10 = noeMat43[0][1]
    m11 = noeMat43[1][1]
    m12 = noeMat43[2][1]
    m20 = noeMat43[0][2]
    m21 = noeMat43[1][2]
    m22 = noeMat43[2][2]
    m30 = noeMat43[3][0]
    m31 = noeMat43[3][1]
    m32 = noeMat43[3][2]

    return inc_noesis.NoeMat43((
        inc_noesis.NoeVec3((m00, m01, m02)),
        inc_noesis.NoeVec3((m10, m11, m12)),
        inc_noesis.NoeVec3((m20, m21, m22)),
        inc_noesis.NoeVec3((m30, m31, m32))
    ))

def mat43Validate(noeMat43):
    mat43 = noeMat43.mat43

    if len(mat43) != 4:
        doException('mat43Validate: validate failed')

    for vec in mat43:
        vec3Validate(vec)

def mat44Add(noeMat44, other):
    m00 = noeMat44[0][0] + other[0][0]
    m01 = noeMat44[0][1] + other[0][1]
    m02 = noeMat44[0][2] + other[0][2]
    m03 = noeMat44[0][3] + other[0][3]
    m10 = noeMat44[1][0] + other[1][0]
    m11 = noeMat44[1][1] + other[1][1]
    m12 = noeMat44[1][2] + other[1][2]
    m13 = noeMat44[1][3] + other[1][3]
    m20 = noeMat44[2][0] + other[2][0]
    m21 = noeMat44[2][1] + other[2][1]
    m22 = noeMat44[2][2] + other[2][2]
    m23 = noeMat44[2][3] + other[2][3]
    m30 = noeMat44[3][0] + other[3][0]
    m31 = noeMat44[3][1] + other[3][1]
    m32 = noeMat44[3][2] + other[3][2]
    m33 = noeMat44[3][3] + other[3][3]

    return inc_noesis.NoeMat44((
        inc_noesis.NoeVec4((m00, m01, m02, m03)),
        inc_noesis.NoeVec4((m10, m11, m12, m13)),
        inc_noesis.NoeVec4((m20, m21, m22, m23)),
        inc_noesis.NoeVec4((m30, m31, m32, m33))
    ))

def mat44FromBytes(data, bigEnd):
    logNotImplementedMethod('mat44FromBytes', locals())
    return inc_noesis.NoeMat44()

def mat44Inverse(mtx):
    m00 = mtx[0][0]
    m01 = mtx[0][1]
    m02 = mtx[0][2]
    m03 = mtx[0][3]
    m10 = mtx[1][0]
    m11 = mtx[1][1]
    m12 = mtx[1][2]
    m13 = mtx[1][3]
    m20 = mtx[2][0]
    m21 = mtx[2][1]
    m22 = mtx[2][2]
    m23 = mtx[2][3]
    m30 = mtx[3][0]
    m31 = mtx[3][1]
    m32 = mtx[3][2]
    m33 = mtx[3][3]

    det = (
          (m00 * m11 - m10 * m01)
        * (m22 * m33 - m32 * m23)
        - (m00 * m21 - m20 * m01)
        * (m12 * m33 - m32 * m13)
        + (m00 * m31 - m30 * m01)
        * (m12 * m23 - m22 * m13)
        + (m10 * m21 - m20 * m11)
        * (m02 * m33 - m32 * m03)
        - (m10 * m31 - m30 * m11)
        * (m02 * m23 - m22 * m03)
        + (m20 * m31 - m30 * m21)
        * (m02 * m13 - m12 * m03)
    )

    if (det == 0.0):
        return inc_noesis.NoeMat44()

    det = 1.0 / det

    i00 = det * (m11 * (m22 * m33 - m32 * m23) + m21 * (m32 * m13 - m12 * m33) + m31 * (m12 * m23 - m22 * m13))
    i10 = det * (m12 * (m20 * m33 - m30 * m23) + m22 * (m30 * m13 - m10 * m33) + m32 * (m10 * m23 - m20 * m13))
    i20 = det * (m13 * (m20 * m31 - m30 * m21) + m23 * (m30 * m11 - m10 * m31) + m33 * (m10 * m21 - m20 * m11))
    i30 = det * (m10 * (m31 * m22 - m21 * m32) + m20 * (m11 * m32 - m31 * m12) + m30 * (m21 * m12 - m11 * m22))
    i01 = det * (m21 * (m02 * m33 - m32 * m03) + m31 * (m22 * m03 - m02 * m23) + m01 * (m32 * m23 - m22 * m33))
    i11 = det * (m22 * (m00 * m33 - m30 * m03) + m32 * (m20 * m03 - m00 * m23) + m02 * (m30 * m23 - m20 * m33))
    i21 = det * (m23 * (m00 * m31 - m30 * m01) + m33 * (m20 * m01 - m00 * m21) + m03 * (m30 * m21 - m20 * m31))
    i31 = det * (m20 * (m31 * m02 - m01 * m32) + m30 * (m01 * m22 - m21 * m02) + m00 * (m21 * m32 - m31 * m22))
    i02 = det * (m31 * (m02 * m13 - m12 * m03) + m01 * (m12 * m33 - m32 * m13) + m11 * (m32 * m03 - m02 * m33))
    i12 = det * (m32 * (m00 * m13 - m10 * m03) + m02 * (m10 * m33 - m30 * m13) + m12 * (m30 * m03 - m00 * m33))
    i22 = det * (m33 * (m00 * m11 - m10 * m01) + m03 * (m10 * m31 - m30 * m11) + m13 * (m30 * m01 - m00 * m31))
    i32 = det * (m30 * (m11 * m02 - m01 * m12) + m00 * (m31 * m12 - m11 * m32) + m10 * (m01 * m32 - m31 * m02))
    i03 = det * (m01 * (m22 * m13 - m12 * m23) + m11 * (m02 * m23 - m22 * m03) + m21 * (m12 * m03 - m02 * m13))
    i13 = det * (m02 * (m20 * m13 - m10 * m23) + m12 * (m00 * m23 - m20 * m03) + m22 * (m10 * m03 - m00 * m13))
    i23 = det * (m03 * (m20 * m11 - m10 * m21) + m13 * (m00 * m21 - m20 * m01) + m23 * (m10 * m01 - m00 * m11))
    i33 = det * (m00 * (m11 * m22 - m21 * m12) + m10 * (m21 * m02 - m01 * m22) + m20 * (m01 * m12 - m11 * m02))

    return inc_noesis.NoeMat44((
        inc_noesis.NoeVec4((i00, i01, i02, i03)),
        inc_noesis.NoeVec4((i10, i11, i12, i13)),
        inc_noesis.NoeVec4((i20, i21, i22, i23)),
        inc_noesis.NoeVec4((i30, i31, i32, i33))
    ))


def mat44Mul(a, b):
    m00 = a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0] + a[0][3] * b[3][0]
    m01 = a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1] + a[0][3] * b[3][1]
    m02 = a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2] + a[0][3] * b[3][2]
    m03 = a[0][0] * b[0][3] + a[0][1] * b[1][3] + a[0][2] * b[2][3] + a[0][3] * b[3][3]
    m10 = a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0] + a[1][3] * b[3][0]
    m11 = a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1] + a[1][3] * b[3][1]
    m12 = a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2] + a[1][3] * b[3][2]
    m13 = a[1][0] * b[0][3] + a[1][1] * b[1][3] + a[1][2] * b[2][3] + a[1][3] * b[3][3]
    m20 = a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0] + a[2][3] * b[3][0]
    m21 = a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1] + a[2][3] * b[3][1]
    m22 = a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2] + a[2][3] * b[3][2]
    m23 = a[2][0] * b[0][3] + a[2][1] * b[1][3] + a[2][2] * b[2][3] + a[2][3] * b[3][3]
    m30 = a[3][0] * b[0][0] + a[3][1] * b[1][0] + a[3][2] * b[2][0] + a[3][3] * b[3][0]
    m31 = a[3][0] * b[0][1] + a[3][1] * b[1][1] + a[3][2] * b[2][1] + a[3][3] * b[3][1]
    m32 = a[3][0] * b[0][2] + a[3][1] * b[1][2] + a[3][2] * b[2][2] + a[3][3] * b[3][2]
    m33 = a[3][0] * b[0][3] + a[3][1] * b[1][3] + a[3][2] * b[2][3] + a[3][3] * b[3][3]

    return inc_noesis.NoeMat44((
        inc_noesis.NoeVec4((m00, m01, m02, m03)),
        inc_noesis.NoeVec4((m10, m11, m12, m13)),
        inc_noesis.NoeVec4((m20, m21, m22, m23)),
        inc_noesis.NoeVec4((m30, m31, m32, m33))
    ))

def mat44Rotate(noeMat44, degrees, rotAngles):
    logNotImplementedMethod('mat44Rotate', locals())

def mat44Sub(noeMat44, other):
    m00 = noeMat44[0][0] - other[0][0]
    m01 = noeMat44[0][1] - other[0][1]
    m02 = noeMat44[0][2] - other[0][2]
    m03 = noeMat44[0][3] - other[0][3]
    m10 = noeMat44[1][0] - other[1][0]
    m11 = noeMat44[1][1] - other[1][1]
    m12 = noeMat44[1][2] - other[1][2]
    m13 = noeMat44[1][3] - other[1][3]
    m20 = noeMat44[2][0] - other[2][0]
    m21 = noeMat44[2][1] - other[2][1]
    m22 = noeMat44[2][2] - other[2][2]
    m23 = noeMat44[2][3] - other[2][3]
    m30 = noeMat44[3][0] - other[3][0]
    m31 = noeMat44[3][1] - other[3][1]
    m32 = noeMat44[3][2] - other[3][2]
    m33 = noeMat44[3][3] - other[3][3]

    return inc_noesis.NoeMat44((
        inc_noesis.NoeVec4((m00, m01, m02, m03)),
        inc_noesis.NoeVec4((m10, m11, m12, m13)),
        inc_noesis.NoeVec4((m20, m21, m22, m23)),
        inc_noesis.NoeVec4((m30, m31, m32, m33))
    ))

def mat44SwapHandedness(noeMat44, axis):
    logNotImplementedMethod('mat44SwapHandedness', locals())

def mat44ToBytes(noeMat44):
    logNotImplementedMethod('mat44ToBytes', locals())

def mat44ToMat43(noeMat44):
    m00 = noeMat44[0][0]
    m10 = noeMat44[0][1]
    m20 = noeMat44[0][2]
    m01 = noeMat44[1][0]
    m11 = noeMat44[1][1]
    m21 = noeMat44[1][2]
    m02 = noeMat44[2][0]
    m12 = noeMat44[2][1]
    m22 = noeMat44[2][2]
    m30 = noeMat44[3][0]
    m31 = noeMat44[3][1]
    m32 = noeMat44[3][2]

    return inc_noesis.NoeMat43((
        inc_noesis.NoeVec3((m00, m01, m02)),
        inc_noesis.NoeVec3((m10, m11, m12)),
        inc_noesis.NoeVec3((m20, m21, m22)),
        inc_noesis.NoeVec3((m30, m31, m32))
    ))

def mat44TransformVec4(noeMat44, other):
    logNotImplementedMethod('mat44TransformVec4', locals())

def mat44Translate(noeMat44, trnVector):
    logNotImplementedMethod('mat44Translate', locals())

def mat44Transpose(noeMat44):
    m00 = noeMat44[0][0]
    m01 = noeMat44[1][0]
    m02 = noeMat44[2][0]
    m03 = noeMat44[3][0]
    m10 = noeMat44[0][1]
    m11 = noeMat44[1][1]
    m12 = noeMat44[2][1]
    m13 = noeMat44[3][1]
    m20 = noeMat44[0][2]
    m21 = noeMat44[1][2]
    m22 = noeMat44[2][2]
    m23 = noeMat44[3][2]
    m30 = noeMat44[0][3]
    m31 = noeMat44[1][3]
    m32 = noeMat44[2][3]
    m33 = noeMat44[3][3]

    return inc_noesis.NoeMat44((
        inc_noesis.NoeVec4((m00, m01, m02, m03)),
        inc_noesis.NoeVec4((m10, m11, m12, m13)),
        inc_noesis.NoeVec4((m20, m21, m22, m23)),
        inc_noesis.NoeVec4((m30, m31, m32, m33))
    ))

def mat44Validate(noeMat44):
    mat44 = noeMat44.mat44

    if len(mat44) != 4:
        doException('mat44Validate: validate failed')

    for vec in mat44:
        vec4Validate(vec)

def messagePrompt(message):
    print(message)

def morton2D(*args):
    logNotImplementedMethod('morton2D', locals())

def nextPow2(*args):
    logNotImplementedMethod('nextPow2', locals())

def openAndRemoveTempFile(path):
    logNotImplementedMethod('openAndRemoveTempFile', locals())

def openFile(path):
    logNotImplementedMethod('openFile', locals())

def optGetArg(name):
    logNotImplementedMethod('optGetArg', locals())

def optWasInvoked(name):
    logNotImplementedMethod('optWasInvoked', locals())

def planeFromPoints(*args):
    logNotImplementedMethod('planeFromPoints', locals())

def quat3FromBytes(data, bigEnd):
    logNotImplementedMethod('quat3FromBytes', locals())
    return inc_noesis.NoeQuat3()

def quat3ToBytes(noeQuat3):
    logNotImplementedMethod('quat3ToBytes', locals())

def quat3ToQuat(noeQuat3):
    x = noeQuat3[0]
    y = noeQuat3[1]
    z = noeQuat3[2]
    return inc_noesis.NoeQuat((x, y, z, 1.0))

def quat3Validate(noeQuat3):
    vec3Validate(noeQuat3)

def quatAdd(noeQuat, other):
    x = noeQuat[0] + other[0]
    y = noeQuat[1] + other[1]
    z = noeQuat[2] + other[2]
    w = noeQuat[3] + other[3]
    return inc_noesis.NoeQuat((x, y, z, w))

def quatFromBytes(data, bigEnd):
    logNotImplementedMethod('quatFromBytes', locals())
    return inc_noesis.NoeQuat()

def quatLen(noeQuat):
    lenSquared = pow(noeQuat[0], 2) + pow(noeQuat[1], 2) + pow(noeQuat[2], 2) + pow(noeQuat[3], 2)
    return math.sqrt(lenSquared)

def quatLerp(noeQuat, other, fraction):
    logNotImplementedMethod('quatLerp', locals())

def quatMul(noeQuat, other):
    logNotImplementedMethod('quatMul', locals())
    return inc_noesis.NoeQuat()

def quatNormalize(noeQuat):
    length = quatLen(noeQuat)
    x = noeQuat[0] / length
    y = noeQuat[1] / length
    z = noeQuat[2] / length
    w = noeQuat[3] / length
    return inc_noesis.NoeQuat((x, y, z, w))

def quatSLerp(noeQuat, other, fraction):
    logNotImplementedMethod('quatSLerp', locals())

def quatSub(noeQuat, other):
    x = noeQuat[0] - other[0]
    y = noeQuat[1] - other[1]
    z = noeQuat[2] - other[2]
    w = noeQuat[3] - other[3]
    return inc_noesis.NoeQuat((x, y, z, w))

def quatToAngles(noeQuat):
    logNotImplementedMethod('quatToAngles', locals())
    return inc_noesis.NoeAngles()

def quatToBytes(noeQuat):
    logNotImplementedMethod('quatToBytes', locals())

def quatToMat43(noeQuat, transposed):
    logNotImplementedMethod('quatToMat43', locals())
    return inc_noesis.NoeMat43()

def quatToQuat3(noeQuat):
    x = noeQuat[0]
    y = noeQuat[1]
    z = noeQuat[2]
    return inc_noesis.NoeQuat3((x, y, z))

def quatTransformNormal(noeQuat, other):
    logNotImplementedMethod('quatTransformNormal', locals())

def quatTransformPoint(noeQuat, other):
    logNotImplementedMethod('quatTransformPoint', locals())

def quatTranspose(noeQuat):
    logNotImplementedMethod('quatTranspose', locals())
    return inc_noesis.NoeQuat()

def quatValidate(noeQuat):
    quat = noeQuat.quat

    if len(quat) != 4:
        doException('quatValidate: validation failed')

    validateListType(quat, Number)

def register(name, fileType):
    # TODO: fileType can be semicolon separated '.obj;.obc'
    handler = Handler(name, fileType)
    this.plugins.append(handler)
    return handler

def registerCleanupFunction(callback):
    logNotImplementedMethod('registerCleanupFunction', locals())

def registerTool(name, callback, description):
    logNotImplementedMethod('registerTool', locals())

def saveImageRGBA(*args):
    logNotImplementedMethod('saveImageRGBA', locals())

def setHandlerExtractArc(handle, callback):
    handle.extractArc = callback

def setHandlerLoadModel(handle, callback):
    handle.loadModel = callback

def setHandlerLoadRGBA(handle, callback):
    handle.loadRGBA = callback

def setHandlerTypeCheck(handle, callback):
    handle.checkType = callback

def setHandlerWriteAnim(handle, callback):
    handle.writeAnim = callback

def setHandlerWriteModel(handle, callback):
    handle.writeModel = callback

def setHandlerWriteRGBA(handle, callback):
    handle.writeRGBA = callback

def setModuleRAPI(handle):
    logNotImplementedMethod('setModuleRAPI', locals())

def setPreviewModuleRAPI():
    logNotImplementedMethod('setPreviewModuleRAPI', locals())

def setToolFlags(handle, flags):
    logNotImplementedMethod('setToolFlags', locals())

def setToolVisibleCallback(handle, callback):
    handle.toolVisibleCallback = callback

def setTypeExportOptions(*args):
    logNotImplementedMethod('setTypeExportOptions', locals())

def triLerp(*args):
    logNotImplementedMethod('triLerp', locals())

def userPrompt(userValType, title, prompt, defaultValue, validationHandler):
    logNotImplementedMethod('userPrompt', locals())

def validateListType(list, types):
    for obj in list:
        if not isinstance(obj, types):
            doException('validateListType: validation failed: expected ' + str(types) + ' but got ' + str(obj))

def validateListTypes(list, types):
    return validateListType(list, types)

def vec3Add(noeVec3, other):
    return inc_noesis.NoeVec3((
        noeVec3[0] + other[0],
        noeVec3[1] + other[1],
        noeVec3[2] + other[2]
    ))

def vec3Cross(noeVec3, other):
    a1 = noeVec3[0]
    a2 = noeVec3[1]
    a3 = noeVec3[2]
    b1 = other[0]
    b2 = other[1]
    b3 = other[2]
    return inc_noesis.NoeVec3((a2 * b3 - a3 * b2,  a3 * b1 - a1 * b3,  a1 * b2 - a2 * b1))

def vec3Div(noeVec3, other):
    x = noeVec3[0] / other[0]
    y = noeVec3[1] / other[1]
    z = noeVec3[2] / other[2]
    return inc_noesis.NoeVec3((x, y, z))

def vec3FromBytes(data, bigEnd):
    logNotImplementedMethod('vec3FromBytes', locals())
    return inc_noesis.NoeVec3()

def vec3Len(noeVec3):
    return math.sqrt(vec3LenSq(noeVec3))

def vec3LenSq(noeVec3):
    return pow(noeVec3[0], 2) + pow(noeVec3[1], 2) + pow(noeVec3[2], 2)

def vec3Lerp(noeVec3, other, fraction):
    logNotImplementedMethod('vec3Lerp', locals())

def vec3Mul(noeVec3, other):
    x = noeVec3[0] * other[0]
    y = noeVec3[1] * other[1]
    z = noeVec3[2] * other[2]
    return inc_noesis.NoeVec3((x, y, z))

def vec3Norm(noeVec3):
    length = vec3Len(noeVec3)
    x = noeVec3[0] / length
    y = noeVec3[1] / length
    z = noeVec3[2] / length
    return inc_noesis.NoeVec3((x, y, z))

def vec3Sub(noeVec3, other):
    return inc_noesis.NoeVec3((
        noeVec3[0] - other[0],
        noeVec3[1] - other[1],
        noeVec3[2] - other[2]
    ))

def vec3ToAngles(noeVec3):
    logNotImplementedMethod('vec3ToAngles', locals())
    return inc_noesis.NoeAngles()

def vec3ToBytes(noeVec3):
    logNotImplementedMethod('vec3ToBytes', locals())

def vec3ToMat43(noeVec3):
    logNotImplementedMethod('vec3ToMat43', locals())
    return inc_noesis.NoeMat43((
        inc_noesis.NoeVec3((noeVec3[0], noeVec3[1], noeVec3[2])),
        inc_noesis.NoeVec3((1.0, 1.0, 1.0)),
        inc_noesis.NoeVec3((1.0, 1.0, 1.0)),
        inc_noesis.NoeVec3((0.0, 0.0, 0.0))
    ))

def vec3ToVec4(noeVec3):
    x = noeVec3[0]
    y = noeVec3[1]
    z = noeVec3[2]
    return inc_noesis.NoeVec4((x, y, z, 0.0))

def vec3Validate(noeVec3):
    vec3 = noeVec3.vec3

    if len(vec3) != 3:
        doException('vec3Validate: validate failed')

    validateListType(vec3, Number)

def vec4Add(noeVec4, other):
    x = noeVec4[0] + other[0]
    y = noeVec4[1] + other[1]
    z = noeVec4[2] + other[2]
    w = noeVec4[3] + other[3]
    return inc_noesis.NoeVec4((x, y, z, w))

def vec4Div(noeVec4, other):
    x = noeVec4[0] / other[0]
    y = noeVec4[1] / other[1]
    z = noeVec4[2] / other[2]
    w = noeVec4[3] / other[3]
    return inc_noesis.NoeVec4((x, y, z, w))

def vec4Dot(noeVec4, other):
    return noeVec4[0] * other[0] + noeVec4[1] * other[1] + noeVec4[2] * other[2] + noeVec4[3] * other[3]

def vec4FromBytes(bytes, bigEnd):
    logNotImplementedMethod('vec4FromBytes', locals())
    return inc_noesis.NoeVec4()

def vec4Len(noeVec4):
    return math.sqrt(vec4LenSq(noeVec4))

def vec4LenSq(noeVec4):
    return pow(noeVec4[0], 2) + pow(noeVec4[1], 2) + pow(noeVec4[2], 2) + pow(noeVec4[3], 2)

def vec4Lerp(noeVec4, other, fraction):
    logNotImplementedMethod('vec4Lerp', locals())

def vec4Mul(noeVec4, other):
    x = noeVec4[0] * other[0]
    y = noeVec4[1] * other[1]
    z = noeVec4[2] * other[2]
    w = noeVec4[3] * other[3]
    return inc_noesis.NoeVec4((x, y, z, w))

def vec4Norm(noeVec4):
    length = vec4Len(noeVec4)
    x = noeVec4[0] / length
    y = noeVec4[1] / length
    z = noeVec4[2] / length
    w = noeVec4[3] / length
    return inc_noesis.NoeVec4((x, y, z, w))

def vec4Sub(noeVec4, other):
    x = noeVec4[0] - other[0]
    y = noeVec4[1] - other[1]
    z = noeVec4[2] - other[2]
    w = noeVec4[3] - other[3]
    return inc_noesis.NoeVec4((x, y, z, w))

def vec4ToBytes(noeVec4):
    logNotImplementedMethod('vec4ToBytes', locals())

def vec4ToVec3(noeVec4):
    return inc_noesis.NoeVec3((noeVec4[0], noeVec4[1], noeVec4[2]))

def vec4Validate(noeVec4):
    vec4 = noeVec4.vec4

    if len(vec4) != 4:
        doException('vec4Validate: validation failed')

    validateListType(vec4, Number)

# private

def bsReadAndUnpack(handle, fmt):
    return handle.bsReadAndUnpack(fmt)

def bsDumpMask(handle):
    data = handle.readData
    writeData = ''.join(map(chr, data))
    mask = open('/Users/andrzej/Desktop/mask.bin', 'wb')
    mask.write(writeData)
    mask.close()

import inc_noesis
