#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains custom subclasses of bpy.ops.Operator
"""


__author__ = "Andres FR"


import bpy


class ObjectCursorArray(bpy.types.Operator):
    """
    Duplicates selected object N times between its position and the cursor's.

    More info:
    <API_URL>/bpy.types.Operator.html#bpy.types.Operator.bl_options
    """
    bl_idname = "object.cursor_array"  # This comes after 'bpy.ops'
    bl_label = "Cursor Array Label"
    bl_options = {'REGISTER', 'UNDO'}

    tot1: bpy.props.IntProperty(name="Steps1", default=2, min=1, max=100)
    tot2: bpy.props.IntProperty(name="Steps2", default=2, min=1, max=100)

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
