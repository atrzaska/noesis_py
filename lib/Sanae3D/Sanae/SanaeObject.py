from inc_noesis import NoeBitStream

class SanaeObject(object):
    def __init__(self, data):
        self.inFile = NoeBitStream(data)
        self.matList = []
        self.texList = []

    def read_string(self, size):
        return self.inFile.readBytes(size)
