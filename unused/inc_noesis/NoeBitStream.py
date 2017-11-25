import struct
import re
from StringIO import StringIO

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
        if type(data) is str:
            data = StringIO(data)
        self.data = data

    def readBytes(self, size):
        return self.data.read(size)

    def read(self, fmt):
        return self.readAndUnpack(fmt)

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
        return self.readAndUnpack('1f')[0]

    def readDouble(self):
        return self.readAndUnpack('1d')[0]

    def readInt8(self):
        return self.readAndUnpack('1b')[0]

    def readUInt8(self):
        return self.readAndUnpack('1B')[0]

    def readInt16(self):
        return self.readAndUnpack('1h')[0]

    def readUInt16(self):
        return self.readAndUnpack('1H')[0]

    def readInt32(self):
        return self.readAndUnpack('1i')[0]

    def readUInt32(self):
        return self.readAndUnpack('1I')[0]

    def readInt64(self):
        return self.readAndUnpack('1q')[0]

    def readUInt64(self):
        return self.readAndUnpack('1Q')[0]

    def readString(self):
        output = ''

        while(True):
            b = self.data.read(1)

            if (b == '\0'):
                return output

            output += b

    def tell(self):
        return self.data.tell()

    def seek(self, offset, from_what = 0):
        self.data.seek(offset, from_what)

    def getSize(self):
        currentPositon = self.tell()
        self.data.seek(0, 2)
        size = self.data.tell()
        self.data.seek(currentPositon)
        return size

    def readAndUnpack(self, fmt):
        matches = re.match("(\d+)?(\w)", fmt)
        length = int(matches.group(1) or "1")
        type = matches.group(2)

        if type == 'L':
            type = 'I'
        if type == 'l':
            type = 'i'

        typeSize = SIZES[type]
        readLength = typeSize * length
        fmt = "{length}{type}".format(**locals())

        return struct.unpack(fmt, self.data.read(readLength))
