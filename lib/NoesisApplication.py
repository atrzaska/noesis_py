import glob
import rapi
import os
import sys
from os.path import dirname, basename, isfile
from noesis import plugins
from importlib import import_module
from NoesisViewer import NoesisViewer

# Your own/third-party plugins (gitignored folder) first, so they win over
# bundled plugins claiming the same files, then the bundled ones. Like Noesis'
# plugins/python, both folders are on sys.path so plugins can import helper
# modules/packages that live next to them.
PLUGIN_DIRS = ["noesis_plugins", "plugins"]


class NoesisApplication:
    def __init__(self):
        self.models = []

    def run(self):
        for plugin in self.plugins():
            plugin.registerNoesisTypes()

        if (len(sys.argv) == 1):
            print("Usage: noesis <file1> <file2> ...")
            return

        files = sys.argv[1:len(sys.argv)]

        for file in files:
            self.loadFile(file)

        NoesisViewer(self.models).call()

    # private

    def loadFile(self, file):
        filename, file_extension = os.path.splitext(file)
        extension = file_extension.lower()
        handlers = [x for x in plugins if x.loadModel and extension in
                    [f.strip().lower() for f in x.format.split(";")]]

        if not handlers:
            print("File format not supported")
            return

        with open(file, "rb") as f:
            data = f.read()

        rapi.setLastCheckedName(file)
        for handler in handlers:
            # Like Noesis, the first handler whose type check accepts the data wins.
            if handler.checkType is None or handler.checkType(data):
                print("Loading %s with '%s'" % (file, handler.name))
                handler.loadModel(data, self.models)
                return

        print("No plugin accepted " + file)

    def plugins(self):
        here = dirname(os.path.abspath(__file__))
        modules = []
        for folder in PLUGIN_DIRS:
            path = os.path.join(here, folder)
            if not os.path.isdir(path):
                continue
            if path not in sys.path:
                sys.path.insert(0, path)
            for f in sorted(glob.glob(os.path.join(path, "fmt_*.py"))):
                modules.append(basename(f)[:-3])
        # modules are importable by bare name now that their folders are on sys.path
        return map(import_module, modules)


if __name__ == "__main__":
    NoesisApplication().run()
