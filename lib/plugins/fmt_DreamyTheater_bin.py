#By Minmode
#Based on max script by Chrrox

from inc_noesis import *
import noesis
import rapi

def registerNoesisTypes():
   handle = noesis.register("Project Diva Dreamy Theater Model", ".bin")
   noesis.setHandlerTypeCheck(handle, objBinCheckType)
   noesis.setHandlerLoadModel(handle, objBinLoadModel)

   handle = noesis.register("Project Diva Dreamy Theater Texture", ".bin")
   noesis.setHandlerTypeCheck(handle, texBinCheckType)
   noesis.setHandlerLoadRGBA(handle, texBinLoadRGBA)
   return 1

def objBinCheckType(data):
   bs = NoeBitStream(data)
   header = bs.read("i")
   if len(data) < 4:
      return 0
   if header[0] != 0x05062500:
      return 0
   return 1

def texBinCheckType(data):
   bs = NoeBitStream(data)
   header = bs.read("i")
   if len(data) < 4:
      return 0
   if header[0] != 0x03505854:
      return 0
   return 1

def objBinLoadModel(data, mdlList):
   ctx = rapi.rpgCreateContext()
   bs = NoeBitStream(data)
   # print("print")

   global  texList, matList, tex_DB, texNameId_Array, boneData_Array, boneList, kfBones, baseName, bAnimInfoName, bAnimInfoRot
   texList = []
   matList = []
   tex_DB = {}
   texNameId_Array = []
   boneData_Array = []
   boneList = []
   kfBones = []
   animList = []
   bAnimInfoName = []
   bAnimInfoRot = []

   baseName = rapi.getExtensionlessName(rapi.getLocalFileName(rapi.getLastCheckedName()))
   baseName = baseName[:-4]

   binTexDB = rapi.loadIntoByteArray(rapi.getDirForFilePath( rapi.getLastCheckedName() ) + "tex_db.bin")
   load_binTexDB(binTexDB)

   binBone = rapi.loadIntoByteArray(rapi.getDirForFilePath( rapi.getLastCheckedName() ) + "bone_data.bin")
   load_binBone(binBone)

   load_BinModel(bs)

   binTex = rapi.loadIntoByteArray( rapi.getDirForFilePath( rapi.getLastCheckedName() ) + baseName + "_tex.bin" )
   load_binTex(binTex, texList)

   mdl = rapi.rpgConstructModel()
   mdlList.append(mdl)
   mdl.setBones(boneList)
   if texList != []:
      mdl.setModelMaterials(NoeModelMaterials(texList, matList))
   if animList != []:
      mdl.setAnims(animList)
      rapi.setPreviewOption("setAnimSpeed", "60")

   rapi.rpgClearBufferBinds()
   return 1

