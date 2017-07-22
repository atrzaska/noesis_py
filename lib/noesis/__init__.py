from Noesis import Noesis

RPGEODATA_FLOAT = 4
RPGEODATA_USHORT = 2
RPGEO_TRIANGLE = 'RPGEO_TRIANGLE' # TODO: check value
RPGEO_TRIANGLE_STRIP = 'RPGEO_TRIANGLE_STRIP' # TODO: check value
NOESISTEX_RGBA32 = 'NOESISTEX_RGBA32' # TODO: check value

noesis = Noesis()

def register(name, fileType):
    return noesis.register(name, fileType)

def setHandlerTypeCheck(handle, noepyCheckType):
    return noesis.setHandlerTypeCheck(handle, noepyCheckType)

def setHandlerLoadModel(handle, noepyLoadModel):
    return noesis.setHandlerLoadModel(handle, noepyLoadModel)

def noepyLoadModelRPG():
    return noesis.noepyLoadModelRPG()
