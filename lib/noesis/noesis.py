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

    def noepyLoadModelRPG(self):
        # TODO: implement me
        pass
