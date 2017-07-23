from NoeBitStream import NoeBitStream
from NoeMaterial import NoeMaterial
from NoeModelMaterials import NoeModelMaterials
from NoeVec4 import NoeVec4
from NoeTexture import NoeTexture
import noesis

NOESEEK_ABS = 0
NOESEEK_CURRENT = 1 # TODO: verify name and value here
NOESEEK_END = 2 # TODO: verify name and value here
NOE_BIGENDIAN = 'NOE_BIGENDIAN' # TODO: check value

# TODO: check implementation
def noeStrFromBytes(bytes):
    return bytes
