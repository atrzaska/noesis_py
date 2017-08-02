from inc_noesis import *

#registerNoesisTypes is called by Noesis to allow the script to register formats.
#Do not implement this function in script files unless you want them to be dedicated format modules!
def registerNoesisTypes():
    handle = noesis.register("FAT12 Disk Image", ".fat12")
    noesis.setHandlerExtractArc(handle, fat12ExtractArc)
    noesis.addOption(handle, "-fatnousefc", "use 2 instead of provided fat count.", 0)
    noesis.addOption(handle, "-fatwritee5", "write entries beginning with 0xE5.", 0)
    noesis.addOption(handle, "-fatmaskfs", "24-bit mask for filesize.", 0)
    
    handle = noesis.register("FAT16 Disk Image", ".fat16")
    noesis.setHandlerExtractArc(handle, fat16ExtractArc)
    
    return 1
    
FAT_ATTRIB_READONLY = (1 << 0)
FAT_ATTRIB_HIDDN = (1 << 1)
FAT_ATTRIB_SYSTEM = (1 << 2)
FAT_ATTRIB_VOLUMELABEL = (1 << 3)
FAT_ATTRIB_DIRECTORY = (1 << 4)
FAT_ATTRIB_ARCHIVE = (1 << 5)
    
FAT_CLUSTER_ROOT = 0
FAT_CLUSTER_FIRST = 2

class FATEntry:
    def __init__(self, bs, parentDirectory):
        filenameBytes = bs.readBytes(8)
        if filenameBytes[0] == 0xE5:
            if noesis.optWasInvoked("-fatwritee5"):
                filenameBytes = bytearray(filenameBytes)
                filenameBytes[0] = bytes("!", "ASCII")[0]
                self.filename = noeAsciiFromBytes(filenameBytes).rstrip(" ")
            else:
                self.filename = ""
        elif filenameBytes[0] != 0:
            self.filename = noeAsciiFromBytes(filenameBytes).rstrip(" ")
        else:
            self.filename = None
        fileExt = noeAsciiFromBytes(bs.readBytes(3)).rstrip(" ")

        self.attributes = bs.readUByte()
        
        if self.isValid() and not (self.attributes & FAT_ATTRIB_DIRECTORY) and len(fileExt) > 0:
            self.filename += "." + fileExt
        
        bs.readUShort() #reserved
        self.createTime = bs.readUShort()
        self.createDate = bs.readUShort()
        self.accessDate = bs.readUShort()
        bs.readUShort() #reserved
        self.writeTime = bs.readUShort()
        self.writeDate = bs.readUShort()
        self.firstCluster = bs.readUShort()
        fileSizeMask = 0xFFFFFF if noesis.optWasInvoked("-fatmaskfs") else 0xFFFFFFFF
        self.fileSize = bs.readUInt() & fileSizeMask
        self.parentDirectory = parentDirectory
        
    def getFullPath(self):
        basePath = self.parentDirectory.getFullPath() + "\\" if self.parentDirectory else ""
        return basePath + self.filename
        
    def isValid(self):
        return self.filename and len(self.filename) > 0 and self.filename[0] != "."
        
    def isTerminator(self):
        return self.filename is None

