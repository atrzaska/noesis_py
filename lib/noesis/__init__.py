from Noesis import Noesis

BLITFLAG_ALPHABLEND = 'BLITFLAG_ALPHABLEND' # TODO: check value
FOURCC_ATI1 = 'FOURCC_ATI1' # TODO: check value
FOURCC_ATI2 = 'FOURCC_ATI2' # TODO: check value
FOURCC_DXT1 = 'FOURCC_DXT1' # TODO: check value
FOURCC_DXT1NORMAL = 'FOURCC_DXT1NORMAL' # TODO: check value
NFORMATFLAG_IMGREAD = 'NFORMATFLAG_IMGREAD' # TODO: check value
NFORMATFLAG_MODELREAD = 'NFORMATFLAG_MODELREAD' # TODO: check value
NMATFLAG_ENV_FLIP = 'NMATFLAG_ENV_FLIP' # TODO: check value
NMATFLAG_PBR_METAL = 'NMATFLAG_PBR_METAL' # TODO: check value
NMATFLAG_PBR_ROUGHNESS_NRMALPHA = 'NMATFLAG_PBR_ROUGHNESS_NRMALPHA' # TODO: check value
NMATFLAG_PBR_SPEC_IR_RG = 'NMATFLAG_PBR_SPEC_IR_RG' # TODO: check value
NMATFLAG_TWOSIDED = 'NMATFLAG_TWOSIDED' # TODO: check value
NOE_ENCODEDXT_BC1 = 'NOE_ENCODEDXT_BC1' # TODO: check value
NOEKF_INTERPOLATE_LINEAR = 'NOEKF_INTERPOLATE_LINEAR' # TODO: check value
NOEKF_ROTATION_QUATERNION_4 = 'NOEKF_ROTATION_QUATERNION_4' # TODO: check value
NOEKF_SCALE_SCALAR_1 = 'NOEKF_SCALE_SCALAR_1' # TODO: check value
NOEKF_TRANSLATION_VECTOR_3 = 'NOEKF_TRANSLATION_VECTOR_3' # TODO: check value
NOESISTEX_DXT1 = 'NOESISTEX_DXT1' # TODO: check value
NOESISTEX_DXT3 = 'NOESISTEX_DXT3' # TODO: check value
NOESISTEX_DXT5 = 'NOESISTEX_DXT5' # TODO: check value
NOESISTEX_RGB24 = 'NOESISTEX_RGB24' # TODO: check value
NOESISTEX_RGBA32 = 'NOESISTEX_RGBA32' # TODO: check value
NOESISTEX_UNKNOWN = 'NOESISTEX_UNKNOWN' # TODO: check value
NOEUSERVAL_SAVEFILEPATH = 'NOEUSERVAL_SAVEFILEPATH' # TODO: check value
NOEUSERVAL_STRING = 'NOEUSERVAL_STRING' # TODO: check value
NTEXFLAG_CUBEMAP = 'NTEXFLAG_CUBEMAP' # TODO: check value
NTEXFLAG_FILTER_NEAREST = 'NTEXFLAG_FILTER_NEAREST' # TODO: check value
NTEXFLAG_WRAP_CLAMP = 'NTEXFLAG_WRAP_CLAMP' # TODO: check value
NTOOLFLAG_CONTEXTITEM = 'NTOOLFLAG_CONTEXTITEM' # TODO: check value
OPTFLAG_WANTARG = 'OPTFLAG_WANTARG' # TODO: check value
PVRTC_DECODE_LINEARORDER = 'PVRTC_DECODE_LINEARORDER' # TODO: check value
PVRTC_DECODE_PVRTC2 = 'PVRTC_DECODE_PVRTC2' # TODO: check value
PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA = 'PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA' # TODO: check value
RPGEO_QUAD_ABC_ACD = 'RPGEO_QUAD_ABC_ACD' # TODO: check value
RPGEO_TRIANGLE = 'RPGEO_TRIANGLE' # TODO: check value
RPGEO_TRIANGLE_STRIP = 'RPGEO_TRIANGLE_STRIP' # TODO: check value
RPGEODATA_BYTE = 1
RPGEODATA_FLOAT = 4
RPGEODATA_HALFFLOAT = 2
RPGEODATA_INT = 4
RPGEODATA_SHORT = 2
RPGEODATA_UBYTE = 1
RPGEODATA_UINT = 4
RPGEODATA_USHORT = 2
RPGOPT_BIGENDIAN = 'RPGOPT_BIGENDIAN' # TODO: check value
RPGOPT_SWAPHANDEDNESS = 'RPGOPT_SWAPHANDEDNESS' # TODO: check value
RPGOPT_TANMATROTATE = 'RPGOPT_TANMATROTATE' # TODO: check value
RPGOPT_TRIWINDBACKWARD = 'RPGOPT_TRIWINDBACKWARD' # TODO: check value
g_flDegToRad = 'g_flDegToRad' # TODO: check value
g_flRadToDeg = 'g_flRadToDeg' # TODO: check value

