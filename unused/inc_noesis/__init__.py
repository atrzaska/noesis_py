import struct

from NoeBitStream import NoeBitStream
from NoeMaterial import NoeMaterial
from NoeModelMaterials import NoeModelMaterials
from NoeVec4 import NoeVec4
from NoeTexture import NoeTexture
from NoeModule import NoeModule
import noesis

noeUnpack = struct.unpack
noeUnpackFrom = struct.unpack_from
noePack = struct.pack

NOESEEK_ABS = 0
NOESEEK_REL = 1
NOE_BIGENDIAN = 1
NOE_LITTLEENDIAN = 0

# TODO: check implementation
def noeStrFromBytes(bytes):
    return bytes

def noeTupleToList(tup):
    return [item for item in tup]

class NoeVec3:
    def __init__(self, vec3 = (0.0, 0.0, 0.0)):
        self.vec3 = vec3
        # noesis.vec3Validate(self)
    def __getitem__(self, index):
        return self.vec3[index]
    def __setitem__(self, index, value):
        if isinstance(self.vec3, tuple):
            self.vec3 = noeTupleToList(self.vec3)
        self.vec3[index] = value
    def __repr__(self):
        return repr(self.vec3)
    def __len__(self):
        return len(self.vec3)
    def binaryCompare(self, other):
        return self.vec3[0] == other.vec3[0] and self.vec3[1] == other.vec3[1] and self.vec3[2] == other.vec3[2]
    def __eq__(self, other):
        return self.binaryCompare(other)
    def __ne__(self, other):
        return not self.binaryCompare(other)

    def __add__(self, other):
        if isinstance(other, (NoeVec3, list, tuple)):
            return noesis.vec3Add(self, other)
        else:
            return NoeVec3([self.vec3[0]+other, self.vec3[1]+other, self.vec3[2]+other])
    def __sub__(self, other):
        if isinstance(other, (NoeVec3, list, tuple)):
            return noesis.vec3Sub(self, other)
        else:
            return NoeVec3([self.vec3[0]-other, self.vec3[1]-other, self.vec3[2]-other])
    def __mul__(self, other):
        if isinstance(other, (NoeVec3, list, tuple)):
            return noesis.vec3Mul(self, other)
        elif isinstance(other, NoeMat43):
            return noesis.mat43TransformPoint(other, self)
        elif isinstance(other, NoeQuat):
            return noesis.quatTransformPoint(other, self)
        else:
            return NoeVec3([self.vec3[0]*other, self.vec3[1]*other, self.vec3[2]*other])
    def __div__(self, other):
        if isinstance(other, (NoeVec3, list, tuple)):
            return noesis.vec3Div(self, other)
        else:
            return NoeVec3([self.vec3[0]/other, self.vec3[1]/other, self.vec3[2]/other])
    def __truediv__(self, other):
        if isinstance(other, (NoeVec3, list, tuple)):
            return noesis.vec3Div(self, other)
        else:
            return NoeVec3([self.vec3[0]/other, self.vec3[1]/other, self.vec3[2]/other])
    def __neg__(self):
        return NoeVec3([-self.vec3[0], -self.vec3[1], -self.vec3[2]])

    def dot(self, other): #returns float
        return noesis.vec3Dot(self, other)
    def cross(self, other): #returns vector
        return noesis.vec3Cross(self, other)
    def length(self): #returns float
        return noesis.vec3Len(self)
    def lengthSq(self): #returns float
        return noesis.vec3LenSq(self)
    def normalize(self): #returns vector
        return noesis.vec3Norm(self)
    def lerp(self, other, fraction): #returns vector
        return noesis.vec3Lerp(self, other, fraction)

    def toAngles(self):
        return noesis.vec3ToAngles(self)
    def toVec4(self):
        return noesis.vec3ToVec4(self)
    def toMat43(self):
        return noesis.vec3ToMat43(self)
    def toAnglesDirect(self):
        return NoeAngles([self.vec3[0], self.vec3[1], self.vec3[2]])
    def toBytes(self): #returns bytearray
        return noesis.vec3ToBytes(self)
    def fromBytes(otherBytes, bigEnd = NOE_LITTLEENDIAN): #returns type built from binary
        return noesis.vec3FromBytes(otherBytes, bigEnd)
    def getStorage(self): #returns raw storage (list, tuple, etc)
        return self.vec3

identityMat43Tuple = ( NoeVec3((1.0, 0.0, 0.0)), NoeVec3((0.0, 1.0, 0.0)), NoeVec3((0.0, 0.0, 1.0)), NoeVec3((0.0, 0.0, 0.0)) )
identityMat44Tuple = ( NoeVec4((1.0, 0.0, 0.0, 0.0)), NoeVec4((0.0, 1.0, 0.0, 0.0)), NoeVec4((0.0, 0.0, 1.0, 0.0)), NoeVec4((0.0, 0.0, 0.0, 1.0)) )

