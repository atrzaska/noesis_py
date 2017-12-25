import glob
from os.path import dirname, basename, isfile
from noesis import plugins
from importlib import import_module
from NoesisViewer import NoesisViewer
import rapi
import os
import sys

class NoesisApplication:
    def __init__(self):
        self.models = []

    def run(self):
        for plugin in self.plugins():
            plugin.registerNoesisTypes()

        if (len(sys.argv) == 1):
            print("Please provide a model file")
            return

        files = sys.argv[1:len(sys.argv)]

        for file in files:
            self.loadFile(file)

        NoesisViewer(rapi).call()


    def loadFile(self, file):
        filename, file_extension = os.path.splitext(file)

        plugin = [x for x in plugins if x.format == file_extension]

        if plugin:
            with open(file, "rb") as f:
                rapi.setLastCheckedName(file)
                rapi.getLastCheckedName()
                plugin[0].loadModel(f.read(), self.models)
        else:
            print("File format not supported")

    def plugins(self):
        files = glob.glob("lib/plugins/fmt_*.py")
        plugins = [ basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]
        plugins = map(lambda x: "plugins." + x, plugins)
        return map(import_module, plugins)

if __name__ == "__main__":
    NoesisApplication().run()
