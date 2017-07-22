import glob
from os.path import dirname, basename, isfile
from noesis import noesis
from importlib import import_module

class NoesisApplication:
    def run(self):
        for plugin in self.plugins():
            plugin.registerNoesisTypes()

        fo = open("/Users/andrzej/Documents/mmd/projects/pymmd/data/model.pmd", "rb")
        noesis.plugins[0].noepyLoadModel(fo, noesis.mdlList)

        fo = open("/Users/andrzej/Documents/mmd/projects/pymmd/data/model.mdl", "rb")
        noesis.plugins[1].noepyLoadModel(fo, noesis.mdlList)

    def plugins(self):
        files = glob.glob("lib/plugins/fmt_*.py")
        plugins = [ basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]
        plugins = map(lambda x: "plugins." + x, plugins)
        return map(import_module, plugins)
