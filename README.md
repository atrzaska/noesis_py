# Noesis-Py

Noesis implementation that works on Linux and MacOS. Goal of this project is to provide a working open source implementation of noesis software which provides ability to load plugins written for original noesis. That said, plugins written once for noesis should work with this project without any changes. API should be consistent with official noesis implementation.

http://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91

Noesis is a tool for previewing and converting between hundreds of model, image, and animation formats. It utilizes a robust plugin system, with support for native extension modules and Python scripts. The plugin/script API features hundreds of functions and interfaces which assist in developing new formats, tools, and visualization aids. Noesis also features processing, conversion, and visualization options for many different types of volume data, including medical imaging formats such as Analyze 7.5, NifTI-1, and DICOM.

![Screenshot](/screenshots/screenshot.png?raw=true)
On a screenshot you can see a PMX model loaded with `fmt_MikuMikuDance_pmx.py` noesis plugin.

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

# 3D Navigation

3D OpenGL window has following navigation features:

- hold left mouse button and move the mouse to rotate
- hold right mouse button and move the mouse to pan
- scroll up to zoom in
- scoll down to zoom out

# Work In Progress

This project is a work in progress. At the moment it only allows basic viewing of noesis supported models.

There are currently many methods that are not implemented yet.

To view a list of not implemented methods please run (`ag` program is required):

    ag logNotImplementedMethod
    ag "\*args"
    

# Not implemented features

- morphs
- bones
- quaternions
- animations
- noesis tools
- bit operations
- some matrix 4x3 operations
- some matrix 4x4 operations
- full pvr support
- from/to byte operations
- vertex colors
- tangents
- user data buffer
- light uv map


# Configuration

Supported environement variables that can be manipulated

    DEBUG=true # turns on debug logging, default false
    SCALE=2 # scale of the window by 2, default 1

# Problems

This implementation of noesis library is pure python only.
Loading of the models is currently very slow due to fact that each buffer value needs to be unpacked and converted to noesis classes.

# Licence

MIT

`inc_noesis.py` rights belong to Rich Whitehouse
`lib/plugins` plugin rights belong to original authors.
