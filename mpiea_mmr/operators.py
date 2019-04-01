#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains ubclasses from ``bpy.types.Operator`` defining
user-callable functors. Operators can also be embedded in Panels and
other UI elements.
"""


__author__ = "Andres FR"

from mathutils import Vector  # mathutils is a blender package
import bpy
from bpy.types import Operator
# from bpy.props import IntProperty
#
from .blender_utils import get_area_by_type
from .blender_utils import rot_euler_degrees
from .blender_utils import PurgeUnusedData
from .blender_utils import add_sun
from .blender_utils import add_cam
from .blender_utils import add_floor
from .blender_utils import asset_path
#



# #############################################################################
# ## EXAMPLE
# #############################################################################

# class ObjectCursorArray(Operator):
#     """
#     Duplicates selected object N times between its position and the cursor's.

#     More info:
#     <API_URL>/bpy.types.Operator.html#bpy.types.Operator.bl_options
#     """
#     bl_idname = "object.cursor_array"  # This comes after 'bpy.ops'
#     bl_label = "Cursor Array Label"
#     bl_options = {'REGISTER', 'UNDO'}

#     tot1: IntProperty(name="Steps1", default=2, min=1, max=100)
#     tot2: IntProperty(name="Steps2", default=2, min=1, max=100)

#     def execute(self, context):
#         """
#         """
#         scene = context.scene
#         cursor = scene.cursor.location
#         obj = context.active_object
#         tot_all = self.tot1 + self.tot2
#         for i in range(tot_all):
#             obj_new = obj.copy()
#             scene.collection.objects.link(obj_new)

#             factor = i / tot_all
#             obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

#         return {'FINISHED'}


# #############################################################################
# ## APPEARANCE
# #############################################################################

class AbstractMaximizeArea():
    """
    If the current context has an area of type self.AREA_TYPE, that area gets
    maximized. Otherwise does nothing. Supported types can be seen here::

    .. warning::

      This is an **abstract class**. It is not expected to be directly
      used. Instead, extend it before as shown.

    To create an Operator for a specific area type, simply extend this class
    as follows::

       class MaximizeAreaView3d(Operator, AbstractMaximizeArea):
           AREA_TYPE = "VIEW_3D"
           bl_idname = "screen.maximize_view_3d"  # path after 'bpy.ops'
           bl_label = "Maximize VIEW_3D (if present)"

    | Supported types can be seen here:
    | https://docs.blender.org/api/blender2.8/bpy.types.Area.html
    """

    @classmethod
    def poll(cls, context):
        """
        Predicate, True iff context.screen.areas contains an area
        of self.AREA_TYPE
        """
        a = get_area_by_type(context, cls.AREA_TYPE)
        return (a is not None)

    def execute(self, context):
        """
        See class docstring.
        """
        a = get_area_by_type(context, self.AREA_TYPE)
        bpy.ops.screen.screen_full_area({"area": a})
        return {"FINISHED"}


class MaximizeAreaView3d(Operator, AbstractMaximizeArea):
    """
    See docstring for AbstractMaximizeArea.
    """
    AREA_TYPE = "VIEW_3D"
    bl_idname = "screen.maximize_view_3d"  # path after 'bpy.ops'
    bl_label = "Maximize VIEW_3D (if present)"


class MaximizeAreaConsole(Operator, AbstractMaximizeArea):
    """
    See docstring for AbstractMaximizeArea.
    """
    AREA_TYPE = "CONSOLE"
    bl_idname = "screen.maximize_console"  # path after 'bpy.ops'
    bl_label = "Maximize Python console (if present)"


# #############################################################################
# ## SCENE BUILDING
# #############################################################################


class CleanAndPurgeSceneMixin():
    """
    Contains functionality to remove all objects in the secene, as well as all
    data blocks with zero users.
    """

    def clean_and_purge_scene(self, context):
        """
        See class docstring.
        """
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()
        PurgeUnusedData()()


