# -*- coding:utf-8 -*-


"""
"""



#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Abstract
Tool for loading bvh files onto the MHX rig in Blender 2.5x

Place the script in the .blender/scripts/addons dir
Activate the script in the "Add-Ons" tab (user preferences).
Access from UI panel (N-key) when MHX rig is active.

Alternatively, run the script in the script editor (Alt-P), and access from UI panel.
"""

name = "mpiea_blendertools"  # for packaging via setup.py

# required by blender plugins:
bl_info = {
    "name": "SomeBlenderPlugin",
    "author": "SomeAuthor",
    "version": (0, 1),
    "blender": (2, 80, 0),
    # "location": "View3D > Tools > MakeWalk",
    "description": "Mocap retargeting tool",
    "warning": "",
    'wiki_url': "http://thomasmakehuman.wordpress.com/makewalk/",
    "category": "MakeHuman"}



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
    register()  # load as a script into Blender


print("Blender Plugin Loaded")
