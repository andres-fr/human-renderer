#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Init file for the add-on.

To install it, make sure Blender's Python is able to find it under
addon_utils.paths(), and that the Blender version matches to make it
installable.

Alternatively, run this init file as a script from Blender.
"""


__author__ = "Andres FR"


import bpy
#
from .blender_utils import OperatorToMenuManager, KeymapManager
# import operators
from .ui import ObjectCursorArray
# import panels
from .ui import MY_PANEL_PT_MyPanel1, MY_PANEL_PT_MyPanel2
from .ui import MPIEA_MMR_PT_ExportPanel

#
from .ui import MaximizeAreaView3d
from .ui import MaximizeAreaConsole

# scene builder

from . import scene_builder

# #############################################################################
# ## CONFIG
# #############################################################################

name = "mpiea_mmr"  # for packaging via setup.py
VERSION = "0.1.2"  # automatically managed by bumpversion

# required by blender plugins
# (see https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo)
bl_info = {
    "name": "MPIEA MultiModalRenderer",
    "author": "Andres FR",
    "support": "TESTING",
    "blender": (2, 80, 0),
    "description": "Scene building and rendering of 3D video+audio sequences",
    # "warning": "",
    # 'wiki_url': "",
    "category": "MPIEA"}


# #############################################################################
# ## MAIN ROUTINE
# #############################################################################

classes = [ObjectCursorArray, MY_PANEL_PT_MyPanel1, MY_PANEL_PT_MyPanel2,
           MPIEA_MMR_PT_ExportPanel, MaximizeAreaView3d, MaximizeAreaConsole]
register_cl, unregister_cl = bpy.utils.register_classes_factory(classes)
kmm = KeymapManager()
omm = OperatorToMenuManager()


def register():
    """
    Main register function, called on startup by Blender
    """
    register_cl()
    omm.register(ObjectCursorArray, bpy.types.VIEW3D_MT_object)
    kmm.register("D", "PRESS", ObjectCursorArray.bl_idname)
    #
    # scene_builder.main(**scene_builder.MAIN_KWARGS)


def unregister():
    """
    Main unregister function, called on shutdown by Blender
    """
    kmm.unregister()
    omm.unregister()
    unregister_cl()


if __name__ == "__main__":
    # This gets executed if calling `blender --python <THIS_FILE>.py`
    register()


print("[Add-on loaded]: ", bl_info["name"], "version", VERSION)
