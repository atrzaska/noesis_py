from Handler import Handler
from NoeModule import NoeModule
from AllocType import AllocType
from numbers import Number
import sys
from util import logNotImplementedMethod
import struct

# constants

BITSTREAMFL_BIGENDIAN = 'BITSTREAMFL_BIGENDIAN'
BITSTREAMFL_DESCENDINGBITS = 'BITSTREAMFL_DESCENDINGBITS'
BITSTREAMFL_USERFLAG1 = 'BITSTREAMFL_USERFLAG1'
BITSTREAMFL_USERFLAG2 = 'BITSTREAMFL_USERFLAG2'
BITSTREAMFL_USERFLAG3 = 'BITSTREAMFL_USERFLAG3'
BITSTREAMFL_USERFLAG4 = 'BITSTREAMFL_USERFLAG4'
BITSTREAMFL_USERFLAG5 = 'BITSTREAMFL_USERFLAG5'
BITSTREAMFL_USERFLAG6 = 'BITSTREAMFL_USERFLAG6'
BITSTREAMFL_USERFLAG7 = 'BITSTREAMFL_USERFLAG7'
BITSTREAMFL_USERFLAG8 = 'BITSTREAMFL_USERFLAG8'
BLITFLAG_ALPHABLEND = 'BLITFLAG_ALPHABLEND'
BONEFLAG_DECOMPLERP = 'BONEFLAG_DECOMPLERP'
BONEFLAG_DIRECTLERP = 'BONEFLAG_DIRECTLERP'
BONEFLAG_NOLERP = 'BONEFLAG_NOLERP'
BONEFLAG_ORTHOLERP = 'BONEFLAG_ORTHOLERP'
DECODEFLAG_PS2SHIFT = 'DECODEFLAG_PS2SHIFT'
FOURCC_ATI1 = 'FOURCC_ATI1'
FOURCC_ATI2 = 'FOURCC_ATI2'
FOURCC_BC1 = 'FOURCC_BC1'
FOURCC_BC2 = 'FOURCC_BC2'
FOURCC_BC3 = 'FOURCC_BC3'
FOURCC_BC4 = 'FOURCC_BC4'
FOURCC_BC5 = 'FOURCC_BC5'
FOURCC_BC6H = 'FOURCC_BC6H'
FOURCC_BC6S = 'FOURCC_BC6S'
FOURCC_BC7 = 'FOURCC_BC7'
FOURCC_DX10 = 'FOURCC_DX10'
FOURCC_DXT1 = 'FOURCC_DXT1'
FOURCC_DXT1NORMAL = 'FOURCC_DXT1NORMAL'
FOURCC_DXT3 = 'FOURCC_DXT3'
FOURCC_DXT5 = 'FOURCC_DXT5'
g_flDegToRad = 0.0174532925
g_flPI = 3.14159265359
g_flRadToDeg = 57.2957795
MAX_NOESIS_PATH = 'MAX_NOESIS_PATH'
NANIMFLAG_FORCENAMEMATCH = 'NANIMFLAG_FORCENAMEMATCH'
NANIMFLAG_INVALIDHIERARCHY = 'NANIMFLAG_INVALIDHIERARCHY'
NFORMATFLAG_ANIMWRITE = 'NFORMATFLAG_ANIMWRITE'
NFORMATFLAG_ARCREAD = 'NFORMATFLAG_ARCREAD'
NFORMATFLAG_IMGREAD = 'NFORMATFLAG_IMGREAD'
NFORMATFLAG_IMGWRITE = 'NFORMATFLAG_IMGWRITE'
NFORMATFLAG_MODELREAD = 'NFORMATFLAG_MODELREAD'
NFORMATFLAG_MODELWRITE = 'NFORMATFLAG_MODELWRITE'
NMATFLAG_BLENDEDNORMALS = 'NMATFLAG_BLENDEDNORMALS'
NMATFLAG_ENV_FLIP = 'NMATFLAG_ENV_FLIP'
NMATFLAG_GAMMACORRECT = 'NMATFLAG_GAMMACORRECT'
NMATFLAG_KAJIYAKAY = 'NMATFLAG_KAJIYAKAY'
NMATFLAG_NMAPSWAPRA = 'NMATFLAG_NMAPSWAPRA'
NMATFLAG_NORMAL_UV1 = 'NMATFLAG_NORMAL_UV1'
NMATFLAG_NORMALMAP_FLIPY = 'NMATFLAG_NORMALMAP_FLIPY'
NMATFLAG_NORMALMAP_NODERZ = 'NMATFLAG_NORMALMAP_NODERZ'
NMATFLAG_PBR_ALBEDOENERGYCON = 'NMATFLAG_PBR_ALBEDOENERGYCON'
NMATFLAG_PBR_COMPENERGYCON = 'NMATFLAG_PBR_COMPENERGYCON'
NMATFLAG_PBR_METAL = 'NMATFLAG_PBR_METAL'
NMATFLAG_PBR_ROUGHNESS_NRMALPHA = 'NMATFLAG_PBR_ROUGHNESS_NRMALPHA'
NMATFLAG_PBR_SPEC = 'NMATFLAG_PBR_SPEC'
NMATFLAG_PBR_SPEC_IR_RG = 'NMATFLAG_PBR_SPEC_IR_RG'
NMATFLAG_PREVIEWLOAD = 'NMATFLAG_PREVIEWLOAD'
NMATFLAG_SORT01 = 'NMATFLAG_SORT01'
NMATFLAG_SPEC_UV1 = 'NMATFLAG_SPEC_UV1'
NMATFLAG_SPRITE_FACINGXY = 'NMATFLAG_SPRITE_FACINGXY'
NMATFLAG_TWOSIDED = 'NMATFLAG_TWOSIDED'
NMATFLAG_USELMUVS = 'NMATFLAG_USELMUVS'
NMATFLAG_VCOLORSUBTRACT = 'NMATFLAG_VCOLORSUBTRACT'
NMSHAREDFL_BONEPALETTE = 'NMSHAREDFL_BONEPALETTE'
NMSHAREDFL_FLATWEIGHTS = 'NMSHAREDFL_FLATWEIGHTS'
NMSHAREDFL_FLATWEIGHTS_FORCE4 = 'NMSHAREDFL_FLATWEIGHTS_FORCE4'
NMSHAREDFL_REVERSEWINDING = 'NMSHAREDFL_REVERSEWINDING'
NMSHAREDFL_UNIQUEVERTS = 'NMSHAREDFL_UNIQUEVERTS'
NMSHAREDFL_WANTGLOBALARRAY = 'NMSHAREDFL_WANTGLOBALARRAY'
NMSHAREDFL_WANTNEIGHBORS = 'NMSHAREDFL_WANTNEIGHBORS'
NMSHAREDFL_WANTTANGENTS = 'NMSHAREDFL_WANTTANGENTS'
NMSHAREDFL_WANTTANGENTS4 = 'NMSHAREDFL_WANTTANGENTS4'
NMSHAREDFL_WANTTANGENTS4R = 'NMSHAREDFL_WANTTANGENTS4R'
NOE_ENCODEDXT_BC1 = 'NOE_ENCODEDXT_BC1'
NOE_ENCODEDXT_BC3 = 'NOE_ENCODEDXT_BC3'
NOE_ENCODEDXT_BC4 = 'NOE_ENCODEDXT_BC4'
NOEBLEND_DST_ALPHA = 'NOEBLEND_DST_ALPHA'
NOEBLEND_DST_COLOR = 'NOEBLEND_DST_COLOR'
NOEBLEND_NONE = 'NOEBLEND_NONE'
NOEBLEND_ONE = 'NOEBLEND_ONE'
NOEBLEND_ONE_MINUS_DST_ALPHA = 'NOEBLEND_ONE_MINUS_DST_ALPHA'
NOEBLEND_ONE_MINUS_DST_COLOR = 'NOEBLEND_ONE_MINUS_DST_COLOR'
NOEBLEND_ONE_MINUS_SRC_ALPHA = 'NOEBLEND_ONE_MINUS_SRC_ALPHA'
NOEBLEND_ONE_MINUS_SRC_COLOR = 'NOEBLEND_ONE_MINUS_SRC_COLOR'
NOEBLEND_SRC_ALPHA = 'NOEBLEND_SRC_ALPHA'
NOEBLEND_SRC_ALPHA_SATURATE = 'NOEBLEND_SRC_ALPHA_SATURATE'
NOEBLEND_SRC_COLOR = 'NOEBLEND_SRC_COLOR'
NOEBLEND_ZERO = 'NOEBLEND_ZERO'
NOEFSMODE_READBINARY = 'NOEFSMODE_READBINARY'
NOEFSMODE_READWRITEBINARY = 'NOEFSMODE_READWRITEBINARY'
NOEFSMODE_WRITEBINARY = 'NOEFSMODE_WRITEBINARY'
NOEKF_INTERPOLATE_LINEAR = 'NOEKF_INTERPOLATE_LINEAR'
NOEKF_INTERPOLATE_NEAREST = 'NOEKF_INTERPOLATE_NEAREST'
NOEKF_ROTATION_QUATERNION_4 = 'NOEKF_ROTATION_QUATERNION_4'
NOEKF_SCALE_SCALAR_1 = 'NOEKF_SCALE_SCALAR_1'
NOEKF_SCALE_SINGLE = 'NOEKF_SCALE_SINGLE'
NOEKF_SCALE_TRANSPOSED_VECTOR_3 = 'NOEKF_SCALE_TRANSPOSED_VECTOR_3'
NOEKF_SCALE_VECTOR_3 = 'NOEKF_SCALE_VECTOR_3'
NOEKF_TRANSLATION_SINGLE = 'NOEKF_TRANSLATION_SINGLE'
NOEKF_TRANSLATION_VECTOR_3 = 'NOEKF_TRANSLATION_VECTOR_3'
NOESIS_PLUGIN_VERSION = 'NOESIS_PLUGIN_VERSION'
NOESIS_PLUGINAPI_VERSION = 'NOESIS_PLUGINAPI_VERSION'
NOESISTEX_DXT1 = 'NOESISTEX_DXT1'
NOESISTEX_DXT3 = 'NOESISTEX_DXT3'
NOESISTEX_DXT5 = 'NOESISTEX_DXT5'
NOESISTEX_RGB24 = 'NOESISTEX_RGB24'
NOESISTEX_RGBA32 = 'NOESISTEX_RGBA32'
NOESISTEX_UNKNOWN = 'NOESISTEX_UNKNOWN'
NOESPLINEFLAG_CLOSED = 'NOESPLINEFLAG_CLOSED'
NOEUSERVAL_BOOL = 'NOEUSERVAL_BOOL'
NOEUSERVAL_FILEPATH = 'NOEUSERVAL_FILEPATH'
NOEUSERVAL_FLOAT = 'NOEUSERVAL_FLOAT'
NOEUSERVAL_FOLDERPATH = 'NOEUSERVAL_FOLDERPATH'
NOEUSERVAL_INT = 'NOEUSERVAL_INT'
NOEUSERVAL_NONE = 'NOEUSERVAL_NONE'
NOEUSERVAL_SAVEFILEPATH = 'NOEUSERVAL_SAVEFILEPATH'
NOEUSERVAL_STRING = 'NOEUSERVAL_STRING'
NSEQFLAG_NONLOOPING = 'NSEQFLAG_NONLOOPING'
NSEQFLAG_REVERSE = 'NSEQFLAG_REVERSE'
NTEXFLAG_CUBEMAP = 'NTEXFLAG_CUBEMAP'
NTEXFLAG_FILTER_NEAREST = 'NTEXFLAG_FILTER_NEAREST'
NTEXFLAG_HDRISLINEAR = 'NTEXFLAG_HDRISLINEAR'
NTEXFLAG_ISLINEAR = 'NTEXFLAG_ISLINEAR'
NTEXFLAG_ISNORMALMAP = 'NTEXFLAG_ISNORMALMAP'
NTEXFLAG_PREVIEWLOAD = 'NTEXFLAG_PREVIEWLOAD'
NTEXFLAG_SEGMENTED = 'NTEXFLAG_SEGMENTED'
NTEXFLAG_STEREO = 'NTEXFLAG_STEREO'
NTEXFLAG_STEREO_SWAP = 'NTEXFLAG_STEREO_SWAP'
NTEXFLAG_WANTSEAMLESS = 'NTEXFLAG_WANTSEAMLESS'
NTEXFLAG_WRAP_CLAMP = 'NTEXFLAG_WRAP_CLAMP'
NTEXFLAG_WRAP_MIRROR_CLAMP = 'NTEXFLAG_WRAP_MIRROR_CLAMP'
NTEXFLAG_WRAP_MIRROR_REPEAT = 'NTEXFLAG_WRAP_MIRROR_REPEAT'
NTEXFLAG_WRAP_REPEAT = 'NTEXFLAG_WRAP_REPEAT'
NTOOLFLAG_CONTEXTITEM = 'NTOOLFLAG_CONTEXTITEM'
NTOOLFLAG_USERBITS = 'NTOOLFLAG_USERBITS'
NUM_NOE_BLENDS = 'NUM_NOE_BLENDS'
NUM_NOEKF_INTERPOLATION_TYPES = 'NUM_NOEKF_INTERPOLATION_TYPES'
NUM_NOEKF_ROTATION_TYPES = 'NUM_NOEKF_ROTATION_TYPES'
NUM_NOEKF_SCALE_TYPES = 'NUM_NOEKF_SCALE_TYPES'
NUM_NOEKF_TRANSLATION_TYPES = 'NUM_NOEKF_TRANSLATION_TYPES'
NUM_RPGEO_DATATYPES = 'NUM_RPGEO_DATATYPES'
NUM_RPGEO_TYPES = 'NUM_RPGEO_TYPES'
OPTFLAG_WANTARG = 'OPTFLAG_WANTARG'
PS2_VIFCODE_BASE = 'PS2_VIFCODE_BASE'
PS2_VIFCODE_DIRECT = 'PS2_VIFCODE_DIRECT'
PS2_VIFCODE_DIRECTHL = 'PS2_VIFCODE_DIRECTHL'
PS2_VIFCODE_FLUSH = 'PS2_VIFCODE_FLUSH'
PS2_VIFCODE_FLUSHA = 'PS2_VIFCODE_FLUSHA'
PS2_VIFCODE_FLUSHE = 'PS2_VIFCODE_FLUSHE'
PS2_VIFCODE_ITOP = 'PS2_VIFCODE_ITOP'
PS2_VIFCODE_MARK = 'PS2_VIFCODE_MARK'
PS2_VIFCODE_MPG = 'PS2_VIFCODE_MPG'
PS2_VIFCODE_MSCAL = 'PS2_VIFCODE_MSCAL'
PS2_VIFCODE_MSCALF = 'PS2_VIFCODE_MSCALF'
PS2_VIFCODE_MSCNT = 'PS2_VIFCODE_MSCNT'
PS2_VIFCODE_MSKPATH3 = 'PS2_VIFCODE_MSKPATH3'
PS2_VIFCODE_NOP = 'PS2_VIFCODE_NOP'
PS2_VIFCODE_OFFSET = 'PS2_VIFCODE_OFFSET'
PS2_VIFCODE_STCOL = 'PS2_VIFCODE_STCOL'
PS2_VIFCODE_STCYCL = 'PS2_VIFCODE_STCYCL'
PS2_VIFCODE_STMASK = 'PS2_VIFCODE_STMASK'
PS2_VIFCODE_STMOD = 'PS2_VIFCODE_STMOD'
PS2_VIFCODE_STROW = 'PS2_VIFCODE_STROW'
PVRTC_DECODE_BICUBIC = 'PVRTC_DECODE_BICUBIC'
PVRTC_DECODE_LINEARORDER = 'PVRTC_DECODE_LINEARORDER'
PVRTC_DECODE_PVRTC2 = 'PVRTC_DECODE_PVRTC2'
PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA = 'PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA'
PVRTC_DECODE_PVRTC2_ROTATE_BLOCK_PAL = 'PVRTC_DECODE_PVRTC2_ROTATE_BLOCK_PAL'
RPGEO_NONE = 'RPGEO_NONE'
RPGEO_POINTS = 'RPGEO_POINTS'
RPGEO_POLYGON = 'RPGEO_POLYGON'
RPGEO_QUAD = 'RPGEO_QUAD' # ABC_DCB
RPGEO_QUAD_ABC_ACD = 'RPGEO_QUAD_ABC_ACD'
RPGEO_QUAD_ABC_BCD = 'RPGEO_QUAD_ABC_BCD'
RPGEO_QUAD_ABC_DCA = 'RPGEO_QUAD_ABC_DCA'
RPGEO_QUAD_STRIP = 'RPGEO_QUAD_STRIP'
RPGEO_TRIANGLE = 'RPGEO_TRIANGLE'
RPGEO_TRIANGLE_FAN = 'RPGEO_TRIANGLE_FAN'
RPGEO_TRIANGLE_STRIP = 'RPGEO_TRIANGLE_STRIP'
RPGEO_TRIANGLE_STRIP_FLIPPED = 'RPGEO_TRIANGLE_STRIP_FLIPPED'
RPGEODATA_BYTE = 'RPGEODATA_BYTE'
RPGEODATA_DOUBLE = 'RPGEODATA_DOUBLE'
RPGEODATA_FLOAT = 'RPGEODATA_FLOAT'
RPGEODATA_HALFFLOAT = 'RPGEODATA_HALFFLOAT'
RPGEODATA_INT = 'RPGEODATA_INT'
RPGEODATA_SHORT = 'RPGEODATA_SHORT'
RPGEODATA_UBYTE = 'RPGEODATA_UBYTE'
RPGEODATA_UINT = 'RPGEODATA_UINT'
RPGEODATA_USHORT = 'RPGEODATA_USHORT'
RPGOPT_BIGENDIAN = 'RPGOPT_BIGENDIAN'
RPGOPT_DERIVEBONEORIS = 'RPGOPT_DERIVEBONEORIS'
RPGOPT_FILLINWEIGHTS = 'RPGOPT_FILLINWEIGHTS'
RPGOPT_MORPH_RELATIVENORMALS = 'RPGOPT_MORPH_RELATIVENORMALS'
RPGOPT_MORPH_RELATIVEPOSITIONS = 'RPGOPT_MORPH_RELATIVEPOSITIONS'
RPGOPT_SWAPHANDEDNESS = 'RPGOPT_SWAPHANDEDNESS'
RPGOPT_TANMATROTATE = 'RPGOPT_TANMATROTATE'
RPGOPT_TRIWINDBACKWARD = 'RPGOPT_TRIWINDBACKWARD'
RPGOPT_UNSAFE = 'RPGOPT_UNSAFE'
RPGVUFLAG_NOREUSE = 'RPGVUFLAG_NOREUSE'
RPGVUFLAG_PERINSTANCE = 'RPGVUFLAG_PERINSTANCE'
SHAREDSTRIP_LIST = 'SHAREDSTRIP_LIST'
SHAREDSTRIP_STRIP = 'SHAREDSTRIP_STRIP'

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

