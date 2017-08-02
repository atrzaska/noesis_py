import struct
import itertools
from RapiModel import RapiModel
from RapiContext import RapiContext
from pymmd import NoesisViewer

class Rpg:
    def __init__(self):
        self.vertexBuffers = []
        self.normalBuffers = []
        self.uvBuffers = []
        self.materials = []
        self.faceBuffers = []

    def rpgCreateContext(self):
        return RapiContext()

    def rpgConstructModel(self):
        return RapiModel()

    def rpgBindPositionBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped)
        self.vertexBuffers.append(mapped)

    def rpgBindNormalBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped)
        self.normalBuffers.append(mapped)

    def rpgBindUV1BufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 2], splitted)
        mapped = map(lambda x: struct.unpack('2f', x), mapped)
        self.uvBuffers.append(mapped)

    def rpgSetMaterial(self, matName):
        self.materials.append(matName)

    def rpgCommitTriangles(self, buff, typeSize, numIdx, shape, unk1):
        fmt = "{numIdx}H".format(**locals()) # TODO: make format dynamic
        unpacked = struct.unpack(fmt, buff)

        self.faceBuffers.append({
            'buff': unpacked,
            'typeSize': typeSize,
            'numIdx': numIdx,
            'shape': shape,
            'unk1': unk1
        })

    def splitBuffer(self, buff, structSize):
        return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]

    def rpgLog(self):
        NoesisViewer.run(self)
