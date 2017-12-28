from inc_noesis import *
from noesis import *
import rapi

def registerNoesisTypes():
    handle = register('Test Format', '.test')
    setHandlerTypeCheck(handle, checkType)
    setHandlerLoadModel(handle, loadModel)
    return 1

def checkType(data):
    return 1

def noeassert(name, result, expected):
    classMatching = result.__class__.__name__ == expected.__class__.__name__
    valueMatching = result == expected

    if classMatching and valueMatching:
        print('OK ' + name)
    else:
        print('ERR ' + name)

def loadModel(data, mdlList):
    print('Constants')
    noeassert('BITSTREAMFL_BIGENDIAN', BITSTREAMFL_BIGENDIAN, 65536)
    noeassert('BITSTREAMFL_DESCENDINGBITS', BITSTREAMFL_DESCENDINGBITS, 131072)
    noeassert('BITSTREAMFL_USERFLAG1', BITSTREAMFL_USERFLAG1, 16777216)
    noeassert('BITSTREAMFL_USERFLAG2', BITSTREAMFL_USERFLAG2, 33554432)
    noeassert('BITSTREAMFL_USERFLAG3', BITSTREAMFL_USERFLAG3, 67108864)
    noeassert('BITSTREAMFL_USERFLAG4', BITSTREAMFL_USERFLAG4, 134217728)
    noeassert('BITSTREAMFL_USERFLAG5', BITSTREAMFL_USERFLAG5, 268435456)
    noeassert('BITSTREAMFL_USERFLAG6', BITSTREAMFL_USERFLAG6, 536870912)
    noeassert('BITSTREAMFL_USERFLAG7', BITSTREAMFL_USERFLAG7, 1073741824)
    noeassert('BITSTREAMFL_USERFLAG8', BITSTREAMFL_USERFLAG8, -2147483648)
    noeassert('BLITFLAG_ALPHABLEND', BLITFLAG_ALPHABLEND, 1)
    noeassert('BONEFLAG_DECOMPLERP', BONEFLAG_DECOMPLERP, 8)
    noeassert('BONEFLAG_DIRECTLERP', BONEFLAG_DIRECTLERP, 2)
    noeassert('BONEFLAG_NOLERP', BONEFLAG_NOLERP, 4)
    noeassert('BONEFLAG_ORTHOLERP', BONEFLAG_ORTHOLERP, 1)
    noeassert('DECODEFLAG_PS2SHIFT', DECODEFLAG_PS2SHIFT, 1)
    noeassert('FOURCC_ATI1', FOURCC_ATI1, 826889281)
    noeassert('FOURCC_ATI2', FOURCC_ATI2, 843666497)
    noeassert('FOURCC_BC1', FOURCC_BC1, 827611204)
    noeassert('FOURCC_BC2', FOURCC_BC2, 861165636)
    noeassert('FOURCC_BC3', FOURCC_BC3, 894720068)
    noeassert('FOURCC_BC4', FOURCC_BC4, 826889281)
    noeassert('FOURCC_BC5', FOURCC_BC5, 843666497)
    noeassert('FOURCC_BC6H', FOURCC_BC6H, 1211515714)
    noeassert('FOURCC_BC6S', FOURCC_BC6S, 1396065090)
    noeassert('FOURCC_BC7', FOURCC_BC7, 1480016706)
    noeassert('FOURCC_DX10', FOURCC_DX10, 808540228)
    noeassert('FOURCC_DXT1', FOURCC_DXT1, 827611204)
    noeassert('FOURCC_DXT1NORMAL', FOURCC_DXT1NORMAL, 1311855684)
    noeassert('FOURCC_DXT3', FOURCC_DXT3, 861165636)
    noeassert('FOURCC_DXT5', FOURCC_DXT5, 894720068)
    noeassert('g_flDegToRad', g_flDegToRad, 0.01745329238474369)
    noeassert('g_flPI', g_flPI, 3.1415927410125732)
    noeassert('g_flRadToDeg', g_flRadToDeg, 57.2957763671875)
    noeassert('MAX_NOESIS_PATH', MAX_NOESIS_PATH, 4096)
    noeassert('NANIMFLAG_FORCENAMEMATCH', NANIMFLAG_FORCENAMEMATCH, 1)
    noeassert('NANIMFLAG_INVALIDHIERARCHY', NANIMFLAG_INVALIDHIERARCHY, 2)
    noeassert('NFORMATFLAG_ANIMWRITE', NFORMATFLAG_ANIMWRITE, 32)
    noeassert('NFORMATFLAG_ARCREAD', NFORMATFLAG_ARCREAD, 1)
    noeassert('NFORMATFLAG_IMGREAD', NFORMATFLAG_IMGREAD, 2)
    noeassert('NFORMATFLAG_IMGWRITE', NFORMATFLAG_IMGWRITE, 4)
    noeassert('NFORMATFLAG_MODELREAD', NFORMATFLAG_MODELREAD, 8)
    noeassert('NFORMATFLAG_MODELWRITE', NFORMATFLAG_MODELWRITE, 16)
    noeassert('NMATFLAG_BLENDEDNORMALS', NMATFLAG_BLENDEDNORMALS, 16)
    noeassert('NMATFLAG_ENV_FLIP', NMATFLAG_ENV_FLIP, 1048576)
    noeassert('NMATFLAG_GAMMACORRECT', NMATFLAG_GAMMACORRECT, 8192)
    noeassert('NMATFLAG_KAJIYAKAY', NMATFLAG_KAJIYAKAY, 32)
    noeassert('NMATFLAG_NMAPSWAPRA', NMATFLAG_NMAPSWAPRA, 1)
    noeassert('NMATFLAG_NORMAL_UV1', NMATFLAG_NORMAL_UV1, 33554432)
    noeassert('NMATFLAG_NORMALMAP_FLIPY', NMATFLAG_NORMALMAP_FLIPY, 131072)
    noeassert('NMATFLAG_NORMALMAP_NODERZ', NMATFLAG_NORMALMAP_NODERZ, 262144)
    noeassert('NMATFLAG_PBR_ALBEDOENERGYCON', NMATFLAG_PBR_ALBEDOENERGYCON, 4194304)
    noeassert('NMATFLAG_PBR_COMPENERGYCON', NMATFLAG_PBR_COMPENERGYCON, 8388608)
    noeassert('NMATFLAG_PBR_METAL', NMATFLAG_PBR_METAL, 65536)
    noeassert('NMATFLAG_PBR_ROUGHNESS_NRMALPHA', NMATFLAG_PBR_ROUGHNESS_NRMALPHA, 536870912)
    noeassert('NMATFLAG_PBR_SPEC', NMATFLAG_PBR_SPEC, 32768)
    noeassert('NMATFLAG_PBR_SPEC_IR_RG', NMATFLAG_PBR_SPEC_IR_RG, 524288)
    noeassert('NMATFLAG_PREVIEWLOAD', NMATFLAG_PREVIEWLOAD, 4)
    noeassert('NMATFLAG_SORT01', NMATFLAG_SORT01, 64)
    noeassert('NMATFLAG_SPEC_UV1', NMATFLAG_SPEC_UV1, 67108864)
    noeassert('NMATFLAG_SPRITE_FACINGXY', NMATFLAG_SPRITE_FACINGXY, 16777216)
    noeassert('NMATFLAG_TWOSIDED', NMATFLAG_TWOSIDED, 2)
    noeassert('NMATFLAG_USELMUVS', NMATFLAG_USELMUVS, 8)
    noeassert('NMATFLAG_VCOLORSUBTRACT', NMATFLAG_VCOLORSUBTRACT, 16384)
    noeassert('NMSHAREDFL_BONEPALETTE', NMSHAREDFL_BONEPALETTE, 1024)
    noeassert('NMSHAREDFL_FLATWEIGHTS', NMSHAREDFL_FLATWEIGHTS, 8)
    noeassert('NMSHAREDFL_FLATWEIGHTS_FORCE4', NMSHAREDFL_FLATWEIGHTS_FORCE4, 16)
    noeassert('NMSHAREDFL_REVERSEWINDING', NMSHAREDFL_REVERSEWINDING, 32)
    noeassert('NMSHAREDFL_UNIQUEVERTS', NMSHAREDFL_UNIQUEVERTS, 256)
    noeassert('NMSHAREDFL_WANTGLOBALARRAY', NMSHAREDFL_WANTGLOBALARRAY, 2)
    noeassert('NMSHAREDFL_WANTNEIGHBORS', NMSHAREDFL_WANTNEIGHBORS, 1)
    noeassert('NMSHAREDFL_WANTTANGENTS', NMSHAREDFL_WANTTANGENTS, 4)
    noeassert('NMSHAREDFL_WANTTANGENTS4', NMSHAREDFL_WANTTANGENTS4, 64)
    noeassert('NMSHAREDFL_WANTTANGENTS4R', NMSHAREDFL_WANTTANGENTS4R, 128)
    noeassert('NOE_ENCODEDXT_BC1', NOE_ENCODEDXT_BC1, 0)
    noeassert('NOE_ENCODEDXT_BC3', NOE_ENCODEDXT_BC3, 1)
    noeassert('NOE_ENCODEDXT_BC4', NOE_ENCODEDXT_BC4, 2)
    noeassert('NOEBLEND_DST_ALPHA', NOEBLEND_DST_ALPHA, 7)
    noeassert('NOEBLEND_DST_COLOR', NOEBLEND_DST_COLOR, 9)
    noeassert('NOEBLEND_NONE', NOEBLEND_NONE, 0)
    noeassert('NOEBLEND_ONE', NOEBLEND_ONE, 2)
    noeassert('NOEBLEND_ONE_MINUS_DST_ALPHA', NOEBLEND_ONE_MINUS_DST_ALPHA, 8)
    noeassert('NOEBLEND_ONE_MINUS_DST_COLOR', NOEBLEND_ONE_MINUS_DST_COLOR, 10)
    noeassert('NOEBLEND_ONE_MINUS_SRC_ALPHA', NOEBLEND_ONE_MINUS_SRC_ALPHA, 6)
    noeassert('NOEBLEND_ONE_MINUS_SRC_COLOR', NOEBLEND_ONE_MINUS_SRC_COLOR, 4)
    noeassert('NOEBLEND_SRC_ALPHA', NOEBLEND_SRC_ALPHA, 5)
    noeassert('NOEBLEND_SRC_ALPHA_SATURATE', NOEBLEND_SRC_ALPHA_SATURATE, 11)
    noeassert('NOEBLEND_SRC_COLOR', NOEBLEND_SRC_COLOR, 3)
    noeassert('NOEBLEND_ZERO', NOEBLEND_ZERO, 1)
    noeassert('NOEFSMODE_READBINARY', NOEFSMODE_READBINARY, 0)
    noeassert('NOEFSMODE_READWRITEBINARY', NOEFSMODE_READWRITEBINARY, 2)
    noeassert('NOEFSMODE_WRITEBINARY', NOEFSMODE_WRITEBINARY, 1)
    noeassert('NOEKF_INTERPOLATE_LINEAR', NOEKF_INTERPOLATE_LINEAR, 0)
    noeassert('NOEKF_INTERPOLATE_NEAREST', NOEKF_INTERPOLATE_NEAREST, 1)
    noeassert('NOEKF_ROTATION_QUATERNION_4', NOEKF_ROTATION_QUATERNION_4, 0)
    noeassert('NOEKF_SCALE_SCALAR_1', NOEKF_SCALE_SCALAR_1, 0)
    noeassert('NOEKF_SCALE_SINGLE', NOEKF_SCALE_SINGLE, 1)
    noeassert('NOEKF_SCALE_TRANSPOSED_VECTOR_3', NOEKF_SCALE_TRANSPOSED_VECTOR_3, 3)
    noeassert('NOEKF_SCALE_VECTOR_3', NOEKF_SCALE_VECTOR_3, 2)
    noeassert('NOEKF_TRANSLATION_SINGLE', NOEKF_TRANSLATION_SINGLE, 1)
    noeassert('NOEKF_TRANSLATION_VECTOR_3', NOEKF_TRANSLATION_VECTOR_3, 0)
    noeassert('NOESIS_PLUGIN_VERSION', NOESIS_PLUGIN_VERSION, 3)
    noeassert('NOESIS_PLUGINAPI_VERSION', NOESIS_PLUGINAPI_VERSION, 73)
    noeassert('NOESISTEX_DXT1', NOESISTEX_DXT1, 3)
    noeassert('NOESISTEX_DXT3', NOESISTEX_DXT3, 4)
    noeassert('NOESISTEX_DXT5', NOESISTEX_DXT5, 5)
    noeassert('NOESISTEX_RGB24', NOESISTEX_RGB24, 2)
    noeassert('NOESISTEX_RGBA32', NOESISTEX_RGBA32, 1)
    noeassert('NOESISTEX_UNKNOWN', NOESISTEX_UNKNOWN, 0)
    noeassert('NOESPLINEFLAG_CLOSED', NOESPLINEFLAG_CLOSED, 1)
    noeassert('NOEUSERVAL_BOOL', NOEUSERVAL_BOOL, 4)
    noeassert('NOEUSERVAL_FILEPATH', NOEUSERVAL_FILEPATH, 5)
    noeassert('NOEUSERVAL_FLOAT', NOEUSERVAL_FLOAT, 2)
    noeassert('NOEUSERVAL_FOLDERPATH', NOEUSERVAL_FOLDERPATH, 6)
    noeassert('NOEUSERVAL_INT', NOEUSERVAL_INT, 3)
    noeassert('NOEUSERVAL_NONE', NOEUSERVAL_NONE, 0)
    noeassert('NOEUSERVAL_SAVEFILEPATH', NOEUSERVAL_SAVEFILEPATH, 7)
    noeassert('NOEUSERVAL_STRING', NOEUSERVAL_STRING, 1)
    noeassert('NSEQFLAG_NONLOOPING', NSEQFLAG_NONLOOPING, 1)
    noeassert('NSEQFLAG_REVERSE', NSEQFLAG_REVERSE, 2)
    noeassert('NTEXFLAG_CUBEMAP', NTEXFLAG_CUBEMAP, 256)
    noeassert('NTEXFLAG_FILTER_NEAREST', NTEXFLAG_FILTER_NEAREST, 16)
    noeassert('NTEXFLAG_HDRISLINEAR', NTEXFLAG_HDRISLINEAR, 2048)
    noeassert('NTEXFLAG_ISLINEAR', NTEXFLAG_ISLINEAR, 1024)
    noeassert('NTEXFLAG_ISNORMALMAP', NTEXFLAG_ISNORMALMAP, 1)
    noeassert('NTEXFLAG_PREVIEWLOAD', NTEXFLAG_PREVIEWLOAD, 128)
    noeassert('NTEXFLAG_SEGMENTED', NTEXFLAG_SEGMENTED, 2)
    noeassert('NTEXFLAG_STEREO', NTEXFLAG_STEREO, 4)
    noeassert('NTEXFLAG_STEREO_SWAP', NTEXFLAG_STEREO_SWAP, 8)
    noeassert('NTEXFLAG_WANTSEAMLESS', NTEXFLAG_WANTSEAMLESS, 4096)
    noeassert('NTEXFLAG_WRAP_CLAMP', NTEXFLAG_WRAP_CLAMP, 32)
    noeassert('NTEXFLAG_WRAP_MIRROR_CLAMP', NTEXFLAG_WRAP_MIRROR_CLAMP, 16384)
    noeassert('NTEXFLAG_WRAP_MIRROR_REPEAT', NTEXFLAG_WRAP_MIRROR_REPEAT, 8192)
    noeassert('NTEXFLAG_WRAP_REPEAT', NTEXFLAG_WRAP_REPEAT, 0)
    noeassert('NTOOLFLAG_CONTEXTITEM', NTOOLFLAG_CONTEXTITEM, 1)
    noeassert('NTOOLFLAG_USERBITS', NTOOLFLAG_USERBITS, -268435456)
    noeassert('NUM_NOE_BLENDS', NUM_NOE_BLENDS, 12)
    noeassert('NUM_NOEKF_INTERPOLATION_TYPES', NUM_NOEKF_INTERPOLATION_TYPES, 2)
    noeassert('NUM_NOEKF_ROTATION_TYPES', NUM_NOEKF_ROTATION_TYPES, 1)
    noeassert('NUM_NOEKF_SCALE_TYPES', NUM_NOEKF_SCALE_TYPES, 4)
    noeassert('NUM_NOEKF_TRANSLATION_TYPES', NUM_NOEKF_TRANSLATION_TYPES, 2)
    noeassert('NUM_RPGEO_DATATYPES', NUM_RPGEO_DATATYPES, 9)
    noeassert('NUM_RPGEO_TYPES', NUM_RPGEO_TYPES, 12)
    noeassert('OPTFLAG_WANTARG', OPTFLAG_WANTARG, 1)
    noeassert('PS2_VIFCODE_BASE', PS2_VIFCODE_BASE, 3)
    noeassert('PS2_VIFCODE_DIRECT', PS2_VIFCODE_DIRECT, 80)
    noeassert('PS2_VIFCODE_DIRECTHL', PS2_VIFCODE_DIRECTHL, 81)
    noeassert('PS2_VIFCODE_FLUSH', PS2_VIFCODE_FLUSH, 17)
    noeassert('PS2_VIFCODE_FLUSHA', PS2_VIFCODE_FLUSHA, 19)
    noeassert('PS2_VIFCODE_FLUSHE', PS2_VIFCODE_FLUSHE, 16)
    noeassert('PS2_VIFCODE_ITOP', PS2_VIFCODE_ITOP, 4)
    noeassert('PS2_VIFCODE_MARK', PS2_VIFCODE_MARK, 7)
    noeassert('PS2_VIFCODE_MPG', PS2_VIFCODE_MPG, 74)
    noeassert('PS2_VIFCODE_MSCAL', PS2_VIFCODE_MSCAL, 20)
    noeassert('PS2_VIFCODE_MSCALF', PS2_VIFCODE_MSCALF, 21)
    noeassert('PS2_VIFCODE_MSCNT', PS2_VIFCODE_MSCNT, 23)
    noeassert('PS2_VIFCODE_MSKPATH3', PS2_VIFCODE_MSKPATH3, 6)
    noeassert('PS2_VIFCODE_NOP', PS2_VIFCODE_NOP, 0)
    noeassert('PS2_VIFCODE_OFFSET', PS2_VIFCODE_OFFSET, 2)
    noeassert('PS2_VIFCODE_STCOL', PS2_VIFCODE_STCOL, 49)
    noeassert('PS2_VIFCODE_STCYCL', PS2_VIFCODE_STCYCL, 1)
    noeassert('PS2_VIFCODE_STMASK', PS2_VIFCODE_STMASK, 32)
    noeassert('PS2_VIFCODE_STMOD', PS2_VIFCODE_STMOD, 5)
    noeassert('PS2_VIFCODE_STROW', PS2_VIFCODE_STROW, 48)
    noeassert('PVRTC_DECODE_BICUBIC', PVRTC_DECODE_BICUBIC, 4)
    noeassert('PVRTC_DECODE_LINEARORDER', PVRTC_DECODE_LINEARORDER, 2)
    noeassert('PVRTC_DECODE_PVRTC2', PVRTC_DECODE_PVRTC2, 1)
    noeassert('PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA', PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA, 16)
    noeassert('PVRTC_DECODE_PVRTC2_ROTATE_BLOCK_PAL', PVRTC_DECODE_PVRTC2_ROTATE_BLOCK_PAL, 8)
    noeassert('RPGEO_NONE', RPGEO_NONE, 0)
    noeassert('RPGEO_POINTS', RPGEO_POINTS, 1)
    noeassert('RPGEO_POLYGON', RPGEO_POLYGON, 5)
    noeassert('RPGEO_QUAD', RPGEO_QUAD, 4)
    noeassert('RPGEO_QUAD_ABC_ACD', RPGEO_QUAD_ABC_ACD, 10)
    noeassert('RPGEO_QUAD_ABC_BCD', RPGEO_QUAD_ABC_BCD, 9)
    noeassert('RPGEO_QUAD_ABC_DCA', RPGEO_QUAD_ABC_DCA, 11)
    noeassert('RPGEO_QUAD_STRIP', RPGEO_QUAD_STRIP, 7)
    noeassert('RPGEO_TRIANGLE', RPGEO_TRIANGLE, 2)
    noeassert('RPGEO_TRIANGLE_FAN', RPGEO_TRIANGLE_FAN, 6)
    noeassert('RPGEO_TRIANGLE_STRIP', RPGEO_TRIANGLE_STRIP, 3)
    noeassert('RPGEO_TRIANGLE_STRIP_FLIPPED', RPGEO_TRIANGLE_STRIP_FLIPPED, 8)
    noeassert('RPGEODATA_BYTE', RPGEODATA_BYTE, 7)
    noeassert('RPGEODATA_DOUBLE', RPGEODATA_DOUBLE, 6)
    noeassert('RPGEODATA_FLOAT', RPGEODATA_FLOAT, 0)
    noeassert('RPGEODATA_HALFFLOAT', RPGEODATA_HALFFLOAT, 5)
    noeassert('RPGEODATA_INT', RPGEODATA_INT, 1)
    noeassert('RPGEODATA_SHORT', RPGEODATA_SHORT, 3)
    noeassert('RPGEODATA_UBYTE', RPGEODATA_UBYTE, 8)
    noeassert('RPGEODATA_UINT', RPGEODATA_UINT, 2)
    noeassert('RPGEODATA_USHORT', RPGEODATA_USHORT, 4)
    noeassert('RPGOPT_BIGENDIAN', RPGOPT_BIGENDIAN, 1)
    noeassert('RPGOPT_DERIVEBONEORIS', RPGOPT_DERIVEBONEORIS, 8)
    noeassert('RPGOPT_FILLINWEIGHTS', RPGOPT_FILLINWEIGHTS, 16)
    noeassert('RPGOPT_MORPH_RELATIVENORMALS', RPGOPT_MORPH_RELATIVENORMALS, 256)
    noeassert('RPGOPT_MORPH_RELATIVEPOSITIONS', RPGOPT_MORPH_RELATIVEPOSITIONS, 128)
    noeassert('RPGOPT_SWAPHANDEDNESS', RPGOPT_SWAPHANDEDNESS, 32)
    noeassert('RPGOPT_TANMATROTATE', RPGOPT_TANMATROTATE, 4)
    noeassert('RPGOPT_TRIWINDBACKWARD', RPGOPT_TRIWINDBACKWARD, 2)
    noeassert('RPGOPT_UNSAFE', RPGOPT_UNSAFE, 64)
    noeassert('RPGVUFLAG_NOREUSE', RPGVUFLAG_NOREUSE, 2)
    noeassert('RPGVUFLAG_PERINSTANCE', RPGVUFLAG_PERINSTANCE, 1)
    noeassert('SHAREDSTRIP_LIST', SHAREDSTRIP_LIST, 0)
    noeassert('SHAREDSTRIP_STRIP', SHAREDSTRIP_STRIP, 1)

    print('Methods')

    m11 = 2.5
    m12 = 3.6
    m13 = 4.7
    m14 = 5.8
    m21 = 2.9
    m22 = 3.1
    m23 = 4.3
    m24 = 5.2
    m31 = 2.5
    m32 = 3.6
    m33 = 4.7
    m34 = 5.3
    m41 = 1.1
    m42 = 2.4
    m43 = 3.2
    m44 = 4.1

    noeAngles = NoeAngles((m11, m12, m13))
    other = NoeAngles((m21, m22, m23))

    result = anglesAngleVectors(noeAngles)
    expected = NoeMat43((
        NoeVec3((0.9970768690109253, 0.06273075193166733, -0.04361938685178757)),
        NoeVec3((0.05901231989264488, -0.9948951601982117, -0.08186052739620209)),
        NoeVec3((0.04853188991546631, -0.07904715090990067, 0.9956888556480408)),
        NoeVec3((0.0, 0.0, 0.0))
    ))
    noeassert('anglesAngleVectors', result, expected)

    result = anglesNormalize180(noeAngles)
    expected = NoeAngles((2.5, 3.5999999046325684, 4.699999809265137))
    noeassert('anglesNormalize180', result, expected)

    result = anglesNormalize360(noeAngles)
    expected = NoeAngles((2.5, 3.5999999046325684, 4.699999809265137))
    noeassert('anglesNormalize360', result, expected)

    result = anglesToMat43(noeAngles)
    expected = NoeMat43((
        NoeVec3((0.9946707487106323, -0.06629780679941177, 0.0789601057767868)),
        NoeVec3((0.06257937103509903, 0.9968523979187012, 0.04867337644100189)),
        NoeVec3((-0.08193850517272949, -0.043472710996866226, 0.9956888556480408)),
        NoeVec3((0.0, 0.0, 0.0))
    ))
    noeassert('anglesToMat43', result, expected)

    result = anglesToQuat(noeAngles)
    expected = NoeQuat((0.023073436692357063, -0.04028910771012306, -0.032270923256874084, 0.9984001517295837))
    noeassert('anglesToQuat', result, expected)

    result = anglesToVec3(noeAngles)
    expected = NoeVec3((0.9970768690109253, 0.06273075193166733, -0.04361938685178757))
    noeassert('anglesToVec3', result, expected)

    noeMat43 = NoeMat43((
        NoeVec3((m11, m12, m13)),
        NoeVec3((m21, m22, m23)),
        NoeVec3((m31, m32, m33)),
        NoeVec3((m41, m42, m43))
    ))
    other = NoeMat43((
        NoeVec3((m11, m12, m13)),
        NoeVec3((m21, m22, m23)),
        NoeVec3((m31, m32, m33)),
        NoeVec3((m41, m42, m43))
    ))

    result = mat43Add(noeMat43, other)
    expected = NoeMat43((
        NoeVec3((5.0, 7.199999809265137, 9.399999618530273)),
        NoeVec3((5.800000190734863, 6.199999809265137, 8.600000381469727)),
        NoeVec3((5.0, 7.199999809265137, 9.399999618530273)),
        NoeVec3((2.200000047683716, 4.800000190734863, 6.400000095367432))
    ))
    noeassert('mat43Add', result, expected)

    result = mat43Inverse(noeMat43)
    expected = NoeMat43((
        NoeVec3((0.11956002563238144, 0.13868963718414307, 0.11956002563238144)),
        NoeVec3((0.10132283717393875, 0.08725021779537201, 0.10132283717393875)),
        NoeVec3((0.07499600201845169, 0.06861337274312973, 0.07499600201845169)),
        NoeVec3((-0.8469632863998413, -0.6450887322425842, -0.48715493083000183))
    ))
    noeassert('mat43Inverse', result, expected)

    result = mat43IsSkewed(noeMat43)
    expected = 1
    noeassert('mat43IsSkewed', result, expected)

    result = mat43Mul(noeMat43, other)
    expected = NoeMat43((
        NoeVec3((28.440000534057617, 37.07999801635742, 49.31999969482422)),
        NoeVec3((26.990001678466797, 35.529998779296875, 47.17000198364258)),
        NoeVec3((28.440000534057617, 37.07999801635742, 49.31999969482422)),
        NoeVec3((27.530000686645508, 26.790000915527344, 29.6299991607666))
    ))
    noeassert('mat43Mul', result, expected)

    result = mat43Orthogonalize(noeMat43)
    expected = NoeMat43((
        NoeVec3((0.38901376724243164, 0.5601798295974731, 0.7313458919525146)),
        NoeVec3((0.8933345079421997, -0.42327600717544556, -0.1509665995836258)),
        NoeVec3((0.0, 0.0, 0.0)),
        NoeVec3((1.100000023841858, 2.4000000953674316, 3.200000047683716))
    ))
    noeassert('mat43Orthogonalize', result, expected)

    result = mat43Sub(noeMat43, other)
    expected = NoeMat43((
        NoeVec3((0.0, 0.0, 0.0)),
        NoeVec3((0.0, 0.0, 0.0)),
        NoeVec3((0.0, 0.0, 0.0)),
        NoeVec3((0.0, 0.0, 0.0))
    ))
    noeassert('mat43Sub', result, expected)

    result = mat43ToAngles(noeMat43)
    expected = NoeAngles((0.0, 310.73211669921875, 270.0))
    noeassert('mat43ToAngles', result, expected)

    result = mat43ToBytes(noeMat43)
    expected = bytearray(b'\x00\x00 @fff@ff\x96@\x9a\x999@ffF@\x9a\x99\x89@\x00\x00 @fff@ff\x96@\xcd\xcc\x8c?\x9a\x99\x19@\xcd\xccL@')
    noeassert('mat43ToAngles', result, expected)

    result = mat43ToMat44(noeMat43)
    expected = NoeMat44((
        NoeVec4((2.5, 2.9000000953674316, 2.5, 0.0)),
        NoeVec4((3.5999999046325684, 3.0999999046325684, 3.5999999046325684, 0.0)),
        NoeVec4((4.699999809265137, 4.300000190734863, 4.699999809265137, 0.0)),
        NoeVec4((1.100000023841858, 2.4000000953674316, 3.200000047683716, 1.0))
    ))
    noeassert('mat43ToMat44', result, expected)

    result = mat43ToQuat(noeMat43)
    expected = NoeQuat((0.046668071299791336, -0.10547725856304169, 0.024721255525946617, 0.8113884925842285))
    noeassert('mat43ToQuat', result, expected)

    result = mat43Transpose(noeMat43)
    expected = NoeMat43((
        NoeVec3((2.5, 2.9000000953674316, 2.5)),
        NoeVec3((3.5999999046325684, 3.0999999046325684, 3.5999999046325684)),
        NoeVec3((4.699999809265137, 4.300000190734863, 4.699999809265137)),
        NoeVec3((1.100000023841858, 2.4000000953674316, 3.200000047683716))
    ))
    noeassert('mat43Transpose', result, expected)

    noeMat44 = NoeMat44((
        NoeVec4(((m11, m12, m13, m14))),
        NoeVec4(((m21, m22, m23, m24))),
        NoeVec4(((m31, m32, m33, m34))),
        NoeVec4(((m41, m42, m43, m44)))
    ))
    other = NoeMat44((
        NoeVec4(((m11, m12, m13, m14))),
        NoeVec4(((m21, m22, m23, m24))),
        NoeVec4(((m31, m32, m33, m34))),
        NoeVec4(((m41, m42, m43, m44)))
    ))

    result = mat44Add(noeMat44, other)
    expected = NoeMat44((
        NoeVec4((5.0, 7.199999809265137, 9.399999618530273, 11.600000381469727)),
        NoeVec4((5.800000190734863, 6.199999809265137, 8.600000381469727, 10.399999618530273)),
        NoeVec4((5.0, 7.199999809265137, 9.399999618530273, 10.600000381469727)),
        NoeVec4((2.200000047683716, 4.800000190734863, 6.400000095367432, 8.199999809265137))
    ))
    noeassert('mat44Add', result, expected)

    result = mat44Inverse(noeMat44)
    expected = NoeMat44((
        NoeVec4((1.0446702241897583, 0.34531402587890625, -0.4690943956375122, -1.309409260749817)),
        NoeVec4((6.932554244995117, -4.072056293487549, -0.3856006860733032, -4.143986225128174)),
        NoeVec4((-8.121102333068848, 2.9353432655334473, 3.0130395889282227, 3.8706283569335938)),
        NoeVec4((2.0000646114349365, -2.3108409550332e-06, -2.0000531673431396, -1.0429002372802643e-07))
    ))
    noeassert('mat44Inverse', result, expected)

    result = mat44Mul(noeMat44, other)
    expected = NoeMat44((
        NoeVec4((34.81999969482422, 51.0, 67.87999725341797, 81.90999603271484)),
        NoeVec4((32.709999084472656, 48.0099983215332, 63.810001373291016, 77.05000305175781)),
        NoeVec4((34.27000045776367, 49.79999923706055, 66.27999877929688, 79.86000061035156)),
        NoeVec4((22.220001220703125, 32.7599983215332, 43.650001525878906, 52.630001068115234))
    ))
    noeassert('mat44Mul', result, expected)

    result = mat44Sub(noeMat44, other)
    expected = NoeMat44((
        NoeVec4((0.0, 0.0, 0.0, 0.0)),
        NoeVec4((0.0, 0.0, 0.0, 0.0)),
        NoeVec4((0.0, 0.0, 0.0, 0.0)),
        NoeVec4((0.0, 0.0, 0.0, 0.0))
    ))
    noeassert('mat44Sub', result, expected)

    result = mat44ToBytes(noeMat44)
    expected = bytearray(b'\x00\x00 @fff@ff\x96@\x9a\x99\xb9@\x9a\x999@ffF@\x9a\x99\x89@ff\xa6@\x00\x00 @fff@ff\x96@\x9a\x99\xa9@\xcd\xcc\x8c?\x9a\x99\x19@\xcd\xccL@33\x83@')
    noeassert('mat44ToBytes', result, expected)

    result = mat44ToMat43(noeMat44)
    expected = NoeMat43((
        NoeVec3((2.5, 2.9000000953674316, 2.5)),
        NoeVec3((3.5999999046325684, 3.0999999046325684, 3.5999999046325684)),
        NoeVec3((4.699999809265137, 4.300000190734863, 4.699999809265137)),
        NoeVec3((1.100000023841858, 2.4000000953674316, 3.200000047683716))
    ))
    noeassert('mat44ToMat43', result, expected)

    result = mat44Transpose(noeMat44)
    expected = NoeMat44((
        NoeVec4((2.5, 2.9000000953674316, 2.5, 1.100000023841858)),
        NoeVec4((3.5999999046325684, 3.0999999046325684, 3.5999999046325684, 2.4000000953674316)),
        NoeVec4((4.699999809265137, 4.300000190734863, 4.699999809265137, 3.200000047683716)),
        NoeVec4((5.800000190734863, 5.199999809265137, 5.300000190734863, 4.099999904632568))
    ))
    noeassert('mat44Transpose', result, expected)

    noeQuat3 = NoeQuat3()
    other = NoeQuat3()

    result = quat3ToBytes(noeQuat3)
    expected = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    noeassert('quat3ToBytes', result, expected)

    result = quat3ToQuat(noeQuat3)
    expected = NoeQuat((0.0, 0.0, 0.0, 1.0))
    noeassert('quat3ToQuat', result, expected)

    noeQuat = NoeQuat((m11, m12, m13, m14))
    other = NoeQuat((m21, m22, m23, m24))

    result = quatAdd(noeQuat, other)
    expected = NoeQuat((5.400000095367432, 6.699999809265137, 9.0, 11.0))
    noeassert('quatAdd', result, expected)

    result = quatLen(noeQuat)
    expected = 8.656789779663086
    noeassert('quatLen', result, expected)

    result = quatMul(noeQuat, other)
    expected = NoeQuat((30.73000144958496, 39.57999801635742, 46.689998626708984, -8.460000038146973))
    noeassert('quatMul', result, expected)

    result = quatNormalize(noeQuat)
    expected = NoeQuat((0.28879064321517944, 0.41585853695869446, 0.5429264307022095, 0.6699943542480469))
    noeassert('quatNormalize', result, expected)

    result = quatSub(noeQuat, other)
    expected = NoeQuat((-0.40000009536743164, 0.5, 0.39999961853027344, 0.6000003814697266))
    noeassert('quatSub', result, expected)

    result = quatToAngles(noeQuat)
    expected = NoeAngles((0.0, 232.48338317871094, 270.0))
    noeassert('quatToAngles', result, expected)

    result = quatToBytes(noeQuat)
    expected = bytearray(b'\x00\x00 @fff@ff\x96@\x9a\x99\xb9@')
    noeassert('quatToBytes', result, expected)

    result = quatToQuat3(noeQuat)
    expected = NoeQuat3((2.5, 3.5999999046325684, 4.699999809265137))
    noeassert('quatToQuat3', result, expected)

    result = quatTranspose(noeQuat)
    expected = NoeQuat((0.1489858776330948, 0.3312559127807617, 0.6690264344215393, -0.43000486493110657))
    noeassert('quatTranspose', result, expected)

    noeVec3 = NoeVec3((m11, m12, m13))
    other = NoeVec3((m21, m22, m23))

    result = vec3Add(noeVec3, other)
    expected = NoeVec3((5.400000095367432, 6.699999809265137, 9.0))
    noeassert('vec3Add', result, expected)

    result = vec3Cross(noeVec3, other)
    expected = NoeVec3((0.9100013375282288, 2.8799993991851807, -2.690000295639038))
    noeassert('vec3Cross', result, expected)

    result = vec3Div(noeVec3, other)
    expected = NoeVec3((0.8620689511299133, 1.1612902879714966, 1.0930231809616089))
    noeassert('vec3Div', result, expected)

    result = vec3Len(noeVec3)
    expected = 6.426507472991943
    noeassert('vec3Len', result, expected)

    result = vec3LenSq(noeVec3)
    expected = 41.29999923706055
    noeassert('vec3LenSq', result, expected)

    result = vec3Mul(noeVec3, other)
    expected = NoeVec3((7.25, 11.159998893737793, 20.21000099182129))
    noeassert('vec3Mul', result, expected)

    result = vec3Norm(noeVec3)
    expected = NoeVec3((0.38901376724243164, 0.5601798295974731, 0.7313458919525146))
    noeassert('vec3Norm', result, expected)

    result = vec3Sub(noeVec3, other)
    expected = NoeVec3((-0.40000009536743164, 0.5, 0.39999961853027344))
    noeassert('vec3Sub', result, expected)

    result = vec3ToAngles(noeVec3)
    expected = NoeAngles((-46.99934387207031, 55.22216796875, 0.0))
    noeassert('vec3ToAngles', result, expected)

    result = vec3ToBytes(noeVec3)
    expected = bytearray(b'\x00\x00 @fff@ff\x96@')
    noeassert('vec3ToBytes', result, expected)

    result = vec3ToMat43(noeVec3)
    expected = NoeMat43((
        NoeVec3((2.5, 3.5999999046325684, 4.699999809265137)),
        NoeVec3((-0.821370005607605, 0.570395827293396, 0.0)),
        NoeVec3((-2.6808602809906006, -3.860438823699951, 4.3829216957092285)),
        NoeVec3((0.0, 0.0, 0.0))
    ))
    noeassert('vec3ToMat43', result, expected)

    result = vec3ToVec4(noeVec3)
    expected = NoeVec4((2.5, 3.5999999046325684, 4.699999809265137, 0.0))
    noeassert('vec3ToVec4', result, expected)

    noeVec4 = NoeVec4((m11, m12, m13, m14))
    other = NoeVec4((m21, m22, m23, m24))

    result = vec4Add(noeVec4, other)
    expected = NoeVec4((5.400000095367432, 6.699999809265137, 9.0, 11.0))
    noeassert('vec4Add', result, expected)

    result = vec4Div(noeVec4, other)
    expected = NoeVec4((0.8620689511299133, 1.1612902879714966, 1.0930231809616089, 1.34883713722229))
    noeassert('vec4Div', result, expected)

    result = vec4Dot(noeVec4, other)
    expected = 68.77999877929688
    noeassert('vec4Dot', result, expected)

    result = vec4Len(noeVec4)
    expected = 8.656789779663086
    noeassert('vec4Len', result, expected)

    result = vec4LenSq(noeVec4)
    expected = 74.94000244140625
    noeassert('vec4LenSq', result, expected)

    result = vec4Mul(noeVec4, other)
    expected = NoeVec4((7.25, 11.159998893737793, 20.21000099182129, 30.15999984741211))
    noeassert('vec4Mul', result, expected)

    result = vec4Norm(noeVec4)
    expected = NoeVec4((0.28879064321517944, 0.41585853695869446, 0.5429264307022095, 0.6699943542480469))
    noeassert('vec4Norm', result, expected)

    result = vec4Sub(noeVec4, other)
    expected = NoeVec4((-0.40000009536743164, 0.5, 0.39999961853027344, 0.6000003814697266))
    noeassert('vec4Sub', result, expected)

    result = vec4ToBytes(noeVec4)
    expected = bytearray(b'\x00\x00 @fff@ff\x96@\x9a\x99\xb9@')
    noeassert('vec4ToBytes', result, expected)

    result = vec4ToVec3(noeVec4)
    expected = NoeVec3((2.5, 3.5999999046325684, 4.699999809265137))
    noeassert('vec4ToVec3', result, expected)

    return 1