def load_BinModel(bs):
   idString = bs.read("i")
   sectionCount = bs.read("i")
   boneCount = bs.read("i")
   sectionTableOff = bs.read("i")
   boneTableOff1 = bs.read("i")
   meshNameOff = bs.read("i")
   meshNameId = bs.read("i")
   texNameIdOff = bs.read("i")
   texNameIdCount = bs.read("i")

   bs.seek(texNameIdOff[0], NOESEEK_ABS)
   for i in range(0, texNameIdCount[0]):
      tNID = bs.read("i")
      texNameId_Array.append(tNID[0])

   bs.seek(boneTableOff1[0], NOESEEK_ABS)
   boneTableOff1_Array = []
   for i in range(0, sectionCount[0]):
      bto1a = bs.read("i")
      boneTableOff1_Array.append(bto1a[0])
   boneOff_Array = []
   if boneTableOff1_Array[0] != 0:
      for i in range(0, sectionCount[0]):
         bs.seek(boneTableOff1_Array[i], NOESEEK_ABS)
         boneOff1 = bs.read("i")
         boneOff2 = bs.read("i")
         boneOff3 = bs.read("i")
         boneParentOff = bs.read("i")
         boneCount = bs.read("i")
         boneOff_Array.append([boneOff1[0], boneOff2[0], boneOff3[0], boneCount[0], boneParentOff[0]])
      boneParent_Array = []
      boneChild_Array = []
      EXPParent_Array = []
      EXPChild_Array = []
      boneMatrix_Array = []
      boneName_Array = []
      boneSectionCount = []
      bdCount = 0
      for i in range(0, sectionCount[0]):
         if boneOff_Array[i][4] != 0:
            parentInfo = []
            parentNameInfo = []
            bs.seek(boneOff_Array[i][4], NOESEEK_ABS)
            parentCount1 = bs.read("i")
            parentCount2 = bs.read("i")
            parentCount3 = bs.read("i")
            parentOff1 = bs.read("i")
            parentOff2 = bs.read("i")
            parentOff3 = bs.read("i")
            parentCount4 = bs.read("i")
            parentOff4 = bs.read("i")
            parentOff5 = bs.read("i")
            bs.seek(parentOff3[0], NOESEEK_ABS)
            pT = bs.read("i")
            pI = bs.read("i")
            parentInfo.append([pT[0], pI[0]])
            while pT[0] != 0 and pT[0] != 0:
               pT = bs.read("i")
               pI = bs.read("i")
               parentInfo.append([pT[0], pI[0]])
            bs.seek(parentOff4[0], NOESEEK_ABS)
            current = bs.tell()
            for a in range(0, parentCount4[0]):
               bs.seek(current, NOESEEK_ABS)
               pNO = bs.read("i")
               current = bs.tell()
               bs.seek(pNO[0], NOESEEK_ABS)
               pN = bs.readString()
               parentNameInfo.append(pN)
            for a in range(0, len(parentInfo)):
               bs.seek(parentInfo[a][0], NOESEEK_ABS)
               parentType = bs.readString()
               if parentType == "OSG":
                  bs.seek(parentInfo[a][1], NOESEEK_ABS)
                  parentNameOff = bs.read("i")
                  bs.seek(0x28, NOESEEK_REL)
                  childCount = bs.read("i")
                  pNInfoRef1 = bs.read("i")
                  pNInfoRef2 = bs.read("i")
                  bs.seek(parentNameOff[0], NOESEEK_ABS)
                  parentName = bs.readString()
                  #print("parent: " + parentName + " child: " + parentNameInfo[(pNInfoRef1[0]-0x8000+1)])
                  for b in range(0, childCount[0]):
                     if b == 0:
                        boneParent_Array.append(parentName)
                        boneChild_Array.append(parentNameInfo[(pNInfoRef1[0]-0x8000+1+b)])
                     else:
                        boneParent_Array.append(parentNameInfo[(pNInfoRef1[0]-0x8000+b)])
                        boneChild_Array.append(parentNameInfo[(pNInfoRef1[0]-0x8000+1+b)])
               if parentType == "EXP":
                  bs.seek(parentInfo[a][1], NOESEEK_ABS)
                  parentNameOff = bs.read("i")
                  bs.seek(0x24, NOESEEK_REL)
                  childNameOff = bs.read("i")
                  bs.seek(parentNameOff[0], NOESEEK_ABS)
                  parentName = bs.readString()
                  bs.seek(childNameOff[0], NOESEEK_ABS)
                  childName = bs.readString()
                  EXPParent_Array.append(parentName)
                  EXPChild_Array.append(childName)
                  #print("parent: " + parentName + " child: " + childName)
