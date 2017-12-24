import math
import io
import re
import struct
from util import logNotImplementedMethod

NOE_BIGENDIAN = 1
NOE_LITTLEENDIAN = 0

class AllocType:
    def __init__(self, name, data):
        self.name = name
        self.data = io.BytesIO(data or '')
        self.readData = [0] * len(data or '')
        self.bsSetEndian(NOE_LITTLEENDIAN)
        self.flags = 0

    def bsGetBuffer(self):
        return self.data

    def bsGetBufferSlice(self, start, end):
        if start is not None and end is None:
            return self.data[start:]
        elif start is None and end is not None:
            return self.data[:end]
        elif start is not None and end is not None:
            return self.data[start:end]
        else
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
        return self.readValue('?')

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
        output = ''

        while(True):
            b = self.read(1)

            if (b == '\n'):
                return output

            output += b

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
        self.writeValue('?', val)

    def bsWriteByte(self, val):
        self.writeValue('b', val)

    def bsWriteBytes(self, data):
        self.data.write(data)

    def bsWriteDouble(self, val):
        self.writeValue('d', val)

    def bsWriteFloat(self, val):
        self.writeValue('f', val)

    def bsWriteInt(self, val):
        self.writeValue('i', val)

    def bsWriteInt64(self, val):
        self.writeValue('q', val)

    def bsWriteShort(self, val):
        self.writeValue('h', val)

    def bsWriteString(self, str, writeTerminator):
        self.data.write(str)
        if writeTerminator:
            self.date.write('\0')

    def bsWriteUByte(self, val):
        self.writeValue('B', val)

    def bsWriteUInt(self, val):
        self.writeValue('I', val)

    def bsWriteUInt64(self, val):
        self.writeValue('Q', val)

    def bsWriteUShort(self, val):
        self.writeValue('H', val)

    # private

    def writeValue(self, fmt, val):
        self.data.write(struct.pack(fmt, val))

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
