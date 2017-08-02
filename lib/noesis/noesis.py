from Handler import Handler

class Noesis:
    def __init__(self):
        self.plugins = []
        self.models = []
        self.modules = []

    def addOption(self, handle, option, description, flags):
        # TODO: implement me
        pass

    def allocBytes(self, size):
        return bytearray(size)

    def doException(self, error):
        raise ValueError(error)

    def freeModule(self, module):
        # TODO: rek0ve module from modules
        pass

    def getCharSplineSet(self):
        # TODO: implement me
        pass

    def getFormatExtensionFlags(self):
        # TODO: implement me
        pass

    def getMFFP(self, uint):
        # TODO: implement me
        pass

    def getScenesPath(self):
        # TODO: implement me
        pass

    def getSelectedDirectory(self):
        # TODO: implement me
        pass

    def getSelectedFile(self):
        # TODO: implement me
        pass

    def getWindowHandle(self):
        # TODO: implement me
        pass

    def instantiateModule(self):
        module = NoeModule()
        self.modules.append(module)
        return module

    def isPreviewModuleRAPIValid(self):
        # TODO: implement me
        pass

    def loadImageRGBA(self):
        # TODO: implement me
        pass

    def logPopup(self):
        # TODO: implement me
        pass

    def messagePrompt(self):
        # TODO: implement me
        pass

    def openAndRemoveTempFile(self):
        # TODO: implement me
        pass

    def openFile(self):
        # TODO: implement me
        pass

    def optGetArg(self):
        # TODO: implement me
        pass

    def optWasInvoked(self):
        # TODO: implement me
        return true

    # TODO: fileType can be semicolon separated '.obj;.obc'
    def register(self, name, fileType):
        handler = Handler(name, fileType)
        self.plugins.append(handler)
        return handler

    def registerCleanupFunction(self):
        # TODO: implement me
        pass

    def registerTool(self):
        # TODO: implement me
        pass

    def setHandlerExtractArc(self, handle, grpExtractArc):
        handle.grpExtractArc = grpExtractArc

    def setHandlerLoadModel(self, handle, noepyLoadModel):
        handle.noepyLoadModel = noepyLoadModel

    def setHandlerLoadRGBA(self, handle, txdLoadRGBA):
        handle.txdLoadRGBA = txdLoadRGBA

    def setHandlerTypeCheck(self, handle, noepyCheckType):
        handle.noepyCheckType = noepyCheckType

    def setHandlerWriteModel(self, handle, noepyWriteModel):
        handle.noepyWriteModel = noepyWriteModel

    def setHandlerWriteRGBA(self, handle, walWriteRGBA):
        handle.walWriteRGBA = walWriteRGBA

    def setHandlerWriteAnim(self, handle, noepyWriteAnim):
        handle.noepyWriteAnim = noepyWriteAnim

    def setModuleRAPI(self):
        # TODO: implement me
        pass

    def setPreviewModuleRAPI(self):
        # TODO: implement me
        pass

    def setToolFlags(self):
        # TODO: implement me
        pass

    def setToolVisibleCallback(self):
        # TODO: implement me
        pass

    def userPrompt(self):
        # TODO: implement me
        pass
