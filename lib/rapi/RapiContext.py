from RapiMeshPart import RapiMeshPart
from util import last

class RapiContext:
    def __init__(self):
        self.models = [] # TODO: not used yet
        self.vertexBuffers = []
        self.normalBuffers = []
        self.uvBuffers = []
        self.faceBuffers = []
        self.colorBuffers = [] # 0 # TODO: not used yet
        self.boneWeightBuffers = [] # TODO: not used yet
        self.boneIndexBuffers = []  # TODO: not used yet
        self.materials = []
        self.names = [] # TODO: not used yet
        self.lightMaps = [] # 0  # TODO: not used yet
        self.boneMaps = [] # TODO: not used yet
        self.uvScaleBiases = [] # TODO: not used yet

        self.meshParts = []

    def commit(self):
        meshPart = RapiMeshPart()
        meshPart.vertexBuffer = self.currentVertexBuffer()
        meshPart.normalBuffer = self.currentNormalBuffer()
        meshPart.uvBuffer = self.currentUvBuffer()
        meshPart.faceBuffer = self.currentFaceBuffer()
        meshPart.colorBuffer = self.currentColorBuffer()
        meshPart.boneWeightBuffer = self.currentBoneWeightBuffer()
        meshPart.boneIndexBuffer = self.currentBoneIndexBuffer()
        meshPart.material = self.currentMaterial()
        meshPart.name = self.currentName()
        meshPart.lightMap = self.currentLightMap()
        meshPart.boneMap = self.currentBoneMap()
        meshPart.uvScaleBiase = self.currentUvScaleBias()

        self.meshParts.append(meshPart)

    def currentModel(self):
        return last(self.models)

    def currentNormalBuffer(self):
        return last(self.normalBuffers)

    def currentVertexBuffer(self):
        return last(self.vertexBuffers)

    def currentUvBuffer(self):
        return last(self.uvBuffers)

    def currentFaceBuffer(self):
        return last(self.faceBuffers)

    def currentColorBuffer(self):
        return last(self.colorBuffers)

    def currentBoneWeightBuffer(self):
        return last(self.boneWeightBuffers)

    def currentBoneIndexBuffer(self):
        return last(self.boneIndexBuffers)

    def currentMaterial(self):
        return last(self.materials)

    def currentName(self):
        return last(self.names)

    def currentLightMap(self):
        return last(self.lightMaps)

    def currentBoneMap(self):
        return last(self.boneMaps)

    def currentUvScaleBias(self):
        return last(self.uvScaleBiases)
