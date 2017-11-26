class Handler:
    def __init__(self, name, format):
        self.name = name
        self.format = format
        self.noepyCheckType = None
        self.noepyLoadModel = None
        self.grpExtractArc = None
        self.txdLoadRGBA = None
        self.noepyWriteModel = None
        self.walWriteRGBA = None
        self.noepyWriteAnim = None
        self.options = []

    def addOption(self, option, description, flags):
        self.options.append({
            "option": option,
            "description": description,
            "flags": flags
        })

    def __repr__(self):
        return self.name