##         bs.seek(boneOff_Array[i][0], NOESEEK_ABS)
##         for a in range(0, boneOff_Array[i][3]):
##            bpa = bs.read("i")
##            boneParent_Array.append(bpa[0])
         bs.seek(boneOff_Array[i][1], NOESEEK_ABS)
         for a in range(0, boneOff_Array[i][3]):
            m01, m11, m21, m31 = bs.read("4f")
            m02, m12, m22, m32 = bs.read("4f")
            m03, m13, m23, m33 = bs.read("4f")
            m04, m14, m24, m34 = bs.read("4f")
            boneMtx = (NoeMat44( [NoeVec4((m01, m02, m03, m04)), NoeVec4((m11, m12, m13, m14)), NoeVec4((m21, m22, m23, m24)), NoeVec4((m31, m32, m33, m34))]).inverse()).toMat43()
            boneMatrix_Array.append(boneMtx)
         bs.seek(boneOff_Array[i][2], NOESEEK_ABS)
         boneNameOff_Array = []
         for a in range(0, boneOff_Array[i][3]):
            bno = bs.read("i")
            boneNameOff_Array.append(bno[0])
         for a in range(0, boneOff_Array[i][3]):
            bs.seek(boneNameOff_Array[a], NOESEEK_ABS)
            bn = bs.readString()
            if bn in boneName_Array:
               bn = bn + "_duplicate_" + str(bdCount)
               bdCount = bdCount + 1
            boneName_Array.append(bn)
         boneSectionCount.append(len(boneName_Array))
      #print(boneOff_Array[0][0])
      #print(boneParent_Array)
      if boneData_Array != []:
         boneDataInc_Array = []
         boneDataNotInc_Array = []
         for i in range(0, len(boneData_Array[0])):
            if boneData_Array[0][i] in boneName_Array:
               boneDataInc_Array.append(boneData_Array[0][i])
            else:
               boneDataNotInc_Array.append(boneData_Array[0][i])
         for i in range(0, len(boneName_Array)):
            if boneName_Array[i] in boneDataInc_Array:
               srch = boneData_Array[0].index(boneName_Array[i])
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent]) + len(boneName_Array)
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
                           print(EXPParent_Array[srch] + " " + boneName_Array[i])
                           newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                     else:
                        print(EXPParent_Array[srch] + " " + boneName_Array[i])
                        newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                  elif boneParent_Array[srch] in boneDataNotInc_Array:
                     newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, boneDataNotInc_Array.index(boneParent_Array[srch]) + len(boneName_Array))
                  else:
                     print(boneParent_Array[srch] + " " + boneName_Array[i])
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
                        print(EXPParent_Array[srch] + " " + boneName_Array[i])
                        newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                  else:
                     print(EXPParent_Array[srch] + " " + boneName_Array[i])
                     newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
               else:
                  newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
            rot = NoeMat43()
            rot[0] = boneMatrix_Array[i][0]
            rot[1] = boneMatrix_Array[i][1]
            rot[2] = boneMatrix_Array[i][2]
            bAnimInfoName.append(boneName_Array[i])
            bAnimInfoRot.append(rot)
            boneList.append(newBone)
         boneDataNotIncMatrix_Array = []
         for i in range(0, len(boneDataNotInc_Array)):
            boneMtx = NoeMat43()
            if boneDataNotInc_Array[i] == "n_hara_cp":
               if "kl_kosi_etc_wj" in boneName_Array:
                  boneMtx[3] = boneMatrix_Array[boneName_Array.index("kl_kosi_etc_wj")][3]
               else:
                  pass
            elif boneDataNotInc_Array[i] == "n_hara":
               srch = boneData_Array[0].index(boneDataNotInc_Array[i])
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneMatrix_Array[parent]
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            elif boneDataNotInc_Array[i] == "cl_mune":
               srch = boneData_Array[0].index(boneDataNotInc_Array[i])
               boneMtx[3] = boneData_Array[2][srch][3]
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneMatrix_Array[parent]
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                  rot = NoeAngles((0, 0, 90))
                  mat = rot.toMat43_XYZ()
                  boneMtx[0] = mat[0]
                  boneMtx[1] = mat[1]
                  boneMtx[2] = mat[2]
            elif boneDataNotInc_Array[i] == "kl_kubi":
               if "n_kubi_wj_ex" in boneName_Array:
                  boneMtx = boneMatrix_Array[boneName_Array.index("n_kubi_wj_ex")]
               else:
                  srch = boneData_Array[0].index(boneDataNotInc_Array[i])
                  boneMtx[3] = boneData_Array[2][srch][3]
                  parent = boneData_Array[1][srch]
                  if boneData_Array[0][parent] in boneName_Array:
                     parent = boneName_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneMatrix_Array[parent]
                  else:
                     parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            elif boneDataNotInc_Array[i] == "n_kao" or boneDataNotInc_Array[i] == "cl_kao":
               if "j_kao_wj" in boneName_Array:
                  boneMtx = boneMatrix_Array[boneName_Array.index("j_kao_wj")]
               else:
                  srch = boneData_Array[0].index(boneDataNotInc_Array[i])
                  boneMtx[3] = boneData_Array[2][srch][3]
                  parent = boneData_Array[1][srch]
                  if boneData_Array[0][parent] in boneName_Array:
                     parent = boneName_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneMatrix_Array[parent]
                  else:
                     parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            elif boneDataNotInc_Array[i] == "face_root":
               srch = boneData_Array[0].index(boneDataNotInc_Array[i])
               boneMtx[3] = boneData_Array[2][srch][3]
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneMatrix_Array[parent]
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
                  rot = NoeAngles((0, 0, 0))
                  mat = rot.toMat43_XYZ()
                  boneMtx[0] = mat[0]
                  boneMtx[1] = mat[1]
                  boneMtx[2] = mat[2]
            elif boneDataNotInc_Array[i] == "c_kata_l":
               if "n_skata_l_wj_cd_ex" in boneName_Array:
                  boneMtx = boneMatrix_Array[boneName_Array.index("n_skata_l_wj_cd_ex")]
               else:
                  srch = boneData_Array[0].index(boneDataNotInc_Array[i])
                  boneMtx[3] = boneData_Array[2][srch][3]
                  parent = boneData_Array[1][srch]
                  if boneData_Array[0][parent] in boneName_Array:
                     parent = boneName_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneMatrix_Array[parent]
                  else:
                     parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            elif boneDataNotInc_Array[i] == "c_kata_r":
               if "n_skata_r_wj_cd_ex" in boneName_Array:
                  boneMtx = boneMatrix_Array[boneName_Array.index("n_skata_r_wj_cd_ex")]
               else:
                  srch = boneData_Array[0].index(boneDataNotInc_Array[i])
                  boneMtx[3] = boneData_Array[2][srch][3]
                  parent = boneData_Array[1][srch]
                  if boneData_Array[0][parent] in boneName_Array:
                     parent = boneName_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneMatrix_Array[parent]
                  else:
                     parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                     boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            elif boneDataNotInc_Array[i] == "cl_momo_l":
               srch = boneData_Array[0].index(boneDataNotInc_Array[i])
               boneMtx[3] = boneData_Array[2][srch][3]
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneMatrix_Array[parent]
                  rot = NoeAngles((0, 0, -90))
                  mat = rot.toMat43_XYZ()
                  boneMtx[0] = mat[0]
                  boneMtx[1] = mat[1]
                  boneMtx[2] = mat[2]
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            elif boneDataNotInc_Array[i] == "cl_momo_r":
               srch = boneData_Array[0].index(boneDataNotInc_Array[i])
               boneMtx[3] = boneData_Array[2][srch][3]
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneMatrix_Array[parent]
                  rot = NoeAngles((0, 0, -90))
                  mat = rot.toMat43_XYZ()
                  boneMtx[0] = mat[0]
                  boneMtx[1] = mat[1]
                  boneMtx[2] = mat[2]
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            else:
               srch = boneData_Array[0].index(boneDataNotInc_Array[i])
               boneMtx[3] = boneData_Array[2][srch][3]
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneMatrix_Array[parent]
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent])
                  boneMtx = boneMtx * boneDataNotIncMatrix_Array[parent]
            boneDataNotIncMatrix_Array.append(boneMtx)
         for i in range(0, len(boneDataNotInc_Array)):
            boneMtx = NoeMat43()
            if boneDataNotInc_Array[i] != "n_hara_cp":
               srch = boneData_Array[0].index(boneDataNotInc_Array[i])
               parent = boneData_Array[1][srch]
               if boneData_Array[0][parent] in boneName_Array:
                  parent = boneName_Array.index(boneData_Array[0][parent])
                  if boneDataNotInc_Array[i] == "n_momo_r_cd_ex":
                     parent = boneDataNotInc_Array.index("cl_momo_r") + len(boneName_Array)
                  if boneDataNotInc_Array[i] == "n_momo_l_cd_ex":
                     parent = boneDataNotInc_Array.index("cl_momo_l") + len(boneName_Array)
               else:
                  parent = boneDataNotInc_Array.index(boneData_Array[0][parent]) + len(boneName_Array)
               newBone = NoeBone(i+len(boneName_Array), boneDataNotInc_Array[i], boneDataNotIncMatrix_Array[i], None, parent)
            else:
               newBone = NoeBone(i+len(boneName_Array), boneDataNotInc_Array[i], boneDataNotIncMatrix_Array[i], None, -1)
            rot = NoeMat43()
            rot[0] = boneDataNotIncMatrix_Array[i][0]
            rot[1] = boneDataNotIncMatrix_Array[i][1]
            rot[2] = boneDataNotIncMatrix_Array[i][2]
            bAnimInfoName.append(boneDataNotInc_Array[i])
            bAnimInfoRot.append(rot)
            boneList.append(newBone)
      else:
         for i in range(0, len(boneName_Array)):
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
                        print(EXPParent_Array[srch] + " " + boneName_Array[i])
                        newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
                  else:
                     print(EXPParent_Array[srch] + " " + boneName_Array[i])
                     newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
               else:
                  print(boneParent_Array[srch] + " " + boneName_Array[i])
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
                     print(EXPParent_Array[srch] + " " + boneName_Array[i])
                     newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
               else:
                  print(EXPParent_Array[srch] + " " + boneName_Array[i])
                  newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
            else:
               newBone = NoeBone(i, boneName_Array[i], boneMatrix_Array[i], None, -1)
            boneList.append(newBone)

   meshNameOff_Array = []
   bs.seek(meshNameOff[0], NOESEEK_ABS)
   for i in range(0, sectionCount[0]):
      mno = bs.read("i")
      meshNameOff_Array.append(mno[0])
   for i in range(0, sectionCount[0]):
      bs.seek(meshNameOff_Array[i], NOESEEK_ABS)
      test = bs.readString()
   bs.seek(sectionTableOff[0], NOESEEK_ABS)
   baseOff_Array = []
   for i in range(0, sectionCount[0]):
      bo = bs.read("i")
      baseOff_Array.append(bo[0])
   matDupCheck = []
   count = 1
   for i in range(0, sectionCount[0]):
      bs.seek(baseOff_Array[i], NOESEEK_ABS)
      baseOff = bs.tell()
      bs.seek(0x18, NOESEEK_REL)
      meshCount = bs.read("i")
      meshTableStart = bs.read("i")
      materialCount = bs.read("i")
      materialOffset = bs.read("i")
      bs.seek(materialOffset[0] + baseOff, NOESEEK_ABS)
      materialNames = []
      uvScales = []
      for a in range(0, materialCount[0]):
         bs.seek(0x8, NOESEEK_REL)
         matType = bs.readBytes(8).decode("ASCII").rstrip("\0")
         materialInfo = []
         for b in range(0, 8):
            unk1 = bs.read("i")
            unk2 = bs.read("i")
            texDB_ID = bs.read("i")
            texType = bs.read("i")
            if b == 0:
               bs.seek(0xc, NOESEEK_REL)
               uvX = bs.read("f")
               bs.seek(0x10, NOESEEK_REL)
               uvY = bs.read("f")
               bs.seek(0x10, NOESEEK_REL)
               uvZ = bs.read("f")
               uvScales.append([uvX[0], uvY[0], uvZ[0]])
               bs.seek(0x30, NOESEEK_REL)
            else:
               bs.seek(0x68, NOESEEK_REL)
            materialInfo.append([texType[0], texDB_ID[0]])
         bs.seek(0x8, NOESEEK_REL)
         diffColour = bs.read("4f")
         ambiColour = bs.read("4f")
         specColour = bs.read("4f")
         lightColour = bs.read("4f")
         specPower = bs.read("f")
         bs.seek(0x14, NOESEEK_REL)
         matName = bs.readBytes(64).decode("ASCII").rstrip("\0")
         bs.seek(0x40, NOESEEK_REL)
         if matName in matDupCheck:
            matName = matName + "_" + str(count)
            count += 1
         else:
            pass
         matDupCheck.append(matName)
         material = NoeMaterial(matType + "_" + matName, "")
         for b in range(0, 8):
            if materialInfo[b][0] == 0xf1 and b == 0:
               material.setTexture(tex_DB[materialInfo[b][1]])
            elif materialInfo[b][0] == 0xf2:
               material.setNormalTexture(tex_DB[materialInfo[b][1]])
            elif materialInfo[b][0] == 0xf3:
               material.setSpecularTexture(tex_DB[materialInfo[b][1]])
            elif materialInfo[b][0] == 0x3f9:
               material.setEnvTexture(tex_DB[materialInfo[b][1]])
            else:
               pass
         material.setDiffuseColor(diffColour)
         material.setSpecularColor([specColour[0], specColour[1], specColour[2], specPower[0]])
         matList.append(material)
         materialNames.append(matType + "_" + matName)
      bs.seek(meshTableStart[0] + baseOff, NOESEEK_ABS)
      offsetInfo_Array = []
      for a in range(0, meshCount[0]):
         bs.seek(0x14, NOESEEK_REL)
         meshFaceSectionCount = bs.read("i")
         meshFaceHeaderOff = bs.read("i")
         C13_17 = bs.read("i")
         num50 = bs.read("i")
         vertCount = bs.read("i")
         vertStart = bs.read("i")
         normalStart = bs.read("i")
         vertColourStart = bs.read("i")
         null01 = bs.read("i")
         uvStart = bs.read("i")
         bs.seek(0x14, NOESEEK_REL)
         weightStart = bs.read("i")
         boneIdStart = bs.read("i")
         faceStart = ((boneIdStart[0] + baseOff) + (0x10 * vertStart[0]))
         bs.seek(0x40, NOESEEK_REL)
         meshName = bs.readBytes(64).decode("ASCII").rstrip("\0")
         offsetInfo_Array.append([meshFaceSectionCount[0], meshFaceHeaderOff[0] + baseOff, vertCount[0], vertStart[0] + baseOff, normalStart[0] + baseOff, vertColourStart[0] + baseOff, uvStart[0] + baseOff, weightStart[0] + baseOff, boneIdStart[0] + baseOff, faceStart, meshName])
      for a in range(0, meshCount[0]):
         faceInfo_Array = []
         bs.seek(offsetInfo_Array[a][1], NOESEEK_ABS)
         for b in range(0, offsetInfo_Array[a][0]):
            bs.seek(0x14, NOESEEK_REL)
            matNumber1 = bs.read("i")
            bs.seek(0x8, NOESEEK_REL)
            fCount1 = bs.read("i")
            fOffset1 = bs.read("i")
            num4 = bs.read("i")
            fType = bs.read("i")
            num1 = bs.read("i")
            fCount2 = bs.read("i")
            fOffset2 = bs.read("i")
            bs.seek(0x20, NOESEEK_REL)
            faceInfo_Array.append([fCount1[0], fOffset1[0] + baseOff, num4[0], fType[0], matNumber1[0], fCount2[0], fOffset2[0] + baseOff])
         if boneTableOff1_Array[0] != 0:
            bs.seek(offsetInfo_Array[a][8], NOESEEK_ABS)
            boneIndexBuffer = 0
            for b in range(offsetInfo_Array[a][2]):
               bi1, bi2, bi3, bi4 = bs.read("4f")
               if bi1 == 255:
                  bi1 = 0
               if bi2 == 255:
                  bi2 = 0
               if bi3 == 255:
                  bi3 = 0
               if bi4 == 255:
                  bi4 = 0
               if offsetInfo_Array[a][8] == baseOff:
                  bi1 = 3
                  bi2 = 0
                  bi3 = 0
                  bi4 = 0
               if b == 0:
                  boneIndexBuffer = struct.pack("i", int(int(bi1)/3.0))
               else:
                  boneIndexBuffer = boneIndexBuffer + struct.pack("i", int(int(bi1)/3.0))
               boneIndexBuffer = boneIndexBuffer + struct.pack("i", int(int(bi2)/3.0))
               boneIndexBuffer = boneIndexBuffer + struct.pack("i", int(int(bi3)/3.0))
               boneIndexBuffer = boneIndexBuffer + struct.pack("i", int(int(bi4)/3.0))
            boneIndexMap = []
            biFix = 0
            if i > 1:
               biFix = biFix + boneSectionCount[i-1]
            for b in range(0, offsetInfo_Array[a][0]):
               bs.seek(faceInfo_Array[b][1], NOESEEK_ABS)
               bim = []
               for c in range(0, faceInfo_Array[b][0]):
                  bim2 = bs.read("h")
                  bim.append(bim2[0]+biFix)
               if offsetInfo_Array[a][8] == baseOff:
                  boneIndexMap.append([0, boneName_Array.index("kl_kosi_etc_wj")])
               else:
                  boneIndexMap.append(bim)
         rapi.rpgSetName(offsetInfo_Array[a][10])
         bs.seek(offsetInfo_Array[a][3], NOESEEK_ABS)
         vertBuff = bs.readBytes(offsetInfo_Array[a][2] * 0xc)
         bs.seek(offsetInfo_Array[a][4], NOESEEK_ABS)
         normalBuff = bs.readBytes(offsetInfo_Array[a][2] * 0xc)
         bs.seek(offsetInfo_Array[a][5], NOESEEK_ABS)
         colourBuff = bs.readBytes(offsetInfo_Array[a][2] * 0x10)
         bs.seek(offsetInfo_Array[a][6], NOESEEK_ABS)
         uvBuff = bs.readBytes(offsetInfo_Array[a][2] * 0x8)
         if boneTableOff1_Array[0] != 0:
            bs.seek(offsetInfo_Array[a][7], NOESEEK_ABS)
            weightBuff = bs.readBytes(offsetInfo_Array[a][2] * 0x10)
            boneBuff = boneIndexBuffer
         if offsetInfo_Array[a][8] == baseOff:
            for b in range(0, offsetInfo_Array[a][2]):
               if b == 0:
                  weightBuff = struct.pack("f", 1)
               else:
                  weightBuff = weightBuff + struct.pack("f", 1)
               weightBuff = weightBuff + struct.pack("f", 0)
               weightBuff = weightBuff + struct.pack("f", 0)
               weightBuff = weightBuff + struct.pack("f", 0)
         rapi.rpgBindPositionBufferOfs(vertBuff, noesis.RPGEODATA_FLOAT, 12, 0)
         rapi.rpgBindNormalBufferOfs(normalBuff, noesis.RPGEODATA_FLOAT, 12, 0)
         #rapi.rpgBindColorBufferOfs(colourBuff, noesis.RPGEODATA_FLOAT, 16, 0, 4)
         rapi.rpgBindUV1BufferOfs(uvBuff, noesis.RPGEODATA_FLOAT, 8, 0)
         if boneTableOff1_Array[0]:
            rapi.rpgBindBoneWeightBufferOfs(weightBuff, noesis.RPGEODATA_FLOAT, 16, 0, 4)
            rapi.rpgBindBoneIndexBufferOfs(boneBuff, noesis.RPGEODATA_INT, 16, 0, 4)
         for b in range(0, offsetInfo_Array[a][0]):
            bs.seek(faceInfo_Array[b][6], NOESEEK_ABS)
            uvScale = uvScales[faceInfo_Array[b][4]]
            rapi.rpgSetUVScaleBias(NoeVec3 ((uvScale[0], uvScale[1], uvScale[2])), NoeVec3 ((1.0, 1.0, 1.0)))
            if boneTableOff1_Array[0] != 0:
               rapi.rpgSetBoneMap(boneIndexMap[b])
            faceBuff = bs.readBytes(faceInfo_Array[b][5] * 2)
            rapi.rpgSetMaterial(materialNames[faceInfo_Array[b][4]])
            rapi.rpgCommitTriangles(faceBuff, noesis.RPGEODATA_USHORT, faceInfo_Array[b][5], noesis.RPGEO_TRIANGLE_STRIP, 1)

