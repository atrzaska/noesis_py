import glob
from os.path import dirname, basename, isfile
from noesis import noesis
from importlib import import_module
from NoesisViewer import NoesisViewer
import rapi
import os
import sys

class NoesisApplication:
    def run(self):
        for plugin in self.plugins():
            plugin.registerNoesisTypes()

        if (len(sys.argv) == 1):
            print("Please provide a model file")
            return

        file = sys.argv[1]

        filename, file_extension = os.path.splitext(file)

        plugin = [x for x in noesis.plugins if x.format == file_extension]
        models = []

        if plugin:
            with open(file, "rb") as f:
                rapi.setLastCheckedName(file)
                plugin[0].noepyLoadModel(f, models)
            NoesisViewer(rapi.rpg).call()
        else:
            print("File format not supported")

    def plugins(self):
        files = glob.glob("lib/plugins/fmt_*.py")
        plugins = [ basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]
        plugins = map(lambda x: "plugins." + x, plugins)
        return map(import_module, plugins)

if __name__ == "__main__":
    NoesisApplication().run()
