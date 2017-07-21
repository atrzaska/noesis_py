from Noesis import Noesis
from fmt_MikuMikuDance_pmd import registerNoesisTypes

RPGEODATA_FLOAT = 4
RPGEODATA_USHORT = 2
RPGEO_TRIANGLE = 3

noesis = Noesis()

def register(name, fileType):
    return noesis.register(name, fileType)

def setHandlerTypeCheck(handle, noepyCheckType):
    noesis.setHandlerTypeCheck(handle, noepyCheckType)


def setHandlerLoadModel(handle, noepyLoadModel):
    noesis.setHandlerLoadModel(handle, noepyLoadModel)

def noepyLoadModelRPG():
    noesis.noepyLoadModelRPG()

# registerNoesisTypes()
# file = open('/Users/andrzej/Downloads/miku/model.pmd', 'rb')
# noesis.plugins[0].noepyLoadModel(file, noesis.mdlList)
# print(len(noesis.plugins))