def anglesMod(noeAngles, f):
    logNotImplementedMethod('anglesMod', locals())

def anglesNormalize180(noeAngles):
    logNotImplementedMethod('anglesNormalize180', locals())

def anglesNormalize360(noeAngles):
    logNotImplementedMethod('anglesNormalize360', locals())

def anglesToMat43(noeAngles):
    logNotImplementedMethod('anglesToMat43', locals())

def anglesToMat43_XYZ(noeAngles, yFlip):
    # TODO: implement this properly
    return inc_noesis.NoeMat43()

def anglesToQuat(noeAngles):
    logNotImplementedMethod('anglesToQuat', locals())

def anglesToVec3(noeAngles):
    logNotImplementedMethod('anglesToVec3', locals())

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
    logNotImplementedMethod('mat43Add', locals())

def mat43FromBytes(data, bigEnd):
    logNotImplementedMethod('mat43FromBytes', locals())

def mat43Inverse(noeMat43):
    # TODO: implement this properly
    return noeMat43

def mat43IsSkewed(noeMat43):
    logNotImplementedMethod('mat43IsSkewed', locals())

def mat43Lerp(noeMat43, other, fraction):
    logNotImplementedMethod('mat43Lerp', locals())

def mat43Mul(noeMat43, other):
    noeMat44 = noeMat43.toMat44()
    otherMat44 = other.toMat44()
    return (noeMat44 * otherMat44).toMat43()

