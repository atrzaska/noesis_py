import struct
import itertools
from RapiModel import RapiModel
from RapiContext import RapiContext
from pymmd import NoesisViewer
from FaceInfo import FaceInfo

class Rpg:
    def __init__(self):
        self.contexts = []
        self.models = []
        self.vertexBuffers = []
        self.normalBuffers = []
        self.uvBuffers = []
        self.faceBuffers = []
        self.materials = []

    def currentContext(self):
        return self.contexts.last[-1]

    def rpgCreateContext(self):
        context = RapiContext()
        self.contexts.append(context)
        return context

    def rpgConstructModel(self):
        model = RapiModel()
        self.models.append(model)
        return model

    def rpgBindPositionBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped) # TODO: make format dynamic
        self.vertexBuffers.append(mapped)

    def rpgBindNormalBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped) # TODO: make format dynamic
        self.normalBuffers.append(mapped)

    def rpgBindUV1BufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 2], splitted)
        mapped = map(lambda x: struct.unpack('2f', x), mapped) # TODO: make format dynamic
        self.uvBuffers.append(mapped)

    def rpgSetMaterial(self, material):
        print('set material')
        self.materials.append(material)

    def currentMaterial(self):
        material = self.materials[-1]
        print(self.currentModel())
        if self.currentModel() == None:
            return None
        materials = self.currentModel().materials.materials
        currentMaterial = next(x for x in materials if x.name == material)
        return currentMaterial

    def currentTexture(self):
        if self.currentMaterial() == None:
            return None
        return self.currentMaterial().texture

    def currentModel(self):
        if len(self.models) == 0:
            return None
        return self.models[-1]

    def rpgCommitTriangles(self, buff, typeSize, numIdx, shape, unk1):
        print('commit triangles')
        fmt = "{numIdx}H".format(**locals()) # TODO: make format dynamic
        unpacked = struct.unpack(fmt, buff)

        texture = self.currentTexture()
        faceBuffer = FaceInfo(unpacked, typeSize, numIdx, shape, unk1, texture)
        self.faceBuffers.append(faceBuffer)

    def splitBuffer(self, buff, structSize):
        return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]

    def rpgLog(self):
        NoesisViewer(self).call()