def load_binTex(binTex, texList):
   bs = NoeBitStream(binTex)
   idString = bs.read("i")
   texCount = bs.read("i")
   unk1 = bs.read("i")
   texOffList = []
   for i in range(0, texCount[0]):
      tOL = bs.read("i")
      texOffList.append(tOL[0])
   for i in range(0, texCount[0]):
      bs.seek(texOffList[i], NOESEEK_ABS)
      TXP = bs.read("i")
      txpMips = bs.read("i")
      unk2 = bs.read("i")
      texOff = bs.read("i")
      bs.seek(texOffList[i] + texOff[0], NOESEEK_ABS)
      txpHeader = bs.read("i"*6)
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
      name = tex_DB[texNameId_Array[i]]
      tex1 = NoeTexture(name, int(txpHeader[1]), int(txpHeader[2]), txpData, texFmt)
      texList.append(tex1)
   return 1

def load_binTexDB(binTexDB):
   bs = NoeBitStream(binTexDB)
   texCount = bs.read("i")
   texNameTableOff = bs.read("i")
   bs.seek(texNameTableOff[0], NOESEEK_ABS)
   currentOff = bs.tell()
   for i in range(0, texCount[0]):
      bs.seek(currentOff, NOESEEK_ABS)
      texNameID = bs.read("i")
      texNameOff = bs.read("i")
      currentOff = bs.tell()
      bs.seek(texNameOff[0], NOESEEK_ABS)
      texName = bs.readString()
      tex_DB[texNameID[0]] = texName

