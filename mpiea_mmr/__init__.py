#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Init file for the add-on.

To install it, make sure Blender's Python is able to find it under
addon_utils.paths(), and that the Blender version matches to make it
installable.

Alternatively, run this init file as a script from Blender.
"""

from packaging.version import parse
import ast
#
import bpy
#
# from . import dance_scene as ds

name = "mpiea_mmr"  # for packaging via setup.py
VERSION = "0.1.2"  # automatically managed by bumpversion

# required by blender plugins
# (see https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo)
bl_info = {
    "name": "MPIEA MultiModalRenderer",
    "author": "Andres FR",
    "support":"TESTING",
    "blender": (2, 80, 0),
    # "location": "View3D > Tools > MakeWalk",
    "description": "Scene building and rendering of 3D video+audio sequences",
    # "warning": "",
    # 'wiki_url': "",
    "category": "MPIEA"}



###############################################################################
### INITIALIZE/REGISTER
###############################################################################

classes = [
    # MCP_PT_Main,
    # MCP_PT_Utility,
    # utils.ErrorOperator
]

def register():
    """
    """
    # my_module.initialize()  # some modules may require this
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """
    """
    # my_module.uninitialize()
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    # This gets executed if calling `blender --python <THIS_FILE>.py`
    # register()
    pass


print("[Add-on loaded]: ", bl_info["name"], "version", VERSION)
