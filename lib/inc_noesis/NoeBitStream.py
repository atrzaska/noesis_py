import struct

SIZES = {
    'c': 1,
    'b': 1,
    'B': 1,
    'h': 2,
    'H': 2,
    'i': 4,
    'I': 4,
    'l': 4,
    'L': 4,
    'q': 8,
    'Q': 8,
    'f': 4,
    'd': 8
}

class NoeBitStream:
    def __init__(self, data):
        self.data = data

    def readBytes(self, size):
        return self.data.read(size)

    def read(self, fmt):
        size = int(fmt[0])
        type = fmt[1:]
        results = []

        for i in range(size):
            results.append(self.readAndUnpack(type))

        return results

    def readByte(self):
        return self.readInt8()

    def readUByte(self):
        return self.readUInt8()

    def readShort(self):
        return self.readInt16()

    def readUShort(self):
        return self.readUInt16()

    def readInt(self):
        return self.readInt32()

    def readUInt(self):
        return self.readUInt32()

    def readLong(self):
        return self.readInt32()

    def readULong(self):
        return self.readUInt32()

    def readLongLong(self):
        return self.readInt64()

    def readULongLong(self):
        return self.readUInt64()

    def readFloat(self):
        return self.readAndUnpack('f')

    def readDouble(self):
        return self.readAndUnpack('d')

    def readInt8(self):
        return self.readAndUnpack('b')

    def readUInt8(self):
        return self.readAndUnpack('B')

    def readInt16(self):
        return self.readAndUnpack('h')

    def readUInt16(self):
        return self.readAndUnpack('H')

    def readInt32(self):
        return self.readAndUnpack('i')

    def readUInt32(self):
        return self.readAndUnpack('I')

    def readInt64(self):
        return self.readAndUnpack('q')

    def readUInt64(self):
        return self.readAndUnpack('Q')

    def tell(self):
        return self.data.tell()

    def seek(self, offset, from_what = 0):
        self.data.seek(offset, from_what)

    def getSize(self):
        currentPositon = self.tell()
        self.data.seek(0,2)
        size = self.data.tell()
        self.data.seek(currentPositon)
        return size

    def readAndUnpack(self, type):
        return struct.unpack(type, self.data.read(SIZES[type]))[0]