def load_binBone(binBone):
   bs = NoeBitStream(binBone)
   idString = bs.read("i")
   sectionCount = bs.read("i")
   skeletonsOff = bs.read("i")
   unk1 = bs.read("i")
   skeletonInfo = []
   character = []
   bs.seek(skeletonsOff[0], NOESEEK_ABS)
   for i in range(0, sectionCount[0]):
      sI = bs.read("i")
      skeletonInfo.append(sI[0])
   for i in range(0, sectionCount[0]):
      character.append(bs.readString())
   characterName = baseName[:-6]
   if characterName.upper() in character:
      bs.seek(skeletonInfo[character.index(characterName.upper())], NOESEEK_ABS)
   else:
      bs.seek(skeletonInfo[0], NOESEEK_ABS)
   unk2 = bs.read("i")
   skelCount1 = bs.read("i")
   skelMatrixOff = bs.read("i")
   unk3 = bs.read("i")
   skelCount2 = bs.read("i")
   skelNameOff1 = bs.read("i")
   skelCount3 = bs.read("i")
   skelNameOff2 = bs.read("i")
   skelParents = bs.read("i")
   boneMatrix_Array = []
   bs.seek(skelMatrixOff[0], NOESEEK_ABS)
   for i in range(0, skelCount1[0]):
      m01, m02, m03 = bs.read("3f")
      boneMatrix_Array.append((m01, m02, m03))
   boneNames1_Array = []
   bs.seek(skelNameOff1[0], NOESEEK_ABS)
   current = bs.tell()
   for i in range(0, skelCount2[0]):
      bs.seek(current, NOESEEK_ABS)
      boneNameOff = bs.read("i")
      current = bs.tell()
      bs.seek(boneNameOff[0], NOESEEK_ABS)
      boneNames1_Array.append(bs.readString())
   boneNames2_Array = []
   bs.seek(skelNameOff2[0], NOESEEK_ABS)
   current = bs.tell()
   for i in range(0, skelCount3[0]):
      bs.seek(current, NOESEEK_ABS)
      boneNameOff = bs.read("i")
      current = bs.tell()
      bs.seek(boneNameOff[0], NOESEEK_ABS)
      boneNames2_Array.append(bs.readString())
   boneParent_Array = []
   bs.seek(skelParents[0], NOESEEK_ABS)
   for i in range(0, skelCount3[0]):
      bpa = bs.read("h")
      boneParent_Array.append(bpa[0])
   bones = []
   for i in range(0, skelCount3[0]):
      if boneNames2_Array[i] in boneNames1_Array:
         index = boneNames1_Array.index(boneNames2_Array[i])
         pos = NoeVec3(boneMatrix_Array[index+2])
      else:
         pos = NoeVec3((0, 0, 0))
      boneMtx = NoeMat43()
      boneMtx[3] = pos
      bones.append(boneMtx)
   boneData_Array.append(boneNames2_Array)
   boneData_Array.append(boneParent_Array)
   boneData_Array.append(bones)

def texBinLoadRGBA(data, texList):
   bs = NoeBitStream(data)
   idString = bs.read("i")
   texCount = bs.read("i")
   unk1 = bs.read("i")
   texOffList = []
   for i in range(0, texCount[0]):
      tOL = bs.read("i")
      texOffList.append(tOL[0])
   for i in range(0, texCount[0]):
      bs.seek(texOffList[i], NOESEEK_ABS)
      TXP = bs.read("i")
      txpMips = bs.read("i")
      unk2 = bs.read("i")
      texOff = bs.read("i")
      bs.seek(texOffList[i] + texOff[0], NOESEEK_ABS)
      txpHeader = bs.read("i"*6)
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
      tex1 = NoeTexture(name + "_" + str(i), int(txpHeader[1]), int(txpHeader[2]), txpData, texFmt)
      texList.append(tex1)
   return 1
