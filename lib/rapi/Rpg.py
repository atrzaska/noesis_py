import struct
import itertools
from RapiModel import RapiModel
from RapiContext import RapiContext
from FaceInfo import FaceInfo

class Rpg:
    def __init__(self):
        self.contexts = []
        self.lastCheckedName = None

    def rpgCreateContext(self):
        context = RapiContext()
        self.contexts.append(context)
        return context

    def rpgConstructModel(self):
        model = RapiModel()
        self.__currentContext().models.append(model)
        return model

    def rpgBindPositionBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.__splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped) # TODO: make format dynamic
        self.__currentContext().vertexBuffers.append(mapped)

    def rpgBindNormalBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.__splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped) # TODO: make format dynamic
        self.__currentContext().normalBuffers.append(mapped)

    def rpgBindUV1BufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.__splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 2], splitted)
        mapped = map(lambda x: struct.unpack('2f', x), mapped) # TODO: make format dynamic
        self.__currentContext().uvBuffers.append(mapped)

    def rpgSetMaterial(self, material):
        self.__currentContext().currentMaterial = material

    def rpgCommitTriangles(self, buff, typeSize, numIdx, shape, usePlotMap):
        fmt = "{numIdx}H".format(**locals()) # TODO: make format dynamic
        unpacked = struct.unpack(fmt, buff)

        faceBuffer = FaceInfo(unpacked, typeSize, numIdx, shape, usePlotMap, self.__currentContext().currentMaterial)
        self.__currentContext().faceBuffers.append(faceBuffer)

    def getLastCheckedName(self):
        return self.lastCheckedName

    def setLastCheckedName(self, name):
        self.lastCheckedName = name

    # private

    def __currentContext(self):
        return self.contexts[-1]

    def __splitBuffer(self, buff, structSize):
        return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]