def mat43Orthogonalize(noeMat43):
    logNotImplementedMethod('mat43Orthogonalize', locals())

def mat43Rotate(noeMat43, degrees, rotAngles, transposeRot):
    logNotImplementedMethod('mat43Rotate', locals())

def mat43SLerp(noeMat43, other, fraction):
    logNotImplementedMethod('mat43SLerp', locals())

def mat43Sub(noeMat43, other):
    logNotImplementedMethod('mat43Sub', locals())

def mat43SwapHandedness(noeMat43, axis):
    logNotImplementedMethod('mat43SwapHandedness', locals())

def mat43ToAngles(noeMat43):
    logNotImplementedMethod('mat43ToAngles', locals())

def mat43ToBytes(noeMat43):
    logNotImplementedMethod('mat43ToBytes', locals())

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
    logNotImplementedMethod('mat43ToQuat', locals())

def mat43TransformNormal(noeMat43, other):
    logNotImplementedMethod('mat43TransformNormal', locals())

def mat43TransformPoint(noeMat43, other):
    logNotImplementedMethod('mat43TransformPoint', locals())

def mat43TransformVec4(noeMat43, other):
    logNotImplementedMethod('mat43TransformVec4', locals())

def mat43Translate(noeMat43, trnVector):
    logNotImplementedMethod('mat43Translate', locals())