noesis = Noesis()

def addOption(handle, option, description, flags):
    return noesis.addOption(handle, option, description, flags)

def allocBytes(size):
    return noesis.allocBytes(size)

def doException(error):
    return noesis.doException(error)

def freeModule(module):
    return noesis.freeModule(module)

def getCharSplineSet():
    return noesis.getCharSplineSet()

def getFormatExtensionFlags():
    return noesis.getFormatExtensionFlags()

def getMFFP(uint):
    return noesis.getMFFP(uint)

def getScenesPath():
    return noesis.getScenesPath()

def getSelectedDirectory():
    return noesis.getSelectedDirectory()

def getSelectedFile():
    return noesis.getSelectedFile()

def getWindowHandle():
    return noesis.getWindowHandle()

def instantiateModule():
    return noesis.instantiateModule()

def isPreviewModuleRAPIValid():
    return noesis.isPreviewModuleRAPIValid()

def loadImageRGBA():
    return noesis.loadImageRGBA()

def logPopup():
    return noesis.logPopup()

def messagePrompt():
    return noesis.messagePrompt()

def openAndRemoveTempFile():
    return noesis.openAndRemoveTempFile()

def openFile():
    return noesis.openFile()

def optGetArg():
    return noesis.optGetArg()

def optWasInvoked():
    return noesis.optWasInvoked()

def register(name, fileType):
    return noesis.register(name, fileType)

def registerCleanupFunction():
    return noesis.registerCleanupFunction()

def registerTool():
    return noesis.registerTool()

def setHandlerExtractArc(handle, grpExtractArc):
    return noesis.setHandlerExtractArc(handle, grpExtractArc)

def setHandlerLoadModel(handle, noepyLoadModel):
    return noesis.setHandlerLoadModel(handle, noepyLoadModel)

def setHandlerLoadRGBA(handle, dsgLoadRGBA):
    return noesis.setHandlerLoadRGBA(handle, dsgLoadRGBA)

def setHandlerTypeCheck(handle, noepyCheckType):
    return noesis.setHandlerTypeCheck(handle, noepyCheckType)

def setHandlerWriteModel(self, handle, noepyWriteModel):
    return noesis.setHandlerWriteModel(handle, noepyWriteModel)

def setHandlerWriteRGBA(handle, walWriteRGBA):
    return noesis.setHandlerWriteRGBA(handle, walWriteRGBA)

def setHandlerWriteAnim(handle, noepyWriteAnim):
    return noesis.setHandlerWriteAnim(handle, noepyWriteAnim)

def setModuleRAPI():
    return noesis.setModuleRAPI()

def setPreviewModuleRAPI():
    return noesis.setPreviewModuleRAPI()

def setToolFlags():
    return noesis.setToolFlags()

def setToolVisibleCallback():
    return noesis.setToolVisibleCallback()

def userPrompt():
    return noesis.userPrompt()
