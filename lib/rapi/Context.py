import inc_noesis

class Context:
    def __init__(self):
        self.meshes = []
        self.material = None
        self.name = None # TODO: not used yet
        self.lightMap = None # 0  # TODO: not used yet
        self.boneMap = [] # TODO: not used yet
        self.uvScaleBias = None # TODO: not used yet
        self.clearBuffers()

    # def commit(self, faceBuffer, type, numIdx, shape, usePlotMap):
        # mesh = inc_noesis.NoeMesh(faceBuffer, self.vertexBuffer)
        # mesh.setName(self.name)
        # mesh.setMaterial(self.material)
        # mesh.setLightmap(self.lightMap)
        # mesh.setNormals(self.normalBuffer)
        # mesh.setUVs(self.uvBuffer)
        # mesh.setUVs(self.uv2Buffer, 1)
        # mesh.setColors(self.colorBuffer)
        # mesh.setWeights(self.boneWeightBuffer)
        # mesh.setBoneMap(self.boneMap)
        # mesh.boneIndexBuffer = self.boneIndexBuffer
        # mesh.uvScaleBias = self.uvScaleBias
        # mesh.type = type
        # mesh.numIdx = numIdx
        # mesh.shape = shape
        # mesh.usePlotMap = usePlotMap
        # self.meshes.append(mesh)

        # unpackedColorBuffer = map(lambda x: inc_noesis.NoeVec4(x), unpackedBuffer)
        # unpackedNormalBuffer = map(lambda x: inc_noesis.NoeVec3(x), unpackedBuffer)
        # unpackedPositionBuffer = map(lambda x: inc_noesis.NoeVec3(x), unpackedBuffer)
        # unpackedUVBuffer = map(lambda x: inc_noesis.NoeVec3((x[0], x[1], 0)), unpackedBuffer)

    def commit(self, faceBuffer, type, numIdx, shape, usePlotMap):
        mesh = inc_noesis.NoeMesh([], [])
        mesh.indices = faceBuffer
        mesh.positions = self.vertexBuffer
        mesh.normals = self.normalBuffer
        mesh.uvs = self.uvBuffer
        mesh.lmUVs = self.uv2Buffer
        mesh.weights = self.boneWeightBuffer
        mesh.setColors(self.colorBuffer)
        mesh.setName(self.name)
        mesh.setMaterial(self.material)
        mesh.setLightmap(self.lightMap)
        mesh.setBoneMap(self.boneMap)
        mesh.boneIndexBuffer = self.boneIndexBuffer
        mesh.uvScaleBias = self.uvScaleBias
        mesh.type = type
        mesh.numIdx = numIdx
        mesh.shape = shape
        mesh.usePlotMap = usePlotMap
        self.meshes.append(mesh)

    def clearBuffers(self):
        self.vertexBuffer = []
        self.normalBuffer = []
        self.uvBuffer = []
        self.uv2Buffer = []
        self.colorBuffer = [] # 0 # TODO: not used yet
        self.boneWeightBuffer = [] # TODO: not used yet
        self.boneIndexBuffer = []  # TODO: not used yet