def mat43Transpose(noeMat43):
    logNotImplementedMethod('mat43Transpose', locals())

def mat43Validate(noeMat43):
    mat43 = noeMat43.mat43

    if len(mat43) != 4:
        doException('mat43Validate: validate failed')

    for vec in mat43:
        vec3Validate(vec)

def mat44Add(noeMat44, other):
    logNotImplementedMethod('mat44Add', locals())

def mat44FromBytes(data, bigEnd):
    logNotImplementedMethod('mat44FromBytes', locals())

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
    logNotImplementedMethod('mat44Rotate', locals())

def mat44Sub(noeMat44, other):
    logNotImplementedMethod('mat44Sub', locals())

def mat44SwapHandedness(noeMat44, axis):
    logNotImplementedMethod('mat44SwapHandedness', locals())

def mat44ToBytes(noeMat44):
    logNotImplementedMethod('mat44ToBytes', locals())

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
    logNotImplementedMethod('mat44TransformVec4', locals())

def mat44Translate(noeMat44, trnVector):
    logNotImplementedMethod('mat44Translate', locals())

def mat44Transpose(noeMat44):
    logNotImplementedMethod('mat44Transpose', locals())

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

def quat3ToBytes(noeQuat3):
    logNotImplementedMethod('quat3ToBytes', locals())

