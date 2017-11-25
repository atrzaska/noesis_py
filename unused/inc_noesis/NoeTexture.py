class NoeTexture:
    def __init__(self, name, width, height, data, format):
        self.name = name
        self.width = width
        self.height = height
        self.data = data
        self.format = format

    def __repr__(self):
        return "<NoeTexture name: {self.name} width: {self.width} height: {self.height}>".format(**locals())
