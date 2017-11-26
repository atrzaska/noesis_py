from io import BytesIO
import re
import struct

NOE_BIGENDIAN = 1
NOE_LITTLEENDIAN = 0

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

class AllocType:
    def __init__(self, name, data):
        self.name = name
        self.data = BytesIO(data or '')
        self.endianess = NOE_LITTLEENDIAN
        self.flags = 0

    def bsGetBuffer(self):
        return self.data

    def bsGetBufferSlice(self, startOfs, endOfs):
        # TODO implement slice
        return self.data

    def bsGetFlags(self):
        return self.flags

    def bsGetOfs(self):
        return self.data.tell()

    def bsGetSize(self):
        currentPositon = self.data.tell()
        self.data.seek(0, 2)
        size = self.data.tell()
        self.data.seek(currentPositon)
        return size

    def bsReadBits(self, numBits):
        # TODO implement me
        pass

    def bsReadBool(self):
        # TODO implement me
        pass

    def bsReadByte(self):
        return self.readAndUnpack('1b')[0]

    def bsReadBytes(self, numBytes):
        return self.data.read(numBytes)

    def bsReadDouble(self):
        return self.readAndUnpack('1d')[0]

    def bsReadFloat(self):
        return self.readAndUnpack('1f')[0]

    def bsReadInt(self):
        return self.readAndUnpack('1i')[0]

    def bsReadInt64(self):
        return self.readAndUnpack('1q')[0]

    def bsReadLine(self):
        # TODO implement me
        pass

    def bsReadShort(self):
        return self.readAndUnpack('1h')[0]

    def bsReadString(self):
        output = ''

        while(True):
            b = self.data.read(1)

            if (b == '\0'):
                return output

            output += b

    def bsReadUByte(self):
        return self.readAndUnpack('1B')[0]

    def bsReadUInt(self):
        return self.readAndUnpack('1I')[0]

    def bsReadUInt64(self):
        return self.readAndUnpack('1Q')[0]

    def bsReadUShort(self):
        return self.readAndUnpack('1H')[0]

    def bsSetEndian(self, bigEndian):
        self.endianess = bigEndian

    def bsSetFlags(self, flags):
        self.flags = flags

    def bsSetOfs(self, ofs):
        self.data.seek(ofs)

    def bsWriteBits(self, val, numBits):
        # TODO implement me
        pass

    def bsWriteBool(self, val):
        # TODO implement me
        pass

    def bsWriteByte(self, val):
        # TODO implement me
        pass

    def bsWriteBytes(self, data):
        # TODO implement me
        pass

    def bsWriteDouble(self, val):
        # TODO implement me
        pass

    def bsWriteFloat(self, val):
        # TODO implement me
        pass

    def bsWriteInt(self, val):
        # TODO implement me
        pass

    def bsWriteInt64(self, val):
        # TODO implement me
        pass

    def bsWriteShort(self, val):
        # TODO implement me
        pass

    def bsWriteString(self, str, writeTerminator):
        # TODO implement me
        pass

    def bsWriteUByte(self, val):
        # TODO implement me
        pass

    def bsWriteUInt(self, val):
        # TODO implement me
        pass

    def bsWriteUInt64(self, val):
        # TODO implement me
        pass

    def bsWriteUShort(self, val):
        # TODO implement me
        pass

    # private

    def endianessSign(self):
        if (self.endianess == NOE_LITTLEENDIAN):
            return '<'
        else:
            return '>'

    def readAndUnpack(self, fmt):
        matches = re.match("(\d+)?(\w)", fmt)
        length = int(matches.group(1) or "1")
        endianessSign = self.endianessSign()

        type = matches.group(2)

        if type == 'L':
            type = 'I'
        if type == 'l':
            type = 'i'

        typeSize = SIZES[type]
        readLength = typeSize * length
        fmt = "{endianessSign}{length}{type}".format(**locals())

        return struct.unpack(fmt, self.data.read(readLength))
