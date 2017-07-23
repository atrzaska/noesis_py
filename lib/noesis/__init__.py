from Noesis import Noesis

RPGEODATA_FLOAT = 4
RPGEODATA_INT = 4
RPGEODATA_USHORT = 2
RPGEO_TRIANGLE = 'RPGEO_TRIANGLE' # TODO: check value
RPGEO_TRIANGLE_STRIP = 'RPGEO_TRIANGLE_STRIP' # TODO: check value
NOESISTEX_RGBA32 = 'NOESISTEX_RGBA32' # TODO: check value
NOEKF_ROTATION_QUATERNION_4 = 'NOEKF_ROTATION_QUATERNION_4' # TODO: check value
NOEKF_INTERPOLATE_LINEAR = 'NOEKF_INTERPOLATE_LINEAR' # TODO: check value
NOEKF_TRANSLATION_VECTOR_3 = 'NOEKF_TRANSLATION_VECTOR_3' # TODO: check value
NOEKF_SCALE_SCALAR_1 = 'NOEKF_SCALE_SCALAR_1' # TODO: check value
OPTFLAG_WANTARG = 'OPTFLAG_WANTARG' # TODO: check value

noesis = Noesis()

def register(name, fileType):
    return noesis.register(name, fileType)

def setHandlerTypeCheck(handle, noepyCheckType):
    return noesis.setHandlerTypeCheck(handle, noepyCheckType)

def setHandlerLoadModel(handle, noepyLoadModel):
    return noesis.setHandlerLoadModel(handle, noepyLoadModel)

def setHandlerLoadRGBA(handle, dsgLoadRGBA):
    return noesis.setHandlerLoadRGBA(handle, dsgLoadRGBA)

def setHandlerExtractArc(handle, grpExtractArc):
    return noesis.setHandlerExtractArc(handle, grpExtractArc)

def setHandlerWriteRGBA(handle, walWriteRGBA):
    return noesis.setHandlerWriteRGBA(handle, walWriteRGBA)

def allocType(type, data):
    return noesis.allocType(type, data)

def logPopup():
    return noesis.logPopup()

def addOption(handle, option, description, flags):
    return noesis.addOption(handle, option, description, flags)
