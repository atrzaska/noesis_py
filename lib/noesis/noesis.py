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

    def setHandlerWriteModel(self, handle, noepyWriteModel):
        handle.noepyWriteModel = noepyWriteModel

    def setHandlerLoadRGBA(self, handle, txdLoadRGBA):
        handle.txdLoadRGBA = txdLoadRGBA

    def setHandlerWriteRGBA(self, handle, walWriteRGBA):
        handle.walWriteRGBA = walWriteRGBA

    def setHandlerWriteAnim(self, handle, noepyWriteAnim):
        handle.noepyWriteAnim = noepyWriteAnim

    def setHandlerExtractArc(self, handle, grpExtractArc):
        handle.grpExtractArc = grpExtractArc

    def allocType(self, type, data):
        # TODO: implement me
        pass

    def logPopup(self):
        # TODO: implement me
        pass

    def addOption(self, handle, option, description, flags):
        # TODO: implement me
        pass

    def getMFFP(uint):
        # TODO: implement me
        pass

    def getScenesPath(self):
        # TODO: implement me
        pass

    def optWasInvoked(self, option):
        # tODO: implement me
        return true