class FATImage:
    def __init__(self, bs, imageSize, fatBits):
        self.bs = bs
        self.imageSize = imageSize
        self.fatBits = fatBits
        self.entries = []
        
    def parseFAT(self):
        bs = self.bs
        bs.seek(11, NOESEEK_ABS)
        self.sectorSize = bs.readUShort()
        self.sectorsPerCluster = max(bs.readUByte(), 1)
        self.reservedSectorCount = max(bs.readUShort(), 1)
        self.fatCount = bs.readUByte()
        self.rootDirEntryCount = bs.readUShort()
        self.sectorCount = bs.readUShort()
            
        bs.readUByte() #unused
        self.sectorsPerFat = bs.readUShort()
        self.sectorsPerTrack = bs.readUShort()
        self.headCount = bs.readUShort()
        bs.readUInt() #unused
        largeSectorCount = bs.readUInt()
        if self.sectorCount == 0:
            self.sectorCount = largeSectorCount
        
        if self.sectorSize == 0 or self.sectorSize > 8192 or self.fatCount == 0 or self.sectorCount == 0:# or self.sectorSize * self.sectorCount > self.imageSize:
            return -1

        if noesis.optWasInvoked("-fatnousefc"):
            self.fatCount = 2
            
        self.clusterSize = self.sectorsPerCluster * self.sectorSize
            
        bs.readUShort() #unused
        self.bootSig = bs.readUByte()
        if self.bootSig == 0x29:
            self.volumeId = bs.readUInt()
            self.volumeLabel = bs.readBytes(11)
            self.fsType = bs.readBytes(8)

        self.reservedSectorsSize = self.reservedSectorCount * self.sectorSize
        
        self.fatOffset = self.reservedSectorsSize
        self.fatSize = self.sectorsPerFat * self.sectorSize
        
        self.rootDirOffset = self.fatOffset + self.fatSize * self.fatCount
        rootDirSize = 32 * self.rootDirEntryCount
        if (rootDirSize % self.sectorSize) != 0:
            rootDirSize += self.sectorSize - (rootDirSize % self.sectorSize)

        self.dataOffset = self.rootDirOffset + rootDirSize
        
        return 0
        
    def clusterIsValid(self, clusterIndex):
        return clusterIndex >= 0 and clusterIndex < len(self.fatEntries)
        
    def getClusterDataOffset(self, clusterIndex):
        if clusterIndex == FAT_CLUSTER_ROOT:
            return self.rootDirOffset
        else:
            return self.dataOffset + (clusterIndex - FAT_CLUSTER_FIRST) * self.clusterSize

    def getNextCluster(self, clusterIndex):
        return self.fatEntries[clusterIndex]
            
    def recursivelyReadEntries(self, clusterIndex, parentDirectory):
        self.bs.seek(self.getClusterDataOffset(clusterIndex), NOESEEK_ABS)
        entryCount = self.rootDirEntryCount if clusterIndex == FAT_CLUSTER_ROOT else self.sectorSize // 32
        newDirectories = []
        while True:
            for entryIndex in range(0, entryCount):
                entry = FATEntry(self.bs, parentDirectory)
                if entry.isTerminator():
                    break
                elif not entry.isValid():
                    continue
                if entry.attributes & FAT_ATTRIB_DIRECTORY:
                    newDirectories.append(entry)
                self.entries.append(entry)
                
            if clusterIndex == FAT_CLUSTER_ROOT:
                break
            else:
                if not self.clusterIsValid(clusterIndex):
                    break
                clusterIndex = self.getNextCluster(clusterIndex)
        for newDirectory in newDirectories:
            self.recursivelyReadEntries(newDirectory.firstCluster, newDirectory)
            
    def readEntries(self):
        bs = self.bs
        
        print("Reading FAT image. Sector size:", self.sectorSize, "- Cluster size:", self.clusterSize)
        
        print("Reading FAT of size", self.fatSize, "from", self.fatOffset)
        #seek over to FAT sector
        bs.seek(self.fatOffset, NOESEEK_ABS)
        fatData = bs.readBytes(self.fatSize)
        fatBs = NoeBitStream(fatData)
        self.fatEntries = []
        while not fatBs.checkEOF():
            fatValue = fatBs.readBits(self.fatBits)
            #print("FAT:", len(self.fatEntries), fatValue)
            self.fatEntries.append(fatValue)

        print("Reading root directory from", self.rootDirOffset)            
        #seek over to root directory
        self.recursivelyReadEntries(FAT_CLUSTER_ROOT, None)

        for entry in self.entries:
            if (entry.attributes & FAT_ATTRIB_DIRECTORY):
                continue
            entryName = entry.getFullPath()
            print("Writing", entryName)
            
            clusterIndex = entry.firstCluster
            remainingSize = entry.fileSize
            entryData = bytearray()
            while remainingSize > 0:
                bs.seek(self.getClusterDataOffset(clusterIndex), NOESEEK_ABS)
                readSize = min(remainingSize, self.clusterSize)
                entryData += bs.readBytes(readSize)
                remainingSize -= readSize
                if not self.clusterIsValid(clusterIndex):
                    break
                clusterIndex = self.getNextCluster(clusterIndex)
            if remainingSize > 0:
                print("Warning: Failed to read expected file size, bad cluster index on:", entryName, "-", entry.attributes)
                print(len(entryData), "vs", entry.fileSize, "with cluster size", self.clusterSize, "and index", clusterIndex)
            elif len(entryData) != entry.fileSize:
                print("Bad entry size on", entryName, "- probably tried to read off end of image:", len(entryData), "vs", entry.fileSize)
                
            rapi.exportArchiveFile(entryName, entryData)
            
    
def fatGenericExtractArc(fileName, fileLen, justChecking, fatBits):
    if fileLen < 40:
        return 0
    with open(fileName, "rb") as f:
        bs = NoeFileStream(f)
        fat = FATImage(bs, fileLen, fatBits)
        if fat.parseFAT() != 0:
            return 0

        if justChecking:
            return 1

        fat.readEntries()
        
    return 1
    
def fat12ExtractArc(fileName, fileLen, justChecking):
    return fatGenericExtractArc(fileName, fileLen, justChecking, 12)

def fat16ExtractArc(fileName, fileLen, justChecking):
    return fatGenericExtractArc(fileName, fileLen, justChecking, 16)
