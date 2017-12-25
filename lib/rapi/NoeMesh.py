class NoeMesh:
    def __init__(self, triList, posList, name = "default", materialName = "default", glbVertIdx = -1, glbTriIdx = -1):
        self.setIndices(triList)
        self.setPositions(posList)
        self.setName(name)
        self.setMaterial(materialName)
        #glb's are indices into the parent model's globalVtx/globalIdx lists on export
        self.setPrimGlobals(glbVertIdx, glbTriIdx)
        self.setLightmap("")
        self.setTransformedVerts(None, None)
        #fill in placeholders
        self.setNormals([])
        self.setUVs([])
        self.setUVs([], 1)
        self.setTangents([])
        self.setTangents([], 1)
        self.setColors([])
        self.setWeights([])
        self.setMorphList([])
        self.setBoneMap([])
        self.setUserStreams([])
        self.texRefIndex = -1 #this is set by Noesis internally when you load a model's textures manually

    def __repr__(self):
        return "(NoeMesh:" + self.name + "," + self.matName + "," + repr(len(self.indices)) + "," + repr(len(self.positions)) + ")"

    def setName(self, name):
        self.name = name

    def setMaterial(self, materialName):
        self.matName = materialName

    #triangle lists are single-dimension lists of ints, expected to be divisible by 3
    def setIndices(self, triList):
        self.indices = triList

    def setPositions(self, posList):
        self.positions = posList

    def setNormals(self, nrmList):
        self.normals = nrmList

    #uv z component should typically be 0
    def setUVs(self, uvList, slot = 0):
        if slot == 0:
            self.uvs = uvList
        elif slot == 1:
            self.lmUVs = uvList
        else:
            noesis.doException("Unsupported uv slot")

    #translation component of NoeMat43 is ignored for tangents (matrix[0]=normal, matrix[1]=tangent, matrix[2]=bitangent)
    def setTangents(self, tanList, slot = 0):
        if slot == 0:
            self.tangents = tanList
        elif slot == 1:
            self.lmTangents = tanList
        else:
            noesis.doException("Unsupported tangent slot")

    #color lists are rgba values stored in vec4's
    def setColors(self, clrList):
        self.colors = clrList

    def setWeights(self, weightList):
        self.weights = weightList

    def setMorphList(self, morphList):
        self.morphList = morphList

    def setBoneMap(self, boneMap):
        self.boneMap = boneMap

    def setUserStreams(self, userStreamList):
        self.userStreams = userStreamList

    #indices into the parent model's globalVtx/globalIdx lists on export
    def setPrimGlobals(self, glbVertIdx, glbTriIdx):
        self.glbVertIdx = glbVertIdx
        self.glbTriIdx = glbTriIdx

    def setLightmap(self, lmMatName):
        self.lmMatName = lmMatName

    #not currently used, planned in a future update
    def setTransformedVerts(self, positions, normals):
        self.transVerts = positions
        self.transNormals = normals

    #convenience function for checking if vertex components have valid content
    def componentEmpty(component):
        if component is None or len(component) <= 0:
            return 1
        return 0