def quat3ToQuat(noeQuat3):
    logNotImplementedMethod('quat3ToQuat', locals())

def quat3Validate(noeQuat3):
    vec3Validate(noeQuat3)

def quatAdd(noeQuat, other):
    logNotImplementedMethod('quatAdd', locals())

def quatFromBytes(data, bigEnd):
    logNotImplementedMethod('quatFromBytes', locals())

def quatLen(noeQuat):
    logNotImplementedMethod('quatLen', locals())

def quatLerp(noeQuat, other, fraction):
    logNotImplementedMethod('quatLerp', locals())

def quatMul(noeQuat, other):
    logNotImplementedMethod('quatMul', locals())

def quatNormalize(noeQuat):
    logNotImplementedMethod('quatNormalize', locals())

def quatSLerp(noeQuat, other, fraction):
    logNotImplementedMethod('quatSLerp', locals())

def quatSub(noeQuat, other):
    logNotImplementedMethod('quatSub', locals())

def quatToAngles(noeQuat):
    logNotImplementedMethod('quatToAngles', locals())

def quatToBytes(noeQuat):
    logNotImplementedMethod('quatToBytes', locals())

def quatToMat43(noeQuat, transposed):
    logNotImplementedMethod('quatToMat43', locals())

def quatToQuat3(noeQuat):
    logNotImplementedMethod('quatToQuat3', locals())

