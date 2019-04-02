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
from .blender_utils import resolve_path


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

    @classmethod
    def clean_and_purge_scene(_, context):
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
    FLOOR_IMG_ABSPATH = resolve_path("data", "images", "marble_chess.jpg")

    @classmethod
    def create_basic_scene(clss, context):
        """
        See class docstring.
        """
        add_sun(context, clss.SUN_NAME, clss.SUN_LOC, clss.SUN_ROT,
                clss.SUN_STRENGTH)
        add_cam(context, clss.CAM_NAME, clss.CAM_LOC, clss.CAM_ROT,
                clss.CAM_LIGHT_NAME, clss.CAM_LIGHT_LOC,
                clss.CAM_LIGHT_WATTS, clss.CAM_LIGHT_SHADOW)
        add_floor(context, clss.FLOOR_NAME, clss.FLOOR_SIZE,
                  clss.FLOOR_METALLIC, clss.FLOOR_SPECULAR,
                  clss.FLOOR_ROUGHNESS, clss.FLOOR_SUBSURFACE_RATIO,
                  clss.FLOOR_SUBSURFACE_COLOR, clss.FLOOR_IMG_ABSPATH)


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
        Predicate, True if context.area.type=='VIEW_3D' (or
        context.area is None, for background mode)
        """
        if context.area is None:
            return True
        else:
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
        context.area.type == "VIEW_3D" (or context.area is None, for
        background mode)
        """
        num_objects = len(context.scene.objects)
        if num_objects > 0:
            # always false for more than zero objects
            return False
        elif context.area is None:
            # true if there are 0 objects and area doesn't exist
            return True
        else:
            # true if there are 0 objects and existing area is of type 3d
            return context.area.type == "VIEW_3D"

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
    bl_idname = "scene.clean_purge_and_create_basic_scene"  # 'bpy.ops...'
    bl_label = "Clean, purge and create basic scene"
    # bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """
        Predicate, True if context.area.type=='VIEW_3D' (or
        context.area is None, for background mode)
        """
        if context.area is None:
            return True
        else:
            return context.area.type == "VIEW_3D"

    def execute(self, context):
        """
        See class docstring.
        """
        self.clean_and_purge_scene(context)
        self.create_basic_scene(context)
        return {'FINISHED'}


# #############################################################################
# ## MAKEHUMAN
# #############################################################################
