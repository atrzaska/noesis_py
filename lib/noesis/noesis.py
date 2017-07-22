from Handler import Handler

class Noesis:
    def __init__(self):
        self.plugins = []
        self.mdlList = []

    def register(self, name, fileType):
        handler = Handler(name, fileType)
        self.plugins.append(handler)
        return handler

    def setHandlerTypeCheck(self, handle, noepyCheckType):
        handle.noepyCheckType = noepyCheckType

    def setHandlerLoadModel(self, handle, noepyLoadModel):
        handle.noepyLoadModel = noepyLoadModel

    def setHandlerLoadRGBA(self, handle, txdLoadRGBA):
        handle.txdLoadRGBA = txdLoadRGBA

    def setHandlerExtractArc(self, handle, grpExtractArc):
        handle.grpExtractArc = grpExtractArc

    def setHandlerWriteRGBA(self, handle, walWriteRGBA):
        handle.walWriteRGBA = walWriteRGBA

    def allocType(self, type, data):
        # TODO: implement me
        pass

    def noepyLoadModelRPG(self):
        # TODO: implement me
        pass

    def logPopup(self):
        # TODO: implement me
        pass

    def vec3Validate(self, vec3):
        # TODO: implement me
        pass

    def vec4Validate(self, vec4):
        # TODO: implement me
        pass

    def addOption(self, handle, option, description, flags):
        # TODO: implement me
        pass
