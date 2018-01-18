import inc_noesis
import noesis
from NoeMesh import NoeMesh

# TODO: remove this once rapi.rpgConstructModel is rewoked to use NoeVec3 classes
class NoeModel:
    def __init__(self, meshes = [], bones = [], anims = [], modelMats = None):
        self.setMeshes(meshes)
        self.setBones(bones)
        self.setAnims(anims)
        self.setModelMaterials(modelMats)
        self.setPrimGlobals(None, None)

    def setModelMaterials(self, modelMats):
        if modelMats is not None and not isinstance(modelMats, inc_noesis.NoeModelMaterials):
            noesis.doException("Invalid type provided for model materials")
        self.modelMats = modelMats

    #animations will be applied to the model based on matching bone names from their local bone lists
    def setAnims(self, anims):
        noesis.validateListTypes(anims, (inc_noesis.NoeAnim, inc_noesis.NoeKeyFramedAnim))
        self.anims = anims

    def setMeshes(self, meshes):
        noesis.validateListType(meshes, NoeMesh)
        self.meshes = meshes

    def setBones(self, bones):
        noesis.validateListType(bones, inc_noesis.NoeBone)
        self.bones = bones

    #note that globalVtx/Idx are ignored by Noesis (only mesh geometry is used), but are provided for convenience when exporting
    def setPrimGlobals(self, globalVtx, globalIdx):
        self.globalVtx = globalVtx #list of NoeGlobalVert
        self.globalIdx = globalIdx #triangle index (int) list referencing globalVtx
