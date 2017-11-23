#Project Diva F 2nd
#noesis Script by chrrox
#made possible by MR. Adults
#Decryption Made possible by Anon

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Project Diva F 2nd Model", ".osd")
    noesis.setHandlerTypeCheck(handle, osdCheckType)
    noesis.setHandlerLoadModel(handle, osdLoadModel)

    handle = noesis.register("Project Diva F 2nd Texture", ".txd")
    noesis.setHandlerTypeCheck(handle, txdCheckType)
    noesis.setHandlerLoadRGBA(handle, txdLoadRGBA)
    #noesis.logPopup()

    return 1


def osdCheckType(data):
    td = NoeBitStream(data)
    return 1

def txdCheckType(data):
    td = NoeBitStream(data)
    return 1

class osdModel:

    def __init__(self, bs):
        rapi.rpgSetOption(noesis.RPGOPT_BIGENDIAN, 1)
        self.texList  = []
        self.matList  = []
        self.matDict  = {}
        self.boneList = []
        self.boneMap  = []
        self.boneDict  = {}
        self.offsetList = []
        self.meshOffsets = []
        self.loadAll(bs)

    def loadAll(self, bs):
        baseName = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))
        if( rapi.checkFileExists( rapi.getDirForFilePath( rapi.getLastCheckedName() ) + baseName + ".txd" ) ):
            texData = rapi.loadIntoByteArray( rapi.getDirForFilePath( rapi.getLastCheckedName() ) + baseName + ".txd" )
            txdLoadRGBA(texData, self.texList)
        while not bs.checkEOF():
            self.load_CHNK(bs)

    def load_CHNK(self, bs):
        chunkStart = bs.tell(); dataStart = chunkStart + 32
        magic, bigSize, headerSize, unk, \
        version, chunkSize, null00, null01 = bs.read("8I")
        if str(magic) in chunkLoaderDict:
            chunkLoaderDict[str(magic)](self, bs, [chunkStart, chunkSize, bigSize])
        else:
            print("Unkown format found " +  str(magic))
        bs.seek(dataStart + chunkSize, NOESEEK_ABS)

    def load_POF0(self, bs, info):
        #print("POFO")
        pass

    def load_EOFC(self, bs, info):
        #print("EOFC")
        pass

    def load_MOSD(self, bs, info):
        #print("MOSD")
        mosdHeader = bs.read(">" + "9i")
        #print(mosdHeader)
        bs.seek(info[0] + mosdHeader[5], NOESEEK_ABS)
        nameOffset = bs.read(">" + mosdHeader[1] * "i")
        #print(nameOffset)
        for a in range(0, mosdHeader[1]):
            bs.seek(info[0] + nameOffset[a], NOESEEK_ABS)
            mosdString = bs.readString()
            #print(mosdString)
        for a in range(0, mosdHeader[8]):
            bs.seek(info[0] + mosdHeader[7] + (4 * a), NOESEEK_ABS)
            texHash = bs.read(">" + "I")
            self.matDict[str(texHash[0])] = len(self.matDict)
        #print(self.matDict)

    def load_OMDL(self, bs, info):
        #print("OMDL")
        omdlHeader = bs.read(">" + "3i3f4i")
        #print(omdlHeader)
        self.matCount = omdlHeader[8]
        for a in range(0, omdlHeader[8]):
            bs.seek(info[0] + omdlHeader[9] + (a * 0x4B0) + 0x430, NOESEEK_ABS)
            material = NoeMaterial(bs.readBytes(0x40).decode("ASCII").rstrip("\0"), "")
            bs.seek(info[0] + omdlHeader[9] + (a * 0x4B0), NOESEEK_ABS)
            usedTex, matType2 = bs.read(">" + "2I")
            typeName = bs.readBytes(8).decode("ASCII").rstrip("\0")
            #print([usedTex, matType2, typeName])
            for b in range(0, 8):
                matInfo = bs.read(">" + "4H4I24f")
                #print(str(b))
                if str(matInfo[4]) in self.matDict:
                    texIndex = self.matDict[str(matInfo[4])]
                    #print(self.texList[texIndex].name)
                    if b == 0:
                        material.setTexture(self.texList[texIndex].name)
                    elif b == 1:
                        secondPassMat = NoeMaterial(material.name + "_ambient", self.texList[texIndex].name)
                        secondPassMat.setFlags(noesis.NMATFLAG_TWOSIDED, 1)
                        secondPassMat.setBlendMode("GL_ZERO", "GL_SRC_COLOR")
                        secondPassMat.setDiffuseColor( (0.8, 0.8, 0.8, 1.0) )
                        #material.setNextPass(secondPassMat)
                    elif b == 3:
                        material.setSpecularTexture(self.texList[texIndex].name)
                    elif b == 4:
                        pass
                        #toon curve
                    elif b == 5:
                        pass
                        #material.setEnvTexture(self.texList[texIndex].name)
                    else:
                        print([str(b), self.texList[texIndex].name])
            self.matList.append(material)

        self.MeshInfo = []
        for a in range(0, omdlHeader[6]):
            bs.seek(info[0] + omdlHeader[7] + (a * 0xD8), NOESEEK_ABS)
            polyInfo = bs.read(">" + "5f33i")
            polyName = bs.readBytes(0x40).decode("ASCII").rstrip("\0")
            #print(polyName)
            faceInfo = []
            boneMap = []
            for b in range(0, polyInfo[5]):
                tmp = []
                bs.seek(info[0] + polyInfo[6] + (b * 0x70), NOESEEK_ABS)
                faceInfo.append(bs.read(">" + "5f16i5f2i"))
                bs.seek(info[0] + faceInfo[b][9], NOESEEK_ABS)
                for c in range(0, faceInfo[b][8]):
                    b1 = bs.read(">H")
                    tmp.append(b1[0]); tmp.append(b1[0]); tmp.append(b1[0])
                boneMap.append(tmp)
            self.MeshInfo.append([polyName, polyInfo, faceInfo, boneMap])

        bs.seek(info[0] + omdlHeader[9], NOESEEK_ABS)
        for a in range(0, omdlHeader[8]):
            bs.seek(0x430, NOESEEK_REL)
            meshName = bs.readBytes(0x40).decode("ASCII").rstrip("\0")
            #print(meshName)
            bs.seek(0x40, NOESEEK_REL)

    def load_OSKN(self, bs, info):
        #print("OSKN")
        osknHeader = bs.read(">" + "6i")
        #print(osknHeader)

        boneIdList = []
        #print("======Bone ID======")
        bs.seek(info[0] + osknHeader[0], NOESEEK_ABS)
        for a in range(0, osknHeader[4]):
            boneIdList.append(bs.read("2H"))
            if self.boneDict.__contains__(str(boneIdList[a][1])):
                pass
            else:
                self.boneDict[str(boneIdList[a][1])] = len(self.boneDict)
        #print(self.boneDict)

        bonePList = []
        #print("======Bone Parent======")
        bs.seek(info[0] + osknHeader[5], NOESEEK_ABS)
        for a in range(0, osknHeader[4]):
            bonePList.append(bs.read("2H"))
            #print(bonePList[a])

        boneNList = []
        #print("======Bone Name======")
        for a in range(0, osknHeader[4]):
            bs.seek(info[0] + osknHeader[2] + (4 * a), NOESEEK_ABS)
            boneNameOff = bs.read(">I")
            bs.seek(info[0] + boneNameOff[0], NOESEEK_ABS)
            boneNList.append(bs.readString())
            #print(boneNList[a])

        #print("======Bone Matrix======")
        for a in range(0, osknHeader[4]):
            bs.seek(info[0] + osknHeader[1] + (0x40 * a), NOESEEK_ABS)
            m01, m02, m03, m04 = bs.read(">4f")
            m11, m12, m13, m14 = bs.read(">4f")
            m21, m22, m23, m24 = bs.read(">4f")
            m31, m32, m33, m34 = bs.read(">4f")
            if str(bonePList[a][1]) in self.boneDict:
                parent = self.boneDict[str(bonePList[a][1])]
            else:
                parent = -1
                if boneNList[a] == "n_hara_b_wj_ex":
                    if "41728" in self.boneDict:
                        parent = self.boneDict["41728"]
                elif boneNList[a] == "n_hara_c_wj_ex":
                    if "46848" in self.boneDict:
                        parent = self.boneDict["46848"]
                elif boneNList[a] == "kl_mune_b_wj":
                    if "47104" in self.boneDict:
                        parent = self.boneDict["47104"]
                elif boneNList[a] == "j_kao_wj":
                    if "23040" in self.boneDict:
                        parent = self.boneDict["23040"]
                elif boneNList[a] == "kl_te_l_wj":
                    if "30720" in self.boneDict:
                        parent = self.boneDict["30720"]
                elif boneNList[a] == "kl_te_r_wj":
                    if "39680" in self.boneDict:
                        parent = self.boneDict["39680"]

            boneMtx = NoeMat43( [NoeVec3((m01, m02, m03)), NoeVec3((m11, m12, m13)), NoeVec3((m21, m22, m23)), NoeVec3((m04, m14, m24))] ).inverse()
            newBone = NoeBone(self.boneDict[str(boneIdList[a][1])], boneNList[a], boneMtx, None, parent)
            self.boneList.append(newBone)

        if osknHeader[3] != 0:
            #print("============")
            bs.seek(info[0] + osknHeader[3], NOESEEK_ABS)
            osknHeader2 = bs.read(">" + "9i")
            #print(osknHeader2)

            #print("============")
            for a in range(0, osknHeader2[0]):
                bs.seek(info[0] + osknHeader2[3] + (0xC * a), NOESEEK_ABS)
                #print(bs.read(">" + "4b2I"))

            #print("============")
            for a in range(0, osknHeader2[2]):
                bs.seek(info[0] + osknHeader2[8], NOESEEK_ABS)

            #print("============")
            for a in range(0, osknHeader2[1]):
                bs.seek(info[0] + osknHeader2[4] + (0x4 * a), NOESEEK_ABS)
                boneNameOff = bs.read(">I")
                bs.seek(info[0] + boneNameOff[0], NOESEEK_ABS)
                #print(bs.readString())

            #print("============")
            bs.seek(info[0] + osknHeader2[7], NOESEEK_ABS)
            name1off = bs.read(">" + osknHeader2[6] * "I")
            for a in range(0, osknHeader2[6]):
                bs.seek(info[0] + name1off[a], NOESEEK_ABS)
                #print(bs.readString())

            #print("============")
            for a in range(0, 1):
                bs.seek(info[0] + osknHeader2[5] + (8 * a), NOESEEK_ABS)
                boneNameOff = bs.read(">II")
                bs.seek(info[0] + boneNameOff[0], NOESEEK_ABS)
                bone1 = bs.readString()
                bs.seek(info[0] + boneNameOff[1], NOESEEK_ABS)
                boneNameOff2 = bs.read(">I")
                bs.seek(info[0] + boneNameOff2[0], NOESEEK_ABS)
                #print([bone1, bs.readString()])

    def load_OIDX(self, bs, info):
        #print("OIDX")
        self.faceStart = bs.tell()

    def load_OVTX(self, bs, info):
        #print("OVTX")
        self.vertStart = bs.tell()
        matBase = len(self.matList) - self.matCount
        for a in range(0, len(self.MeshInfo)):
            #rapi.rpgSetName(str(a))
            #print(self.MeshInfo[a][0])
            #print(self.MeshInfo[a][1])
            bs.seek(self.vertStart + self.MeshInfo[a][1][23], NOESEEK_ABS)
            #print([bs.tell(), self.MeshInfo[a][1][8], self.MeshInfo[a][1][9]])
            vertBuff = bs.readBytes(self.MeshInfo[a][1][8] * self.MeshInfo[a][1][9])

            rapi.rpgBindPositionBufferOfs(vertBuff, noesis.RPGEODATA_FLOAT, self.MeshInfo[a][1][8], 0)
            rapi.rpgBindNormalBufferOfs(vertBuff, noesis.RPGEODATA_SHORT, self.MeshInfo[a][1][8], 12)
            rapi.rpgBindUV1BufferOfs(vertBuff, noesis.RPGEODATA_HALFFLOAT, self.MeshInfo[a][1][8], 28)
            rapi.rpgBindUV2BufferOfs(vertBuff, noesis.RPGEODATA_HALFFLOAT, self.MeshInfo[a][1][8], 32)
            rapi.rpgBindColorBufferOfs(vertBuff, noesis.RPGEODATA_HALFFLOAT, self.MeshInfo[a][1][8], 36, 4)
            if self.MeshInfo[a][1][8] == 56:
                rapi.rpgBindBoneWeightBufferOfs(vertBuff, noesis.RPGEODATA_USHORT, self.MeshInfo[a][1][8], 44, 4)
                rapi.rpgBindBoneIndexBufferOfs(vertBuff, noesis.RPGEODATA_UBYTE, self.MeshInfo[a][1][8], 52, 4)

            for b in range(0, len(self.MeshInfo[a][2])):
                #print(self.MeshInfo[a][2][b])
                rapi.rpgSetMaterial(self.matList[self.MeshInfo[a][2][b][5] + matBase].name)
                #print(self.MeshInfo[a][3][b])
                if len(self.MeshInfo[a][3][b]) != 0:
                    rapi.rpgSetBoneMap(self.MeshInfo[a][3][b])
                bs.seek(self.faceStart + self.MeshInfo[a][2][b][14], NOESEEK_ABS)
                faceBuff = bs.readBytes(self.MeshInfo[a][2][b][13] * 2)
                rapi.rpgCommitTriangles(faceBuff, noesis.RPGEODATA_USHORT, self.MeshInfo[a][2][b][13], noesis.RPGEO_TRIANGLE, 1)
            rapi.rpgClearBufferBinds()