def quatTransformNormal(noeQuat, other):
    logNotImplementedMethod('quatTransformNormal', locals())

def quatTransformPoint(noeQuat, other):
    logNotImplementedMethod('quatTransformPoint', locals())

def quatTranspose(noeQuat):
    logNotImplementedMethod('quatTranspose', locals())

def quatValidate(noeQuat):
    quat = noeQuat.quat

    validateListType(quat, Number)

    if len(quat) != 4:
        doException('quatValidate: validation failed')

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
    logNotImplementedMethod('vec3Add', locals())

def vec3Cross(noeVec3, other):
    logNotImplementedMethod('vec3Cross', locals())

def vec3Div(noeVec3, other):
    logNotImplementedMethod('vec3Div', locals())

def vec3FromBytes(data, bigEnd):
    logNotImplementedMethod('vec3FromBytes', locals())

def vec3Len(noeVec3):
    logNotImplementedMethod('vec3Len', locals())

def vec3LenSq(noeVec3):
    logNotImplementedMethod('vec3LenSq', locals())

def vec3Lerp(noeVec3, other, fraction):
    logNotImplementedMethod('vec3Lerp', locals())

def vec3Mul(noeVec3, other):
    logNotImplementedMethod('vec3Mul', locals())

def vec3Norm(noeVec3):
    logNotImplementedMethod('vec3Norm', locals())