class NoeMat43:
    def __init__(self, mat43 = identityMat43Tuple):
        self.mat43 = mat43
        # noesis.mat43Validate(self)
    def __getitem__(self, index):
        return self.mat43[index]
    def __setitem__(self, index, value):
        if isinstance(self.mat43, tuple):
            self.mat43 = noeTupleToList(self.mat43)
        self.mat43[index] = value
    def __repr__(self):
        return repr(self.mat43)
    def __len__(self):
        return len(self.mat43)
    def binaryCompare(self, other):
        return self.mat43[0] == other.mat43[0] and self.mat43[1] == other.mat43[1] and self.mat43[2] == other.mat43[2] and self.mat43[3] == other.mat43[3]
    def __eq__(self, other):
        return self.binaryCompare(other)
    def __ne__(self, other):
        return not self.binaryCompare(other)

    def __add__(self, other):
        return noesis.mat43Add(self, other)
    def __sub__(self, other):
        return noesis.mat43Sub(self, other)
    def __mul__(self, other):
        if isinstance(other, (NoeMat43, list, tuple)):
            return noesis.mat43Mul(self, other)
        elif isinstance(other, NoeVec3):
            return noesis.mat43TransformPoint(self, other)
        elif isinstance(other, NoeVec4):
            return noesis.mat43TransformVec4(self, other)
        else:
            return NoeMat43([self.mat43[0]*other, self.mat43[1]*other, self.mat43[2]*other, self.mat43[3]*other])
    def __neg__(self):
        return NoeMat43([-self.mat43[0], -self.mat43[1], -self.mat43[2], -self.mat43[3]])

    def transformPoint(self, other): #returns vec3
        return noesis.mat43TransformPoint(self, other)
    def transformNormal(self, other): #returns vec3
        return noesis.mat43TransformNormal(self, other)
    def transformVec4(self, other): #returns vec4
        return noesis.mat43TransformVec4(self, other)
    def transpose(self): #returns mat43
        return noesis.mat43Transpose(self)
    def inverse(self): #returns mat43
        return noesis.mat43Inverse(self)
    def orthogonalize(self): #returns mat43
        return noesis.mat43Orthogonalize(self)
    def isSkewed(self): #returns 1 if skewed, otherwise 0
        return noesis.mat43IsSkewed(self)
    def rotate(self, degrees, rotAngles, transposeRot = 0): #returns mat43
        return noesis.mat43Rotate(self, degrees, rotAngles, transposeRot)
    def translate(self, trnVector): #returns mat43
        return noesis.mat43Translate(self, trnVector)
    def lerp(self, other, fraction): #returns mat43
        return noesis.mat43Lerp(self, other, fraction)
    def slerp(self, other, fraction): #returns mat43
        return noesis.mat43SLerp(self, other, fraction)
    def swapHandedness(self, axis = 0): #returns mat43
        return noesis.mat43SwapHandedness(self, axis)

    def toQuat(self):
        return noesis.mat43ToQuat(self)
    def toAngles(self):
        return noesis.mat43ToAngles(self)
    def toMat44(self):
        return noesis.mat43ToMat44(self)
    def toBytes(self): #returns bytearray
        return noesis.mat43ToBytes(self)
    def fromBytes(otherBytes, bigEnd = NOE_LITTLEENDIAN): #returns type built from binary
        return noesis.mat43FromBytes(otherBytes, bigEnd)
    def getStorage(self): #returns raw storage (list, tuple, etc)
        return self.mat43

class NoeMat44:
    def __init__(self, mat44 = identityMat44Tuple):
        self.mat44 = mat44
        # noesis.mat44Validate(self)
    def __getitem__(self, index):
        return self.mat44[index]
    def __setitem__(self, index, value):
        if isinstance(self.mat44, tuple):
            self.mat44 = noeTupleToList(self.mat44)
        self.mat44[index] = value
    def __repr__(self):
        return repr(self.mat44)
    def __len__(self):
        return len(self.mat44)
    def binaryCompare(self, other):
        return self.mat44[0] == other.mat44[0] and self.mat44[1] == other.mat44[1] and self.mat44[2] == other.mat44[2] and self.mat44[3] == other.mat44[3]
    def __eq__(self, other):
        return self.binaryCompare(other)
    def __ne__(self, other):
        return not self.binaryCompare(other)

    def __add__(self, other):
        return noesis.mat44Add(self, other)
    def __sub__(self, other):
        return noesis.mat44Sub(self, other)
    def __mul__(self, other):
        if isinstance(other, (NoeMat44, list, tuple)):
            return noesis.mat44Mul(self, other)
        elif isinstance(other, NoeVec4):
            return noesis.mat44TransformVec4(self, other)
        else:
            return NoeMat44([self.mat44[0]*other, self.mat44[1]*other, self.mat44[2]*other, self.mat44[3]*other])
    def __neg__(self):
        return NoeMat44([-self.mat44[0], -self.mat44[1], -self.mat44[2], -self.mat44[3]])

    def transformVec4(self, other): #returns vec4
        return noesis.mat44TransformVec4(self, other)
    def transpose(self): #returns mat44
        return noesis.mat44Transpose(self)
    def inverse(self): #returns mat44
        # return noesis.mat44Inverse(self)
        return self
    def rotate(self, degrees, rotAngles): #returns mat44
        return noesis.mat44Rotate(self, degrees, rotAngles)
    def translate(self, trnVector): #returns mat44
        return noesis.mat44Translate(self, trnVector)
    def swapHandedness(self, axis = 0): #returns mat44
        return noesis.mat44SwapHandedness(self, axis)

    def toMat43(self):
        # return noesis.mat44ToMat43(self)
        return NoeMat43()
    def toBytes(self): #returns bytearray
        return noesis.mat44ToBytes(self)
    def fromBytes(otherBytes, bigEnd = NOE_LITTLEENDIAN): #returns type built from binary
        return noesis.mat44FromBytes(otherBytes, bigEnd)
    def getStorage(self): #returns raw storage (list, tuple, etc)
        return self.mat44
