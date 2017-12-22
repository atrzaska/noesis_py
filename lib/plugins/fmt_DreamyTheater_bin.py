#By Minmode
#Based on max script by Chrrox

from inc_noesis import *
import noesis
import rapi

def registerNoesisTypes():
    # pass # TODO remove this
    handle = noesis.register('Project Diva Dreamy Theater Model', '.bin')
    noesis.setHandlerTypeCheck(handle, objBinCheckType)
    noesis.setHandlerLoadModel(handle, objBinLoadModel)

    handle = noesis.register('Project Diva Dreamy Theater Texture', '.bin')
    noesis.setHandlerTypeCheck(handle, texBinCheckType)
    noesis.setHandlerLoadRGBA(handle, texBinLoadRGBA)
    return 1

def objBinCheckType(data):
    bs = NoeBitStream(data)
    header = bs.readInt()
    if len(data) < 4:
        return 0
    if header != 0x05062500:
        return 0
    return 1

def objBinLoadModel(data, mdlList):
    loader = DreamyTheaterLoader(data, mdlList)
    loader.load()
    return 1

class DreamyTheaterLoader:
    def __init__(self, data, mdlList):
        self.data = data
        self.bs = NoeBitStream(self.data)
        self.mdlList = mdlList
        self.texList = []
        self.matList = []
        self.boneList = []
        self.animList = []
        self.baseName = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))[:-4]
        self.textureIdToName = {}
        self.textureIds = []
        self.bAnimInfoName = []
        self.boneData_Array = []
        self.kfBones = []
        self.bAnimInfoRot = []

    def load(self):
        ctx = rapi.rpgCreateContext()

        self.load_binTexDB()
        self.load_binBone()
        self.load_BinModel()
        self.load_binTex()

        mdl = rapi.rpgConstructModel()
        self.mdlList.append(mdl)
        mdl.setBones(self.boneList)
        if self.texList != []:
            mdl.setModelMaterials(NoeModelMaterials(self.texList, self.matList))
        if self.animList != []:
            mdl.setAnims(self.animList)
            rapi.setPreviewOption('setAnimSpeed', '60')

        rapi.rpgClearBufferBinds()
        return 1

    def load_BinModel(self):
        bs = self.bs
        idString = bs.readInt()
        sectionCount = bs.readInt()
        boneCount = bs.readInt()
        sectionTableOff = bs.readInt()
        boneTableOff1 = bs.readInt()
        meshNameOff = bs.readInt()
        meshNameId = bs.readInt()
        texNameIdOff = bs.readInt()
        texNameIdCount = bs.readInt()

        bs.seek(texNameIdOff)
        for i in range(texNameIdCount):
            tNID = bs.readInt()
            self.textureIds.append(tNID)

        bs.seek(boneTableOff1)

        boneTableOff1_Array = []

        for i in range(sectionCount):
            bto1a = bs.readInt()
            boneTableOff1_Array.append(bto1a)

        boneOff_Array = []

        if boneTableOff1_Array[0] != 0:
            for i in range(sectionCount):
                bs.seek(boneTableOff1_Array[i])
                boneOff1 = bs.readInt()
                boneOff2 = bs.readInt()
                boneOff3 = bs.readInt()
                boneParentOff = bs.readInt()
                boneCount = bs.readInt()
                boneOff_Array.append({
                    'boneOff1': boneOff1,
                    'boneOff2': boneOff2,
                    'boneOff3': boneOff3,
                    'boneCount': boneCount,
                    'boneParentOff': boneParentOff
                })

            boneParent_Array = []
            boneChild_Array = []
            EXPParent_Array = []
            EXPChild_Array = []
            boneMatrix_Array = []
            boneName_Array = []
            boneSectionCount = []
            bdCount = 0

            for i in range(sectionCount):
                boneOffTable = boneOff_Array[i]

                if boneOffTable['boneParentOff'] != 0:
                    parentInfos = []
                    parentNameInfos = []
                    bs.seek(boneOffTable['boneParentOff'])
                    parentCount1 = bs.readInt()
                    parentCount2 = bs.readInt()
                    parentCount3 = bs.readInt()
                    parentOff1 = bs.readInt()
                    parentOff2 = bs.readInt()
                    parentOff3 = bs.readInt()
                    parentCount4 = bs.readInt()
                    parentOff4 = bs.readInt()
                    parentOff5 = bs.readInt()
                    bs.seek(parentOff3)
                    pT = bs.readInt()
                    pI = bs.readInt()
                    parentInfos.append({ 'pT': pT, 'pI': pI })

                    while pT != 0 and pI != 0:
                        pT = bs.readInt()
                        pI = bs.readInt()
                        parentInfos.append({ 'pT': pT, 'pI': pI })

                    bs.seek(parentOff4)
                    current = bs.tell()

                    for a in range(parentCount4):
                        bs.seek(current)
                        pNO = bs.readInt()
                        current = bs.tell()
                        bs.seek(pNO)
                        pN = bs.readString()
                        parentNameInfos.append(pN)

                    for a in range(len(parentInfos)):
                        parentInfo = parentInfos[a]
                        bs.seek(parentInfo['pT'])
                        parentType = bs.readString()

                        if parentType == 'OSG':
                            bs.seek(parentInfo['pI'])
                            parentNameOff = bs.readInt()
                            bs.seek(0x28, NOESEEK_REL)
                            childCount = bs.readInt()
                            pNInfoRef1 = bs.readInt()
                            pNInfoRef2 = bs.readInt()
                            bs.seek(parentNameOff)
                            parentName = bs.readString()
                            #print('parent: ' + parentName + ' child: ' + parentNameInfos[(pNInfoRef1 - 0x8000 + 1)])
                            for b in range(childCount):
                                if b == 0:
                                    boneParent_Array.append(parentName)
                                    boneChild_Array.append(parentNameInfos[(pNInfoRef1 - 0x8000 + 1 + b)])
                                else:
                                    boneParent_Array.append(parentNameInfos[(pNInfoRef1 - 0x8000 + b ) ])
                                    boneChild_Array.append(parentNameInfos[(pNInfoRef1 - 0x8000 + 1 + b)])

                        if parentType == 'EXP':
                            bs.seek(parentInfo['pI'])
                            parentNameOff = bs.readInt()
                            bs.seek(0x24, NOESEEK_REL)
                            childNameOff = bs.readInt()
                            bs.seek(parentNameOff)
                            parentName = bs.readString()
                            bs.seek(childNameOff)
                            childName = bs.readString()
                            EXPParent_Array.append(parentName)
                            EXPChild_Array.append(childName)
                            #print('parent: ' + parentName + ' child: ' + childName)
                # bs.seek(boneOffTable['boneOff1'])
                # for a in range(boneOffTable['boneCount']):
                #     bpa = bs.readInt()
                #     boneParent_Array.append(bpa)
                bs.seek(boneOffTable['boneOff2'])

                for a in range(boneOffTable['boneCount']):
                    m01, m11, m21, m31 = bs.read('4f')
                    m02, m12, m22, m32 = bs.read('4f')
                    m03, m13, m23, m33 = bs.read('4f')
                    m04, m14, m24, m34 = bs.read('4f')
                    boneMtx = (NoeMat44( [NoeVec4((m01, m02, m03, m04)), NoeVec4((m11, m12, m13, m14)), NoeVec4((m21, m22, m23, m24)), NoeVec4((m31, m32, m33, m34))]).inverse()).toMat43()
                    boneMatrix_Array.append(boneMtx)
                bs.seek(boneOffTable['boneOff3'])
                boneNameOff_Array = []

                for a in range(boneOffTable['boneCount']):
                    bno = bs.readInt()
                    boneNameOff_Array.append(bno)

                for a in range(boneOffTable['boneCount']):
                    bs.seek(boneNameOff_Array[a])
                    bn = bs.readString()

                    if bn in boneName_Array:
                        bn = bn + '_duplicate_' + str(bdCount)
                        bdCount = bdCount + 1
                    boneName_Array.append(bn)
                boneSectionCount.append(len(boneName_Array))
            #print(boneOffTable['boneOff1'][0])
            #print(boneParent_Array)
            if self.boneData_Array != []:
                boneDataInc_Array = []
                boneDataNotInc_Array = []
                for i in range(len(self.boneData_Array[0])):
                    if self.boneData_Array[0][i] in boneName_Array:
                        boneDataInc_Array.append(self.boneData_Array[0][i])
                    else:
                        boneDataNotInc_Array.append(self.boneData_Array[0][i])
                for i in range(len(boneName_Array)):
                    if boneName_Array[i] in boneDataInc_Array:
                        srch = self.boneData_Array[0].index(boneName_Array[i])
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent]) + len(boneName_Array)
                        newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, parent)
                    else:
                        if boneName_Array[i] in boneChild_Array:
                            srch = boneChild_Array.index(boneName_Array[i])
                            if boneParent_Array[srch] in boneName_Array:
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(boneParent_Array[srch]))
                            elif boneParent_Array[srch] in EXPChild_Array:
                                srch = EXPChild_Array.index(boneParent_Array[srch])
                                if EXPParent_Array[srch] in boneName_Array:
                                    newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                                elif EXPParent_Array[srch] in EXPChild_Array:
                                    srch = EXPChild_Array.index(EXPParent_Array[srch])
                                    if EXPParent_Array[srch] in boneName_Array:
                                        newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                                    else:
                                        print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                                        newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                                else:
                                    print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                                    newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                            elif boneParent_Array[srch] in boneDataNotInc_Array:
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneDataNotInc_Array.index(boneParent_Array[srch]) + len(boneName_Array))
                            else:
                                print(boneParent_Array[srch] + ' ' + boneName_Array[i])
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                        elif boneName_Array[i] in EXPChild_Array:
                            srch = EXPChild_Array.index(boneName_Array[i])
                            if EXPParent_Array[srch] in boneName_Array:
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                            elif EXPParent_Array[srch] in boneDataNotInc_Array:
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneDataNotInc_Array.index(EXPParent_Array[srch]) + len(boneName_Array))
                            elif EXPParent_Array[srch] in EXPChild_Array:
                                srch = EXPChild_Array.index(EXPParent_Array[srch])
                                if EXPParent_Array[srch] in boneName_Array:
                                    newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                                elif EXPParent_Array[srch] in boneDataNotInc_Array:
                                    newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneDataNotInc_Array.index(EXPParent_Array[srch]) + len(boneName_Array))
                                else:
                                    print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                                    newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                            else:
                                print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                        else:
                            newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                    rot = NoeMat43()
                    rot[0] = boneMatrix_Array[i][0]
                    rot[1] = boneMatrix_Array[i][1]
                    rot[2] = boneMatrix_Array[i][2]
                    self.bAnimInfoName.append(boneName_Array[i])
                    self.bAnimInfoRot.append(rot)
                    self.boneList.append(newBone)

                boneDataNotIncMatrix_Array = []

                for i in range(len(boneDataNotInc_Array)):
                    boneMtx = NoeMat43()
                    if boneDataNotInc_Array[i] == 'n_hara_cp':
                        if 'kl_kosi_etc_wj' in boneName_Array:
                            boneMtx[3] = boneMatrix_Array[boneName_Array.index('kl_kosi_etc_wj')][3]
                        else:
                            pass
                    elif boneDataNotInc_Array[i] == 'n_hara':
                        srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneMatrix_Array[parent]
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    elif boneDataNotInc_Array[i] == 'cl_mune':
                        srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                        boneMtx[3] = self.boneData_Array[2][srch][3]
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneMatrix_Array[parent]
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                            rot = NoeAngles((0, 0, 90))
                            mat = rot.toMat43_XYZ()
                            boneMtx[0] = mat[0]
                            boneMtx[1] = mat[1]
                            boneMtx[2] = mat[2]
                    elif boneDataNotInc_Array[i] == 'kl_kubi':
                        if 'n_kubi_wj_ex' in boneName_Array:
                            boneMtx = boneMatrix_Array[boneName_Array.index('n_kubi_wj_ex')]
                        else:
                            srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                            boneMtx[3] = self.boneData_Array[2][srch][3]
                            parent = self.boneData_Array[1][srch]
                            if self.boneData_Array[0][parent] in boneName_Array:
                                parent = boneName_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneMatrix_Array[parent]
                            else:
                                parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    elif boneDataNotInc_Array[i] == 'n_kao' or boneDataNotInc_Array[i] == 'cl_kao':
                        if 'j_kao_wj' in boneName_Array:
                            boneMtx = boneMatrix_Array[boneName_Array.index('j_kao_wj')]
                        else:
                            srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                            boneMtx[3] = self.boneData_Array[2][srch][3]
                            parent = self.boneData_Array[1][srch]
                            if self.boneData_Array[0][parent] in boneName_Array:
                                parent = boneName_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneMatrix_Array[parent]
                            else:
                                parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    elif boneDataNotInc_Array[i] == 'face_root':
                        srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                        boneMtx[3] = self.boneData_Array[2][srch][3]
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneMatrix_Array[parent]
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                            rot = NoeAngles((0, 0, 0))
                            mat = rot.toMat43_XYZ()
                            boneMtx[0] = mat[0]
                            boneMtx[1] = mat[1]
                            boneMtx[2] = mat[2]
                    elif boneDataNotInc_Array[i] == 'c_kata_l':
                        if 'n_skata_l_wj_cd_ex' in boneName_Array:
                            boneMtx = boneMatrix_Array[boneName_Array.index('n_skata_l_wj_cd_ex')]
                        else:
                            srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                            boneMtx[3] = self.boneData_Array[2][srch][3]
                            parent = self.boneData_Array[1][srch]
                            if self.boneData_Array[0][parent] in boneName_Array:
                                parent = boneName_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneMatrix_Array[parent]
                            else:
                                parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    elif boneDataNotInc_Array[i] == 'c_kata_r':
                        if 'n_skata_r_wj_cd_ex' in boneName_Array:
                            boneMtx = boneMatrix_Array[boneName_Array.index('n_skata_r_wj_cd_ex')]
                        else:
                            srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                            boneMtx[3] = self.boneData_Array[2][srch][3]
                            parent = self.boneData_Array[1][srch]
                            if self.boneData_Array[0][parent] in boneName_Array:
                                parent = boneName_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneMatrix_Array[parent]
                            else:
                                parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                                boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    elif boneDataNotInc_Array[i] == 'cl_momo_l':
                        srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                        boneMtx[3] = self.boneData_Array[2][srch][3]
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneMatrix_Array[parent]
                            rot = NoeAngles((0, 0, -90))
                            mat = rot.toMat43_XYZ()
                            boneMtx[0] = mat[0]
                            boneMtx[1] = mat[1]
                            boneMtx[2] = mat[2]
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    elif boneDataNotInc_Array[i] == 'cl_momo_r':
                        srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                        boneMtx[3] = self.boneData_Array[2][srch][3]
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneMatrix_Array[parent]
                            rot = NoeAngles((0, 0, -90))
                            mat = rot.toMat43_XYZ()
                            boneMtx[0] = mat[0]
                            boneMtx[1] = mat[1]
                            boneMtx[2] = mat[2]
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    else:
                        srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                        boneMtx[3] = self.boneData_Array[2][srch][3]
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneMatrix_Array[parent]
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent])
                            boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                    boneDataNotIncMatrix_Array.append(boneMtx)
                for i in range(len(boneDataNotInc_Array)):
                    boneMtx = NoeMat43()
                    if boneDataNotInc_Array[i] != 'n_hara_cp':
                        srch = self.boneData_Array[0].index(boneDataNotInc_Array[i])
                        parent = self.boneData_Array[1][srch]
                        if self.boneData_Array[0][parent] in boneName_Array:
                            parent = boneName_Array.index(self.boneData_Array[0][parent])
                            if boneDataNotInc_Array[i] == 'n_momo_r_cd_ex':
                                parent = boneDataNotInc_Array.index('cl_momo_r') + len(boneName_Array)
                            if boneDataNotInc_Array[i] == 'n_momo_l_cd_ex':
                                parent = boneDataNotInc_Array.index('cl_momo_l') + len(boneName_Array)
                        else:
                            parent = boneDataNotInc_Array.index(self.boneData_Array[0][parent]) + len(boneName_Array)
                        newBone = NoeBone(i+len(boneName_Array), boneDataNotInc_Array[i], boneDataNotIncMatrix_Array[i], None, parent)
                    else:
                        newBone = NoeBone(i+len(boneName_Array), boneDataNotInc_Array[i], boneDataNotIncMatrix_Array[i], None, -1)
                    rot = NoeMat43()
                    rot[0] = boneDataNotIncMatrix_Array[i][0]
                    rot[1] = boneDataNotIncMatrix_Array[i][1]
                    rot[2] = boneDataNotIncMatrix_Array[i][2]
                    self.bAnimInfoName.append(boneDataNotInc_Array[i])
                    self.bAnimInfoRot.append(rot)
                    self.boneList.append(newBone)
            else:
                for i in range(len(boneName_Array)):
                    if boneName_Array[i] in boneChild_Array:
                        srch = boneChild_Array.index(boneName_Array[i])
                        if boneParent_Array[srch] in boneName_Array:
                            newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(boneParent_Array[srch]))
                        elif boneParent_Array[srch] in EXPChild_Array:
                            srch = EXPChild_Array.index(boneParent_Array[srch])
                            if EXPParent_Array[srch] in boneName_Array:
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                            elif EXPParent_Array[srch] in EXPChild_Array:
                                srch = EXPChild_Array.index(EXPParent_Array[srch])
                                if EXPParent_Array[srch] in boneName_Array:
                                    newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                                else:
                                    print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                                    newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                            else:
                                print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                        else:
                            print(boneParent_Array[srch] + ' ' + boneName_Array[i])
                            newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                    elif boneName_Array[i] in EXPChild_Array:
                        srch = EXPChild_Array.index(boneName_Array[i])
                        if EXPParent_Array[srch] in boneName_Array:
                            newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                        elif EXPParent_Array[srch] in EXPChild_Array:
                            srch = EXPChild_Array.index(EXPParent_Array[srch])
                            if EXPParent_Array[srch] in boneName_Array:
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneName_Array.index(EXPParent_Array[srch]))
                            else:
                                print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                                newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                        else:
                            print(EXPParent_Array[srch] + ' ' + boneName_Array[i])
                            newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                    else:
                        newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                    self.boneList.append(newBone)

        meshNameOff_Array = []
        bs.seek(meshNameOff)

        for i in range(sectionCount):
            mno = bs.readInt()
            meshNameOff_Array.append(mno)

        for i in range(sectionCount):
            bs.seek(meshNameOff_Array[i])
            test = bs.readString()

        bs.seek(sectionTableOff)
        baseOff_Array = []

        for i in range(sectionCount):
            bo = bs.readInt()
            baseOff_Array.append(bo)

        matDupCheck = []
        count = 1

        for i in range(sectionCount):
            bs.seek(baseOff_Array[i])
            baseOff = bs.tell()
            bs.seek(0x18, NOESEEK_REL)
            meshCount = bs.readInt()
            meshTableStart = bs.readInt()
            materialCount = bs.readInt()
            materialOffset = bs.readInt()
            bs.seek(materialOffset + baseOff)
            materialNames = []
            uvScales = []

            for a in range(materialCount):
                bs.seek(0x8, NOESEEK_REL)
                matType = bs.readBytes(8).decode('ASCII').rstrip('\0')
                materialInfos = []

                for b in range(8):
                    unk1 = bs.readInt()
                    unk2 = bs.readInt()
                    textureId = bs.readInt()
                    texType = bs.readInt()

                    if b == 0:
                        bs.seek(0xc, NOESEEK_REL)
                        uvX = bs.readFloat()
                        bs.seek(0x10, NOESEEK_REL)
                        uvY = bs.readFloat()
                        bs.seek(0x10, NOESEEK_REL)
                        uvZ = bs.readFloat()
                        uvScales.append([uvX, uvY, uvZ])
                        bs.seek(0x30, NOESEEK_REL)
                    else:
                        bs.seek(0x68, NOESEEK_REL)

                    materialInfos.append({ 'texType': texType, 'textureId': textureId })

                bs.seek(0x8, NOESEEK_REL)
                diffColour = bs.read('4f')
                ambiColour = bs.read('4f')
                specColour = bs.read('4f')
                lightColour = bs.read('4f')
                specPower = bs.readFloat()
                bs.seek(0x14, NOESEEK_REL)
                matName = bs.readBytes(64).decode('ASCII').rstrip('\0')
                bs.seek(0x40, NOESEEK_REL)

                if matName in matDupCheck:
                    matName = matName + '_' + str(count)
                    count += 1
                else:
                    pass

                matDupCheck.append(matName)
                material = NoeMaterial(matType + '_' + matName, '')

                for b in range(8):
                    materialInfo = materialInfos[b]
                    texType = materialInfo['texType']
                    textureId = materialInfo['textureId']

                    if texType == 0xf1 and b == 0:
                        material.setTexture(self.textureIdToName[textureId])
                    elif texType == 0xf2:
                        material.setNormalTexture(self.textureIdToName[textureId])
                    elif texType == 0xf3:
                        material.setSpecularTexture(self.textureIdToName[textureId])
                    elif texType == 0x3f9:
                        material.setEnvTexture(self.textureIdToName[textureId])
                    else:
                        pass

                material.setDiffuseColor(diffColour)
                material.setSpecularColor([specColour[0], specColour[1], specColour[2], specPower])
                self.matList.append(material)
                materialNames.append(matType + '_' + matName)
            bs.seek(meshTableStart + baseOff)
            offsetInfo_Array = []

            for a in range(meshCount):
                bs.seek(0x14, NOESEEK_REL)
                meshFaceSectionCount = bs.readInt()
                meshFaceHeaderOff = bs.readInt()
                C13_17 = bs.readInt()
                num50 = bs.readInt()
                vertCount = bs.readInt()
                vertStart = bs.readInt()
                normalStart = bs.readInt()
                vertColourStart = bs.readInt()
                null01 = bs.readInt()
                uvStart = bs.readInt()
                bs.seek(0x14, NOESEEK_REL)
                weightStart = bs.readInt()
                boneIdStart = bs.readInt()
                faceStart = ((boneIdStart + baseOff) + (0x10 * vertStart))
                bs.seek(0x40, NOESEEK_REL)
                meshName = bs.readBytes(64).decode('ASCII').rstrip('\0')
                offsetInfo_Array.append({
                    'meshFaceSectionCount': meshFaceSectionCount,
                    'meshFaceHeaderOff': meshFaceHeaderOff + baseOff,
                    'vertCount': vertCount,
                    'vertStart': vertStart + baseOff,
                    'normalStart': normalStart + baseOff,
                    'vertColourStart': vertColourStart + baseOff,
                    'uvStart': uvStart + baseOff,
                    'weightStart': weightStart + baseOff,
                    'boneIdStart': boneIdStart + baseOff,
                    'faceStart': faceStart,
                    'meshName': meshName
                })

            for a in range(meshCount):
                faceInfo_Array = []
                offsetInfo = offsetInfo_Array[a]
                bs.seek(offsetInfo['meshFaceHeaderOff'])

                for b in range(offsetInfo['meshFaceSectionCount']):
                    bs.seek(0x14, NOESEEK_REL)
                    matNumber = bs.readInt()
                    bs.seek(0x8, NOESEEK_REL)
                    fCount1 = bs.readInt()
                    fOffset1 = bs.readInt()
                    num4 = bs.readInt()
                    fType = bs.readInt()
                    num1 = bs.readInt()
                    fCount2 = bs.readInt()
                    fOffset2 = bs.readInt()
                    bs.seek(0x20, NOESEEK_REL)
                    faceInfo_Array.append({
                        'fCount1': fCount1,
                        'fOffset1': fOffset1 + baseOff,
                        'num4': num4,
                        'fType': fType,
                        'matNumber': matNumber,
                        'fCount2': fCount2,
                        'fOffset2': fOffset2 + baseOff
                    })

                if boneTableOff1_Array[0] != 0:
                    bs.seek(offsetInfo['boneIdStart'])
                    boneIndexBuffer = 0

                    for b in range(offsetInfo['vertCount']):
                        bi1, bi2, bi3, bi4 = bs.read('4f')
                        if bi1 == 255:
                            bi1 = 0
                        if bi2 == 255:
                            bi2 = 0
                        if bi3 == 255:
                            bi3 = 0
                        if bi4 == 255:
                            bi4 = 0
                        if offsetInfo['boneIdStart'] == baseOff:
                            bi1 = 3
                            bi2 = 0
                            bi3 = 0
                            bi4 = 0
                        if b == 0:
                            boneIndexBuffer = struct.pack('i', int(int(bi1)/3.0))
                        else:
                            boneIndexBuffer = boneIndexBuffer + struct.pack('i', int(int(bi1)/3.0))

                        boneIndexBuffer = boneIndexBuffer + struct.pack('i', int(int(bi2)/3.0))
                        boneIndexBuffer = boneIndexBuffer + struct.pack('i', int(int(bi3)/3.0))
                        boneIndexBuffer = boneIndexBuffer + struct.pack('i', int(int(bi4)/3.0))
                    boneIndexMap = []
                    biFix = 0

                    if i > 1:
                        biFix = biFix + boneSectionCount[i-1]

                    for b in range(offsetInfo['meshFaceSectionCount']):
                        faceInfo = faceInfo_Array[b]
                        bs.seek(faceInfo['fOffset1'])
                        bim = []
                        for c in range(faceInfo['fCount1']):
                            bim2 = bs.readShort()
                            bim.append(bim2 + biFix)
                        if offsetInfo['boneIdStart'] == baseOff:
                            boneIndexMap.append([0, boneName_Array.index('kl_kosi_etc_wj')])
                        else:
                            boneIndexMap.append(bim)

                rapi.rpgSetName(offsetInfo['meshName'])
                bs.seek(offsetInfo['vertStart'])
                vertBuff = bs.readBytes(offsetInfo['vertCount'] * 0xc)
                bs.seek(offsetInfo['normalStart'])
                normalBuff = bs.readBytes(offsetInfo['vertCount'] * 0xc)
                bs.seek(offsetInfo['vertColourStart'])
                colourBuff = bs.readBytes(offsetInfo['vertCount'] * 0x10)
                bs.seek(offsetInfo['uvStart'])
                uvBuff = bs.readBytes(offsetInfo['vertCount'] * 0x8)

                if boneTableOff1_Array[0] != 0:
                    bs.seek(offsetInfo['weightStart'])
                    weightBuff = bs.readBytes(offsetInfo['vertCount'] * 0x10)
                    boneBuff = boneIndexBuffer

                if offsetInfo['boneIdStart'] == baseOff:
                    for b in range(offsetInfo['vertCount']):
                        if b == 0:
                            weightBuff = struct.pack('f', 1)
                        else:
                            weightBuff = weightBuff + struct.pack('f', 1)
                        weightBuff = weightBuff + struct.pack('f', 0)
                        weightBuff = weightBuff + struct.pack('f', 0)
                        weightBuff = weightBuff + struct.pack('f', 0)

                rapi.rpgBindPositionBufferOfs(vertBuff, noesis.RPGEODATA_FLOAT, 12, 0)
                rapi.rpgBindNormalBufferOfs(normalBuff, noesis.RPGEODATA_FLOAT, 12, 0)
                #rapi.rpgBindColorBufferOfs(colourBuff, noesis.RPGEODATA_FLOAT, 16, 0, 4)
                rapi.rpgBindUV1BufferOfs(uvBuff, noesis.RPGEODATA_FLOAT, 8, 0)

                if boneTableOff1_Array[0]:
                    rapi.rpgBindBoneWeightBufferOfs(weightBuff, noesis.RPGEODATA_FLOAT, 16, 0, 4)
                    rapi.rpgBindBoneIndexBufferOfs(boneBuff, noesis.RPGEODATA_INT, 16, 0, 4)

                for b in range(offsetInfo['meshFaceSectionCount']):
                    bs.seek(faceInfo['fOffset2'])
                    uvScale = uvScales[faceInfo['matNumber']]
                    rapi.rpgSetUVScaleBias(NoeVec3 ((uvScale[0], uvScale[1], uvScale[2])), NoeVec3 ((1.0, 1.0, 1.0)))
                    if boneTableOff1_Array[0] != 0:
                        rapi.rpgSetBoneMap(boneIndexMap[b])
                    faceBuff = bs.readBytes(faceInfo['fCount2'] * 2)
                    rapi.rpgSetMaterial(materialNames[faceInfo['matNumber']])
                    rapi.rpgCommitTriangles(faceBuff, noesis.RPGEODATA_USHORT, faceInfo['fCount2'], noesis.RPGEO_TRIANGLE_STRIP, 1)

    def load_binTex(self):
        binTex = rapi.loadIntoByteArray( rapi.getDirForFilePath( rapi.getLastCheckedName() ) + self.baseName + '_tex.bin' )
        bs = NoeBitStream(binTex)
        idString = bs.readInt()
        texCount = bs.readInt()
        unk1 = bs.readInt()
        texOffList = []
        for i in range(texCount):
            tOL = bs.readInt()
            texOffList.append(tOL)
        for i in range(texCount):
            bs.seek(texOffList[i])
            txp = bs.readInt()
            txpMips = bs.readInt()
            unk2 = bs.readInt()
            texOff = bs.readInt()
            bs.seek(texOffList[i] + texOff)
            txpHeader = bs.read('6i')
            txpData = bs.readBytes(txpHeader[5])
            texFmt = 0
            if txpHeader[3] == 6:
                texFmt = noesis.NOESISTEX_DXT1
            if txpHeader[3] == 7:
                texFmt = noesis.NOESISTEX_DXT3
            if txpHeader[3] == 9:
                texFmt = noesis.NOESISTEX_DXT5
            if txpHeader[3] == 11:
                txpData = rapi.imageDecodeDXT(txpData, int(txpHeader[1]), int(txpHeader[2]), noesis.FOURCC_ATI2)
                texFmt = noesis.NOESISTEX_RGBA32
            name = self.textureIdToName[self.textureIds[i]]
            tex1 = NoeTexture(name, int(txpHeader[1]), int(txpHeader[2]), txpData, texFmt)
            self.texList.append(tex1)
        return 1

    def load_binTexDB(self):
        binTexDB = rapi.loadIntoByteArray(rapi.getDirForFilePath( rapi.getLastCheckedName() ) + 'tex_db.bin')
        bs = NoeBitStream(binTexDB)
        texCount = bs.readInt()
        texNameTableOff = bs.readInt()
        bs.seek(texNameTableOff)
        currentOff = bs.tell()

        for i in range(texCount):
            bs.seek(currentOff)
            texNameID = bs.readInt()
            texNameOff = bs.readInt()
            currentOff = bs.tell()
            bs.seek(texNameOff)
            texName = bs.readString()
            self.textureIdToName[texNameID] = texName

    def load_binBone(self):
        binBone = rapi.loadIntoByteArray(rapi.getDirForFilePath( rapi.getLastCheckedName() ) + 'bone_data.bin')
        bs = NoeBitStream(binBone)
        idString = bs.readInt()
        sectionCount = bs.readInt()
        skeletonsOff = bs.readInt()
        unk1 = bs.readInt()
        skeletonInfo = []
        character = []
        bs.seek(skeletonsOff)
        for i in range(sectionCount):
            sI = bs.readInt()
            skeletonInfo.append(sI)
        for i in range(sectionCount):
            character.append(bs.readString())
        characterName = self.baseName[:-6]
        if characterName.upper() in character:
            bs.seek(skeletonInfo[character.index(characterName.upper())])
        else:
            bs.seek(skeletonInfo[0])
        unk2 = bs.readInt()
        skelCount1 = bs.readInt()
        skelMatrixOff = bs.readInt()
        unk3 = bs.readInt()
        skelCount2 = bs.readInt()
        skelNameOff1 = bs.readInt()
        skelCount3 = bs.readInt()
        skelNameOff2 = bs.readInt()
        skelParents = bs.readInt()
        boneMatrix_Array = []
        bs.seek(skelMatrixOff)
        for i in range(skelCount1):
            m01, m02, m03 = bs.read('3f')
            boneMatrix_Array.append((m01, m02, m03))
        boneNames1_Array = []
        bs.seek(skelNameOff1)
        current = bs.tell()
        for i in range(skelCount2):
            bs.seek(current)
            boneNameOff = bs.readInt()
            current = bs.tell()
            bs.seek(boneNameOff)
            boneNames1_Array.append(bs.readString())
        boneNames2_Array = []
        bs.seek(skelNameOff2)
        current = bs.tell()
        for i in range(skelCount3):
            bs.seek(current)
            boneNameOff = bs.readInt()
            current = bs.tell()
            bs.seek(boneNameOff)
            boneNames2_Array.append(bs.readString())
        boneParent_Array = []
        bs.seek(skelParents)
        for i in range(skelCount3):
            bpa = bs.readShort()
            boneParent_Array.append(bpa)
        bones = []
        for i in range(skelCount3):
            if boneNames2_Array[i] in boneNames1_Array:
                index = boneNames1_Array.index(boneNames2_Array[i])
                pos = NoeVec3(boneMatrix_Array[index+2])
            else:
                pos = NoeVec3((0, 0, 0))
            boneMtx = NoeMat43()
            boneMtx[3] = pos
            bones.append(boneMtx)
        self.boneData_Array.append(boneNames2_Array)
        self.boneData_Array.append(boneParent_Array)
        self.boneData_Array.append(bones)

