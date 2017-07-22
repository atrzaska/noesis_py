# import sys
# from Application import Application
# app = Application()
# app.run(sys.argv[1])

import importlib
from noesis import noesis
from noesis_plugins import plugins
from noesis_plugins.fmt_MikuMikuDance_pmd import registerNoesisTypes

if __name__ == "__main__":
    plugins = map(lambda x: "noesis_plugins." + x, plugins)
    modules = map(importlib.import_module, plugins)
    for module in modules:
        module.registerNoesisTypes()

    fo = open("/Users/andrzej/Downloads/model.pmd", "rb")
    noesis.plugins[0].noepyLoadModel(fo, noesis.mdlList)

    fo = open("/Users/andrzej/Downloads/model.mdl", "rb")
    noesis.plugins[1].noepyLoadModel(fo, noesis.mdlList)