class CreateBasicSceneMixin():
    """
    Contains the following functionality:
    1. Adds a sun with
    Removes all objects in the secene, as well as all data blocks with zero
    users.
    """

    SUN_NAME = "SunLight"
    SUN_LOC = Vector((0.0, 0.0, 10.0))
    SUN_ROT = rot_euler_degrees(0, 0, 0)
    SUN_STRENGTH = 1.0  # in units relative to a reference sun
    #
    CAM_NAME = "Cam"
    CAM_LOC = Vector((-9.0, -9.0, 1.6))  # cam is on the front-right
    CAM_ROT = rot_euler_degrees(85.0, 0.0, -45.0)  # human-like view to origin
    #
    CAM_LIGHT_NAME = "CamLight"
    CAM_LIGHT_LOC = Vector((0.0, 1.0, 0.0))
    CAM_LIGHT_WATTS = 40.0  # intensity of the bulb in watts
    CAM_LIGHT_SHADOW = False
    #
    FLOOR_NAME = "Floor"
    FLOOR_SIZE = 20  # in meters
    FLOOR_METALLIC = 0.0  # metalic aspect, ratio from 0 to 1
    FLOOR_SPECULAR = 0.0  # specular aspect, ratio from 0 to 1
    FLOOR_ROUGHNESS = 1.0  # the higher the more light difussion. From 0 to 1
    FLOOR_SUBSURFACE_RATIO = 0.5
    FLOOR_SUBSURFACE_COLOR = Vector((1.0, 1.0, 1.0, 1.0))  # RGBA (A=1 opaque)
    FLOOR_IMG_ABSPATH = asset_path("assets", "images", "marble_chess.jpg")

    def create_basic_scene(self, context):
        """
        See class docstring.
        """
        add_sun(context, self.SUN_NAME, self.SUN_LOC, self.SUN_ROT,
                self.SUN_STRENGTH)
        add_cam(context, self.CAM_NAME, self.CAM_LOC, self.CAM_ROT,
                self.CAM_LIGHT_NAME, self.CAM_LIGHT_LOC,
                self.CAM_LIGHT_WATTS, self.CAM_LIGHT_SHADOW)
        add_floor(context, self.FLOOR_NAME, self.FLOOR_SIZE,
                  self.FLOOR_METALLIC, self.FLOOR_SPECULAR,
                  self.FLOOR_ROUGHNESS, self.FLOOR_SUBSURFACE_RATIO,
                  self.FLOOR_SUBSURFACE_COLOR, self.FLOOR_IMG_ABSPATH)


class CleanAndPurgeScene(CleanAndPurgeSceneMixin, Operator):
    """
    Straightforward implementation of the CleanAndPurgeSceneMixin.
    """

    bl_idname = "scene.clean_and_purge"  # This comes after 'bpy.ops'
    bl_label = "Clean and purge scene"
    # bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """
        Predicate, True iff context.area.type=='VIEW_3D'
        """
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        """
        See class docstring.
        """
        self.clean_and_purge_scene(context)
        return {'FINISHED'}


class CreateBasicScene(CreateBasicSceneMixin, Operator):
    """
    Straightforward implementation of the CreateBasicSceneMixin.
    """

    bl_idname = "scene.create_basic_scene"  # This comes after 'bpy.ops'
    bl_label = "Create basic scene"
    # bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """
        Predicate, True iff the ``context.scene`` has zero objects and
        context.area.type == "VIEW_3D"
        """
        num_objects = len(context.scene.objects)
        is_area_3d = context.area.type == "VIEW_3D"
        return is_area_3d and (num_objects == 0)

    def execute(self, context):
        """
        See class docstring.
        """
        self.create_basic_scene(context)
        return {'FINISHED'}


class CleanPurgeAndCreateBasicScene(CleanAndPurgeSceneMixin,
                                    CreateBasicSceneMixin, Operator):
    """
    Equivalent of first calling CleanAndPurgeScene, then CreateBasicScene.
    """
    bl_idname = "scene.clean_purge_and_create_basic_scene"  # This comes after 'bpy.ops'
    bl_label = "Clean, purge and create basic scene"
    # bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """
        Predicate, True iff context.area.type=='VIEW_3D'
        """
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        """
        See class docstring.
        """
        self.clean_and_purge_scene(context)
        self.create_basic_scene(context)
        return {'FINISHED'}
