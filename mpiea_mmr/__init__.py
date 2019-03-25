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
# from . import blender_utils
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
    # "location": "View3D > Tools > MakeWalk",
    "description": "Scene building and rendering of 3D video+audio sequences",
    # "warning": "",
    # 'wiki_url': "",
    "category": "MPIEA"}

# #############################################################################
# ## UI
# #############################################################################

# class ObjectSelectPanel(bpy.types.Panel):
#     bl_idname = "OBJECT_PT_select"
#     bl_label = "Select"
#     bl_space_type = 'PROPERTIES'
#     bl_region_type = 'WINDOW'
#     bl_context = "object"
#     bl_options = {'DEFAULT_CLOSED'}

#     @classmethod
#     def poll(cls, context):
#         return (context.object is not None)

#     def draw_header(self, context):
#         layout = self.layout
#         obj = context.object
#         layout.prop(obj, "select", text="")

#     def draw(self, context):
#         layout = self.layout

#         obj = context.object
#         row = layout.row()
#         row.prop(obj, "hide_select")
#         row.prop(obj, "hide_render")

#         box = layout.box()
#         box.label("Selection Tools")
#         box.operator("object.select_all").action = 'TOGGLE'
#         row = box.row()
#         row.operator("object.select_all").action = 'INVERT'
#         row.operator("object.select_random")

# class ObjectCursorArray(bpy.types.Operator):
#     """
#     Object Cursor Array
#     """
#     bl_idname = "object.cursor_array"
#     bl_label = "Cursor Array"
#     bl_options = {'REGISTER', 'UNDO'}

#     total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

#     def execute(self, context):
#         """
#         """
#         scene = context.scene
#         cursor = scene.cursor_location
#         obj = scene.objects.active

#         for i in range(self.total):
#             obj_new = obj.copy()
#             scene.objects.link(obj_new)

#             factor = i / self.total
#             obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

#         return {'FINISHED'}


# def menu_func(self, context):
#     """
#     """
#     self.layout.operator(ObjectCursorArray.bl_idname)

# # store keymaps here to access after registration
# addon_keymaps = []


# def register():
#     bpy.utils.register_class(ObjectCursorArray)
#     bpy.types.VIEW3D_MT_object.append(menu_func)

#     # handle the keymap
#     wm = bpy.context.window_manager
#     # Note that in background mode (no GUI available), keyconfigs are not available either,
#     # so we have to check this to avoid nasty errors in background case.
#     kc = wm.keyconfigs.addon
#     if kc:
#         km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
#         kmi = km.keymap_items.new(ObjectCursorArray.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
#         kmi.properties.total = 4
#         addon_keymaps.append((km, kmi))

# def unregister():
#     # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
#     # Can avoid strange issues like keymap still referring to operators already unregistered...
#     # handle the keymap
#     for km, kmi in addon_keymaps:
#         km.keymap_items.remove(kmi)
#     addon_keymaps.clear()

#     bpy.utils.unregister_class(ObjectCursorArray)
#     bpy.types.VIEW3D_MT_object.remove(menu_func)



# #############################################################################
# ## INITIALIZE/REGISTER
# #############################################################################

classes = [ObjectSelectPanel]

# classes = [
#     # MCP_PT_Main,
#     # MCP_PT_Utility,
#     # utils.ErrorOperator
# ]


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
    register()


print("[Add-on loaded]: ", bl_info["name"], "version", VERSION)
