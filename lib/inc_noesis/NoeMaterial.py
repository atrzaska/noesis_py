class NoeMaterial:
    def __init__(self, name, unk1):
        self.name = name
        self.unk1 = unk1
        self.texture = None

    def setDiffuseColor(self, color):
        self.color = color

    def setTexture(self, name):
        self.texture = name

    def __repr__(self):
        return "<name: {self.name}>".format(**locals())
