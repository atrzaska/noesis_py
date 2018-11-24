# Noesis-Py

Noesis implementation that works on Linux and MacOS

# Dependencies

- cpython2
- pip2
- direnv

# Installation

    git clone ...
    cd noesis_py
    direnv allow
    setup

# Usage

    noesis ~/Desktop/model.fbx
    noesis model1.fbx model2.fbx
    DEBUG=true noesis model.fbx

List of models loaded depends on available plugins.

# Work In Progress

This project is a work in progress. At the moment it only allows basic viewing of noesis supported models.

There are currently many methods that are not implemented yet.

To view a list of not implemented methods please run (`ag` program is required):

    ag logNotImplementedMethod
    ag "\*args"

# Configuration

Supported environement variables that can be manipulated

DEBUG=true # turns on debug logging, default false
SCALE=2 # scale of the window by 2, default 1

# Problems

This implementation of noesis library is pure python only.
Loading of the models is currently very slow due to fact that each buffer value needs to be unpacked and converted to noesis classes.

# Licence

MIT
