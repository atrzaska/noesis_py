class Handler:
    def __init__(self, name, format):
        self.name = name
        self.format = format
        self.checkType = None
        self.loadModel = None
        self.extractArc = None
        self.loadRGBA = None
        self.writeModel = None
        self.writeRGBA = None
        self.writeAnim = None
        self.options = []

    def addOption(self, option, description, flags):
        self.options.append({
            "option": option,
            "description": description,
            "flags": flags
        })

    def __repr__(self):
        return self.name