def vec3Sub(noeVec3, other):
    logNotImplementedMethod('vec3Sub', locals())

def vec3ToAngles(noeVec3):
    logNotImplementedMethod('vec3ToAngles', locals())

def vec3ToBytes(noeVec3):
    logNotImplementedMethod('vec3ToBytes', locals())

def vec3ToMat43(noeVec3):
    logNotImplementedMethod('vec3ToMat43', locals())

def vec3ToVec4(noeVec3):
    logNotImplementedMethod('vec3ToVec4', locals())

def vec3Validate(noeVec3):
    vec3 = noeVec3.vec3

    if len(vec3) != 3:
        doException('vec3Validate: validate failed')

    validateListType(vec3, Number)

def vec4Add(noeVec4, other):
    logNotImplementedMethod('vec4Add', locals())

def vec4Div(noeVec4, other):
    logNotImplementedMethod('vec4Div', locals())

def vec4Dot(noeVec4, other):
    logNotImplementedMethod('vec4Dot', locals())

def vec4FromBytes(bytes, bigEnd):
    logNotImplementedMethod('vec4FromBytes', locals())

def vec4Len(noeVec4):
    logNotImplementedMethod('vec4Len', locals())

def vec4LenSq(noeVec4):
    logNotImplementedMethod('vec4LenSq', locals())

def vec4Lerp(noeVec4, other, fraction):
    logNotImplementedMethod('vec4Lerp', locals())

def vec4Mul(noeVec4, other):
    logNotImplementedMethod('vec4Mul', locals())

def vec4Norm(noeVec4):
    logNotImplementedMethod('vec4Norm', locals())

def vec4Sub(noeVec4, other):
    logNotImplementedMethod('vec4Sub', locals())

def vec4ToBytes(noeVec4):
    logNotImplementedMethod('vec4ToBytes', locals())

def vec4ToVec3(noeVec4):
    logNotImplementedMethod('vec4ToVec3', locals())

def vec4Validate(noeVec4):
    vec4 = noeVec4.vec4

    validateListType(vec4, Number)

    if len(vec4) != 4:
        doException('vec4Validate: validation failed')

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
