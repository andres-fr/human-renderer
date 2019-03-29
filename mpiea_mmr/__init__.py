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
from .operators import ObjectCursorArray
# from . import dance_scene as ds


name = "mpiea_mmr"  # for packaging via setup.py
VERSION = "0.1.2"  # automatically managed by bumpversion


# required by blender plugins
# (see https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo)
bl_info = {
    "name": "MPIEA MultiModalRenderer",
    "author": "Andres FR",
    "support": "TESTING",
    "blender": (2, 80, 0),
    # "location": "View3D > Add > Mesh > Generate",
    # "location": "View3D > Tools > MakeWalk",
    "description": "Scene building and rendering of 3D video+audio sequences",
    # "warning": "",
    # 'wiki_url': "",
    "category": "MPIEA"}



# #############################################################################
# ## UI
# #############################################################################


class MyPanel(bpy.types.Panel):
    """
    | Tutorial on layout:
    | https://blender.stackexchange.com/a/44064
    """

    bl_idname = "MY_PANEL_PT_MyPanel"
    bl_label = "Selection Manager"
    bl_space_type = "VIEW_3D" # 'PROPERTIES'
    bl_region_type = "UI" # 'WINDOW'
    # bl_context = "object"
    # bl_options = {'REGISTER', 'UNDO'} {'DEFAULT_CLOSED'}
    bl_category = "DAZ Runtime"

    @classmethod
    def poll(cls, context):
        """
        """
        return (context.object is not None)

    def draw_header(self, context):
        """
        Draw UI elements into the panel’s header UI layout
        """
        layout = self.layout
        scene = context.scene
        # obj = context.object
        # fn = lambda self, context: obj.select_set(state=True)
        # self.append(fn)

        ###layout.prop(fn, text="quackkk")
        # layout.prop(obj, "select_set", text="")
        # bpy.ops.object.select_all(action="DESELECT")

        box = layout.box()
        row = box.row()
        row.label(text='some label')
        row = box.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        row = box.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

    def draw(self, context):
        """
        """
        layout = self.layout
        scene = context.scene
        # obj = context.object
        # row = layout.row()
        # row.prop(obj, "hide_select")
        # row.prop(obj, "hide_render")

        # box = layout.box()
        # box.label(text="Selection Tools")
        # box.operator("object.select_all").action = 'TOGGLE'
        # row = box.row()
        # row.operator("object.select_all").action = 'INVERT'
        # row.operator("object.select_random")


        box = layout.box()
        row = box.row()
        row.label(text='2222222222 LABEL')
        row = box.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        row = box.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")




# #############################################################################
# ## MAIN ROUTINE
# #############################################################################

classes = [ObjectCursorArray, MyPanel]
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
