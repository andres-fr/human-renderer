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

# class VIEW3D_PT_view3d_cursor(bpy.types.Panel):

#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = "View"
#     bl_label = "3D Cursor"

#     def draw(self, context):
#         layout = self.layout

#         cursor = context.scene.cursor

#         layout.column().prop(cursor, "location", text="Location")  ### asdf
#         rotation_mode = cursor.rotation_mode
#         if rotation_mode == 'QUATERNION':
#             layout.column().prop(cursor, "rotation_quaternion", text="Rotation")
#         elif rotation_mode == 'AXIS_ANGLE':
#             layout.column().prop(cursor, "rotation_axis_angle", text="Rotation")
#         else:
#             layout.column().prop(cursor, "rotation_euler", text="Rotation")
#         layout.prop(cursor, "rotation_mode", text="")


class MpieaMmrPanel():
    """
    Mix-in to be inherited by every MPIEA MMR Panel.
    """
    bl_category = "MPIEA MultiModalRenderer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "object"  # This makes the top right tab show up.
    # bl_options = {'UNDO'}  # {'HIDE_HEADER', 'UNDO', 'REGISTER', 'DEFAULT_CLOSED'}


class MY_PANEL_PT_MyPanel1(bpy.types.Panel, MpieaMmrPanel):
    """
    | Tutorial on layout:
    | https://blender.stackexchange.com/a/44064
    """
    bl_label = "Panel Name 1"

    @classmethod
    def poll(cls, context):
        """
        """
        return (context.object is not None)

    def draw(self, context):
        """
        """
        layout = self.layout
        scene = context.scene
        # obj = context.object
        # row.prop(obj, "hide_select")
        # row.prop(obj, "hide_render")

        box = layout.box()
        row = box.row()
        row.label(text='1111111 LABEL')
        row = box.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        row = box.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")


class MY_PANEL_PT_MyPanel2(bpy.types.Panel, MpieaMmrPanel):
    """
    | Tutorial on layout:
    | https://blender.stackexchange.com/a/44064
    """
    bl_label = "Panel Name 2"

    @classmethod
    def poll(cls, context):
        """
        """
        return (context.object is not None)

    def draw(self, context):
        """
        """
        layout = self.layout
        scene = context.scene
        # obj = context.object
        # row.prop(obj, "hide_select")
        # row.prop(obj, "hide_render")

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

classes = [ObjectCursorArray, MY_PANEL_PT_MyPanel2, MY_PANEL_PT_MyPanel1]
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
