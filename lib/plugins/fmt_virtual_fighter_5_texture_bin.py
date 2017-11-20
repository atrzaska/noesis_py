from inc_noesis import *
import noesis
import rapi

texList = []

def registerNoesisTypes():
   handle = noesis.register("Virtual Fighter 5 Textures", ".bin")
   noesis.setHandlerTypeCheck(handle, noepyCheckType)
   noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
   noesis.logPopup()
   return 1

def noepyCheckType(data):
   bs = NoeBitStream(data)
   if bs.readInt() != 0x3505854 :
      return 0
   return 1

def noepyLoadRGBA(data, texList):
   bs = NoeBitStream(data)
   bs.seek(0, NOESEEK_ABS)
   Tex = bs.readInt()
   TexCount = bs.readInt()
   Unk01 = bs.readInt()
   TexOffList = bs.read("i" * TexCount)

   for i in range(0, TexCount):
      TexName = 'test'
      bs.seek(TexOffList[i], NOESEEK_ABS)
      print(bs.tell())
      TXP = bs.readInt()
      TXPMIPS = bs.readInt()
      TXPUNK = bs.readInt()
      TexOff = bs.readInt()
      bs.seek(TexOffList[i] + TexOff, NOESEEK_ABS)
      TxpHeader = bs.read("i"*6)
      print(bs.tell())
      Txpdata = bs.readBytes(TxpHeader[5])
      print(TxpHeader)
      print(TxpHeader[3])
      texFmt = 0

      #DXT1
      if TxpHeader[3] == 6:
         texFmt = noesis.NOESISTEX_DXT1

      #DXT3
      if TxpHeader[3] == 7:
         texFmt = noesis.NOESISTEX_DXT3

      #DXT5
      if TxpHeader[3] == 9:
         texFmt = noesis.NOESISTEX_DXT5

      #ATI2N
      if TxpHeader[3] == 11:
         Txpdata = rapi.imageDecodeDXT(Txpdata, int(TxpHeader[1]), int(TxpHeader[2]), noesis.FOURCC_ATI2)
         texFmt = noesis.NOESISTEX_RGBA32

      tex1 = NoeTexture(TexName, int(TxpHeader[1]), int(TxpHeader[2]), Txpdata, texFmt)
      texList.append(tex1)

   return 1
