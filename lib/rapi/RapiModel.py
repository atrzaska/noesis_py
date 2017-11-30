from util import last

class RapiModel:
    def setModelMaterials(self, materials):
        self.materials = materials

    def setBones(self, bones):
        self.bones = bones

    def setAnims(self, animations):
        self.animations = animations

    def currentMaterial(self):
        return last(self.materials)
