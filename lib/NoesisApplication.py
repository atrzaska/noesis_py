import glob
from os.path import dirname, basename, isfile
from noesis import noesis
from importlib import import_module
import rapi

class NoesisApplication:
    def run(self):
        for plugin in self.plugins():
            plugin.registerNoesisTypes()

        # with open("./data/model.pmd", "rb") as f:
        #     noesis.plugins[20].noepyLoadModel(f, noesis.models)

        with open("./data/other/c001_decrypted.mdl", "rb") as f:
            noesis.plugins[21].noepyLoadModel(f, noesis.models)

        # with open("./data/other/h001_decrypted.mdl", "rb") as f:
        #     noesis.plugins[21].noepyLoadModel(f, noesis.models)

        rapi.rpgLog()

    def plugins(self):
        files = glob.glob("lib/plugins/fmt_*.py")
        plugins = [ basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]
        plugins = map(lambda x: "plugins." + x, plugins)
        return map(import_module, plugins)
