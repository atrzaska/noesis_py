from io import BytesIO
import re
import struct
from util import logNotImplementedMethod

NOE_BIGENDIAN = 1
NOE_LITTLEENDIAN = 0

class AllocType:
    def __init__(self, name, data):
        self.name = name
        self.data = BytesIO(data or '')
        self.readData = [0] * len(data or '')
        self.bsSetEndian(NOE_LITTLEENDIAN)
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
        logNotImplementedMethod('bsReadBits', locals())

    def bsReadBool(self):
        logNotImplementedMethod('bsReadBool', locals())

    def bsReadByte(self):
        return self.readValue('b')

    def bsReadBytes(self, numBytes):
        return self.read(numBytes)

    def bsReadDouble(self):
        return self.readValue('d')

    def bsReadFloat(self):
        return self.readValue('f')

    def bsReadInt(self):
        return self.readValue('i')

    def bsReadInt64(self):
        return self.readValue('q')

    def bsReadLine(self):
        logNotImplementedMethod('bsReadLine', locals())

    def bsReadShort(self):
        return self.readValue('h')

    def bsReadString(self):
        output = ''

        while(True):
            b = self.read(1)

            if (b == '\0'):
                return output

            output += b

    def bsReadUByte(self):
        return self.readValue('B')

    def bsReadUInt(self):
        return self.readValue('I')

    def bsReadUInt64(self):
        return self.readValue('Q')

    def bsReadUShort(self):
        return self.readValue('H')

    def bsSetEndian(self, bigEndian):
        self.endian = "<" if bigEndian == NOE_LITTLEENDIAN else ">"

    def bsSetFlags(self, flags):
        self.flags = flags

    def bsSetOfs(self, ofs):
        self.data.seek(ofs)

    def bsWriteBits(self, val, numBits):
        logNotImplementedMethod('bsWriteBits', locals())

    def bsWriteBool(self, val):
        logNotImplementedMethod('bsWriteBool', locals())

    def bsWriteByte(self, val):
        logNotImplementedMethod('bsWriteByte', locals())

    def bsWriteBytes(self, data):
        logNotImplementedMethod('bsWriteBytes', locals())

    def bsWriteDouble(self, val):
        logNotImplementedMethod('bsWriteDouble', locals())

    def bsWriteFloat(self, val):
        logNotImplementedMethod('bsWriteFloat', locals())

    def bsWriteInt(self, val):
        logNotImplementedMethod('bsWriteInt', locals())

    def bsWriteInt64(self, val):
        logNotImplementedMethod('bsWriteInt64', locals())

    def bsWriteShort(self, val):
        logNotImplementedMethod('bsWriteShort', locals())

    def bsWriteString(self, str, writeTerminator):
        logNotImplementedMethod('bsWriteString', locals())

    def bsWriteUByte(self, val):
        logNotImplementedMethod('bsWriteUByte', locals())

    def bsWriteUInt(self, val):
        logNotImplementedMethod('bsWriteUInt', locals())

    def bsWriteUInt64(self, val):
        logNotImplementedMethod('bsWriteUInt64', locals())

    def bsWriteUShort(self, val):
        logNotImplementedMethod('bsWriteUShort', locals())

    # private

    def readValue(self, fmt):
        return self.bsReadAndUnpack(self.endian + fmt)[0]

    def bsReadAndUnpack(self, fmt):
        readLength = struct.calcsize(fmt)
        data = self.read(readLength)
        return struct.unpack(fmt, data)

    def read(self, length):
        if self.bsGetOfs() + length > self.bsGetSize():
            raise OverflowError('Buffer error: tried to read ' + str(length) +' bytes from buffer at offset ' + str(self.bsGetSize()))
        for i in range(length):
            self.readData[self.bsGetOfs() + i] += 1
        return self.data.read(length)