def texBinCheckType(data):
    bs = NoeBitStream(data)
    header = bs.readInt()
    if len(data) < 4:
        return 0
    if header != 0x03505854:
        return 0
    return 1

def texBinLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    idString = bs.readInt()
    texCount = bs.readInt()
    unk1 = bs.readInt()
    texOffList = []
    for i in range(texCount):
        tOL = bs.readInt()
        texOffList.append(tOL)
    for i in range(texCount):
        bs.seek(texOffList[i])
        txp = bs.readInt()
        txpMips = bs.readInt()
        unk2 = bs.readInt()
        texOff = bs.readInt()
        bs.seek(texOffList[i] + texOff)
        txpHeader = bs.read('6i')
        txpData = bs.readBytes(txpHeader[5])
        texFmt = 0
        if txpHeader[3] == 6:
            texFmt = noesis.NOESISTEX_DXT1
        if txpHeader[3] == 7:
            texFmt = noesis.NOESISTEX_DXT3
        if txpHeader[3] == 9:
            texFmt = noesis.NOESISTEX_DXT5
        if txpHeader[3] == 11:
            txpData = rapi.imageDecodeDXT(txpData, int(txpHeader[1]), int(txpHeader[2]), noesis.FOURCC_ATI2)
            texFmt = noesis.NOESISTEX_RGBA32
        name = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))
        name = name[:-4]
        tex1 = NoeTexture(name + '_' + str(i), int(txpHeader[1]), int(txpHeader[2]), txpData, texFmt)
        texList.append(tex1)
    return 1