class txdTexture:
    def __init__(self, bs):
        self.matList  = []
        self.texNames = []
        self.boneList = []
        self.bs = bs

    def loadAll(self, texList):
        bs = self.bs
        self.texList = texList
        baseName = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))
        if( rapi.checkFileExists( rapi.getDirForFilePath( rapi.getLastCheckedName() ) + baseName + ".txi" ) ):
            txiData = rapi.loadIntoByteArray( rapi.getDirForFilePath( rapi.getLastCheckedName() ) + baseName + ".txi" )
            self.load_MTXI(txiData)
        while not bs.checkEOF():
            self.load_CHNK(bs)

    def load_MTXI(self, txiData):
        #print("MTXI")
        bs = NoeBitStream(txiData)
        chnkHeader = bs.read("8I")
        mtxiHeader = bs.read(">" + "4I")
        #print(mtxiHeader)
        for a in range(0, mtxiHeader[0]):
            bs.seek( (mtxiHeader[1] + (8 * a)), NOESEEK_ABS)
            texHash, nameOff = bs.read(">" + "2I")
            bs.seek(nameOff, NOESEEK_ABS)
            texName = bs.readString()
            self.texNames.append(texName)



    def load_CHNK(self, bs):
        chunkStart = bs.tell(); dataStart = chunkStart + 32
        magic, bigSize, headerSize, unk, \
        version, chunkSize, null00, null01 = bs.read("8I")
        if str(magic) in texLoaderDict:
            texLoaderDict[str(magic)](self, bs, [chunkStart, chunkSize, bigSize])
        else:
            print("Unkown format found " +  str(magic))
        bs.seek(dataStart + chunkSize, NOESEEK_ABS)

    def load_MTXD(self, bs, info):
        #print("MTXD")
        mtxdHeader = bs.read("2i4B")
        #print(mtxdHeader)
        texOffList = bs.read(mtxdHeader[1] * "I")
        #print(texOffList)
        #print([len(self.texNames), mtxdHeader[1]])
        for a in range(0, mtxdHeader[1]):
            bs.seek((info[0] + 32) + texOffList[a], NOESEEK_ABS)
            txpbase = bs.tell()
            #print(txpbase)
            txpHeader = bs.read("2i4B")
            mipOffList = bs.read(txpHeader[1] * "I")
            for b in range(0, txpHeader[1]):
                bs.seek(txpbase + mipOffList[b], NOESEEK_ABS)
                texHeader = bs.read("6I")
                texData = bs.readBytes(texHeader[5])
                texFmt = 0
                if len(self.texNames) == mtxdHeader[1]:
                    texName = self.texNames[a]
                else:
                    texName = (str(a) + "_" + str(b))
                #RAW
                if texHeader[3] == 1:
                    texFmt = noesis.NOESISTEX_RGB24
                #RGBA
                if texHeader[3] == 2:
                    texFmt = noesis.NOESISTEX_RGBA32
                #DXT1
                if texHeader[3] == 6:
                    texFmt = noesis.NOESISTEX_DXT1
                #DXT3
                if texHeader[3] == 7:
                    texFmt = noesis.NOESISTEX_DXT3
                #DXT5
                if texHeader[3] == 9:
                    texFmt = noesis.NOESISTEX_DXT5
                #ATI2N
                if texHeader[3] == 11:
                    texData = rapi.imageDecodeDXT(texData, texHeader[1], texHeader[2], noesis.FOURCC_ATI2)
                    texFmt = noesis.NOESISTEX_RGBA32
                if b == 0:
                    tex1 = NoeTexture(texName, texHeader[1], texHeader[2], texData, texFmt)
                    self.texList.append(tex1)

    def load_ENRS(self, bs, info):
        #print("ENRS")
        pass

    def load_EOFC(self, bs, info):
        #print("EOFC")
        pass


chunkLoaderDict = {
    "809914192"        : osdModel.load_POF0,
    "1128681285"        : osdModel.load_EOFC,
    "1146310477"        : osdModel.load_MOSD,
    "1279544655"        : osdModel.load_OMDL,
    "1313559375"        : osdModel.load_OSKN,
    "1480870223"        : osdModel.load_OIDX,
    "1481922127"        : osdModel.load_OVTX
}

texLoaderDict = {
    "1146639437"        : txdTexture.load_MTXD,
    "1397902917"        : txdTexture.load_ENRS,
    "1128681285"        : txdTexture.load_EOFC,
}



def osdLoadModel(data, mdlList):
    ctx = rapi.rpgCreateContext()
    osd = osdModel(NoeBitStream(data))
    try:
        mdl = rapi.rpgConstructModel()
    except:
        mdl = NoeModel()
    mdl.setModelMaterials(NoeModelMaterials(osd.texList, osd.matList))
    mdlList.append(mdl); mdl.setBones(osd.boneList)
    return 1


def txdLoadRGBA(data, texList):
    txd = txdTexture(NoeBitStream(data))
    txd.loadAll(texList)
    return 1
