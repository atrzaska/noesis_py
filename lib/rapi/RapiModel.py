from util import last

class RapiModel:
    def __init__(self):
        self.materials = []
        self.bones = []
        self.animations = []

    def setModelMaterials(self, materials):
        self.materials = materials

    def setBones(self, bones):
        self.bones = bones

    def setAnims(self, animations):
        self.animations = animations

    def currentMaterial(self):
        return last(self.materials)

    def currentBone(self):
        return last(self.bones)

    def currentAnimation(self):
        return last(self.animation)
