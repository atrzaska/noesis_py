import struct

class NoeVec4:
    @classmethod
    def fromBytes(self, data):
        x = struct.unpack('f', data[0:4])
        y = struct.unpack('f', data[4:8])
        z = struct.unpack('f', data[8:12])
        w = struct.unpack('f', data[12:16])
        return NoeVec4(x, y, z, w)

    def __init__(self, x = 0, y = 0, z = 0, w = 0):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0

    def __repr__(self):
        return "<x: {self.x}, y: {self.y}, z: {self.z}, w: {self.w}>".format(**locals())
