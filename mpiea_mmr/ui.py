#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the functionality related to user-interaction (UI)
with Blender, i.e.:

- Subclasses from ``bpy.types.Operator`` defining user-callable functors.
- Subclasses from ``bpy.types.Panel`` that contain GUI widgets and \
functionality.
"""


__author__ = "Andres FR"


from bpy.types import Operator, Panel
from bpy.props import IntProperty


# #############################################################################
# ## OPERATORS
# #############################################################################

class ObjectCursorArray(Operator):
    """
    Duplicates selected object N times between its position and the cursor's.

    More info:
    <API_URL>/bpy.types.Operator.html#bpy.types.Operator.bl_options
    """
    bl_idname = "object.cursor_array"  # This comes after 'bpy.ops'
    bl_label = "Cursor Array Label"
    bl_options = {'REGISTER', 'UNDO'}

    tot1: IntProperty(name="Steps1", default=2, min=1, max=100)
    tot2: IntProperty(name="Steps2", default=2, min=1, max=100)

    def execute(self, context):
        """
        """
        scene = context.scene
        cursor = scene.cursor.location
        obj = context.active_object
        tot_all = self.tot1 + self.tot2
        for i in range(tot_all):
            obj_new = obj.copy()
            scene.collection.objects.link(obj_new)

            factor = i / tot_all
            obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        return {'FINISHED'}


# #############################################################################
# ## PANELS
# #############################################################################

class MpieaMmrPanel():
    """
    Mix-in to be inherited by every Panel that belongs to the 'MPIEA
    MultiModalRenderer' tab, to avoid verbosity and potential inconsistencies.

    **Attributes:**

    bl_category
       The tab name. Blender will place the Panel in the tab
       given by its bl_category (i.e. all Panels extending this class will
       belong to the same tab).
    bl_space_type
       The tab will show up in the specified space (e.g. TEXT_EDITOR,
       IMAGE_EDITOR, VIEW_3D). If the tab is desired in multiple spaces,
       multiple classes have to be defined, each with their respective
       ``bl_space_type``.
    bl_region_type
       Value set to ``UI``, alternatives not known.

    .. note::
       Whether a Panel appears in a tab or not, and the ordering among panels
       is specified in the ``register()`` function (by simply registering all
       the desired panels in order).
    """
    bl_category = "MPIEA MultiModalRenderer"
    bl_space_type = "VIEW_3D"  # "TEXT_EDITOR"
    bl_region_type = "UI"
    # not sure if needed:
    # bl_context = "object"
    # bl_options = {'UNDO'}  # {'HIDE_HEADER', 'UNDO', 'REGISTER', 'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        """
        Dummy implementation, returns True always.
        """
        return True  # (context.object is not None)


class MPIEA_MMR_PT_ExportPanel(Panel, MpieaMmrPanel):
    """
    """
    bl_label = "Export"

    def draw(self, context):
        """
        """
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)
        # col.prop(context.scene, "make_tetrahedron_inverted")

        # if you want to call the operator with args, extend its class.
        col.operator("export_scene.obj", text="Export Obj(??)")


class MY_PANEL_PT_MyPanel1(Panel, MpieaMmrPanel):
    """
    | Tutorial on layout:
    | https://blender.stackexchange.com/a/44064
    """
    bl_label = "Panel Name 1"


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


class MY_PANEL_PT_MyPanel2(Panel, MpieaMmrPanel):
    """
    | Tutorial on layout:
    | https://blender.stackexchange.com/a/44064
    """
    bl_label = "Panel Name 2"

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
