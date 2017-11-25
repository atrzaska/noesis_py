class NoeMaterial:
    def __init__(self, name, texture):
        self.name = name
        self.texture = texture
        self.color = None

    def setDiffuseColor(self, color):
        self.color = color

    def setTexture(self, texture):
        self.texture = texture

    def __repr__(self):
        return "<NoeMaterial name: {self.name} texture: {self.texture}>".format(**locals())
