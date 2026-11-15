import inc_noesis

# NoeMesh attributes filled from the bound buffers. Context.commit keeps the buffers (numpy
# arrays from rapi.unpackBuffer) in ARRAYS and NoeMesh.__getattr__ turns one into the usual
# list of tuples (a tuple for indices) the first time it is read; the viewer reads the arrays
# directly. inc_noesis.py itself is not changed: the hook is installed on the class from here.
ARRAYS = "_rapiArrays"
LAZY = ("indices", "positions", "normals", "uvs", "lmUVs", "weights", "colors", "boneIndexBuffer")


def toPython(name, value):
    if not hasattr(value, "tolist"):
        return value
    if name == "indices":
        return tuple(value.tolist())
    return [tuple(row) for row in value.tolist()]


def _noeMeshGetattr(self, name):
    arrays = self.__dict__.get(ARRAYS)
    if arrays is None or name not in arrays:
        raise AttributeError("'NoeMesh' object has no attribute '%s'" % name)
    value = toPython(name, arrays[name])
    self.__dict__[name] = value
    return value


inc_noesis.NoeMesh.__getattr__ = _noeMeshGetattr


def meshArray(mesh, name):
    """A mesh attribute as a numpy array (None when empty), without building Python lists for
    values that are still lazy."""
    import numpy as np
    value = mesh.__dict__[name] if name in mesh.__dict__ else mesh.__dict__.get(ARRAYS, {}).get(name)
    if value is None or not len(value):
        return None
    return np.asarray(value)

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
        for name in LAZY:
            mesh.__dict__.pop(name, None)
        mesh.__dict__[ARRAYS] = {
            "indices": faceBuffer,
            "positions": self.vertexBuffer,
            "normals": self.normalBuffer,
            "uvs": self.uvBuffer,
            "lmUVs": self.uv2Buffer,
            "weights": self.boneWeightBuffer,
            "colors": self.colorBuffer,  # raw values, like positions/normals (setColors wants NoeVec4)
            "boneIndexBuffer": self.boneIndexBuffer,
        }
        mesh.setName(self.name)
        mesh.setMaterial(self.material)
        mesh.setLightmap(self.lightMap)
        mesh.setBoneMap(self.boneMap)
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
