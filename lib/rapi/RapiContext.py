from util import last

class RapiContext:
    def __init__(self):
        self.models = []
        self.vertexBuffers = []
        self.normalBuffers = []
        self.uvBuffers = []
        self.faceBuffers = []
        self.colorBuffers = []
        self.boneWeightBuffers = []
        self.boneIndexBuffers = []
        self.materials = []
        self.names = []
        self.lightMaps = []
        self.boneMaps = []
        self.uvScaleBiases = []

    def currentModel(self):
        return last(self.models)

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
