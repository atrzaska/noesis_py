import struct
from RapiModel import RapiModel
from RapiContext import RapiContext

class Rpg:
    def __init__(self):
        self.comittedTriangles = []

    def rpgCreateContext(self):
        return RapiContext()

    def rpgConstructModel(self):
        return RapiModel()

    def rpgBindPositionBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped)
        self.vertices = mapped

    def rpgBindNormalBufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 3], splitted)
        mapped = map(lambda x: struct.unpack('3f', x), mapped)
        self.normals = mapped

    def rpgBindUV1BufferOfs(self, buff, typeSize, structSize, structOffset):
        splitted = self.splitBuffer(buff, structSize)
        mapped = map(lambda x: x[structOffset:structOffset + typeSize * 2], splitted)
        mapped = map(lambda x: struct.unpack('2f', x), mapped)
        self.uvs = mapped

    def rpgSetMaterial(self, matName):
        self.material = matName

    def rpgCommitTriangles(self, buff, type, numIdx, shape, unk1):
        self.comittedTriangles.append({
            'buff': buff,
            'type': type,
            'numIdx': numIdx,
            'shape': shape,
            'unk1': unk1
        })

    def splitBuffer(self, buff, structSize):
        return [buff[i:i + structSize] for i in range(0, len(buff), structSize)]

    # TODO: remove non official api
    def rpgLog(self):
        print("<vertices: {self.vertices}, normals: {self.normals}, uvs: {self.uvs}, comittedTriangles: {self.comittedTriangles}>".format(**locals()))
