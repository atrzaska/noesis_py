from io import BytesIO
import re
import struct
import logger

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
        logger.logNotImplementedMethod('bsReadBits', locals())

    def bsReadBool(self):
        logger.logNotImplementedMethod('bsReadBool', locals())

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
        logger.logNotImplementedMethod('bsReadLine', locals())

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
        logger.logNotImplementedMethod('bsWriteBits', locals())

    def bsWriteBool(self, val):
        logger.logNotImplementedMethod('bsWriteBool', locals())

    def bsWriteByte(self, val):
        logger.logNotImplementedMethod('bsWriteByte', locals())

    def bsWriteBytes(self, data):
        logger.logNotImplementedMethod('bsWriteBytes', locals())

    def bsWriteDouble(self, val):
        logger.logNotImplementedMethod('bsWriteDouble', locals())

    def bsWriteFloat(self, val):
        logger.logNotImplementedMethod('bsWriteFloat', locals())

    def bsWriteInt(self, val):
        logger.logNotImplementedMethod('bsWriteInt', locals())

    def bsWriteInt64(self, val):
        logger.logNotImplementedMethod('bsWriteInt64', locals())

    def bsWriteShort(self, val):
        logger.logNotImplementedMethod('bsWriteShort', locals())

    def bsWriteString(self, str, writeTerminator):
        logger.logNotImplementedMethod('bsWriteString', locals())

    def bsWriteUByte(self, val):
        logger.logNotImplementedMethod('bsWriteUByte', locals())

    def bsWriteUInt(self, val):
        logger.logNotImplementedMethod('bsWriteUInt', locals())

    def bsWriteUInt64(self, val):
        logger.logNotImplementedMethod('bsWriteUInt64', locals())

    def bsWriteUShort(self, val):
        logger.logNotImplementedMethod('bsWriteUShort', locals())

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
