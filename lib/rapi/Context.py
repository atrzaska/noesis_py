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


def installHook():
    # at first commit rather than import time: inc_noesis imports rapi before defining NoeMesh
    if getattr(inc_noesis.NoeMesh, "__getattr__", None) is not _noeMeshGetattr:
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
        self.transform = None  # (3x3 rotation/scale, translation) numpy arrays
        self.transformed = {}  # (buffer id, kind) -> transformed copy, for the current transform
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
        installHook()
        mesh = inc_noesis.NoeMesh([], [])
        for name in LAZY:
            mesh.__dict__.pop(name, None)
        mesh.__dict__[ARRAYS] = {
            "indices": faceBuffer,
            "positions": self.transformedBuffer(self.vertexBuffer, "points"),
            "normals": self.transformedBuffer(self.normalBuffer, "normals"),
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

    def setTransform(self, transform):
        import numpy as np
        self.transformed = {}
        if transform is None:
            self.transform = None
            return
        m = np.array([[float(transform[r][c]) for c in range(3)] for r in range(4)])
        self.transform = (m[:3], m[3])

    def transformedBuffer(self, buffer, kind):
        """A bound position/normal buffer with the current transform applied (row vectors,
        like NoeMat43.transformPoint / transformNormal)."""
        import numpy as np
        if self.transform is None or not hasattr(buffer, "shape") or not len(buffer):
            return buffer
        key = (id(buffer), kind)
        if key not in self.transformed:
            rotation, translation = self.transform
            v = buffer.astype(np.float64) @ rotation
            if kind == "points":
                v += translation
            else:
                length = np.linalg.norm(v, axis=1, keepdims=True)
                v = np.divide(v, length, out=np.zeros_like(v), where=length > 0)
            self.transformed[key] = (buffer, v.astype(buffer.dtype if buffer.dtype.kind == "f" else np.float32))
        return self.transformed[key][1]

    def clearBuffers(self):
        self.vertexBuffer = []
        self.normalBuffer = []
        self.uvBuffer = []
        self.uv2Buffer = []
        self.colorBuffer = [] # 0 # TODO: not used yet
        self.boneWeightBuffer = [] # TODO: not used yet
        self.boneIndexBuffer = []  # TODO: not used yet
