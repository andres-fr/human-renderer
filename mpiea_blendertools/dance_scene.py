# -*- coding:utf-8 -*-


"""
Scene builder script for Blender. It performs the following tasks:
1. General config (rendering etc)
2. Create and configure sunlight
3. Create and configure camera
4. Create camera light, append to camera and configure
5. Create floor with tiled image texture and colored subsurface
6. Load human model as MHX2 format
7. Load motion capture as BVH and apply to human
8. Run sequence
"""


import argparse
import sys
from math import radians, degrees

from mathutils import Vector, Euler  # mathutils is a blender package
import bpy
C = bpy.context
D = bpy.data


__author__ = "Andres FR"


###############################################################################
### HELPERS
###############################################################################

def rot_euler_degrees(rot_x, rot_y, rot_z, order="XYZ"):
    """
    Returns an Euler rotation object with the given rotations (in degrees)
    and rotation order.
    """
    return Euler((radians(rot_x), radians(rot_y), radians(rot_z)), order)

###

def update_scene():
    """
    Sometimes changes don't show up due to lazy evaluation. This function
    triggers scene update and recalculation of all changes.
    """
    C.scene.update()

def save_blenderfile(filepath=D.filepath):
    """
    Saves blender file
    """
    O.wm.save_as_mainfile(filepath=filepath)

def open_blenderfile(filepath=D.filepath):
    """
    Saves blender file
    """
    O.wm.open_mainfile(filepath=filepath)

def set_render_resolution_percentage(p=100):
    """
    """
    D.scenes[0].render.resolution_percentage = p

def get_obj(obj_name):
    """
    Actions like undo or entering edit mode invalidate the object references.
    This function returns a reference that is always valid, assuming that the
    given obj_name is a key of bpy.data.objects.
    """
    return D.objects[obj_name]

def select_by_name(*names):
    """
    Given a variable number of names as strings, tries to select all existing
    objects in D.objects by their name.
    """
    for name in names:
        try:
            D.objects[name].select_set(True)
        except Exception as e:
            print(e)

def deselect_by_name(*names):
    """
    Given a variable number of names as strings, tries to select all existing
    objects in D.objects by their name.
    """
    for name in names:
        try:
            D.objects[name].select_set(False)
        except Exception as e:
            print(e)

def select_all(action="SELECT"):
    """
    Action can be SELECT, DESELECT, INVERT, TOGGLE
    """
    bpy.ops.object.select_all(action=action)

def delete_selected():
    bpy.ops.object.delete()

def set_mode(mode="OBJECT"):
    """
    """
    bpy.ops.object.mode_set(mode=mode)

def purge_unused_data(categories=[D.meshes, D.materials, D.textures, D.images,
                                  D.curves, D.lights, D.cameras, D.screens]):
    """
    Blender objects point to data. E.g., a lamp points to a given data lamp
    object. Removing the objects doesn't remove the data, which may lead to
    data blocks that aren't being used by anyone. Given an ORDERED collection
    of categories, this function removes all unused datablocks.
    See https://blender.stackexchange.com/a/102046
    """
    for cat in categories:
        for block in cat:
            if block.users == 0:
                cat.remove(block)

class ArgumentParserForBlender(argparse.ArgumentParser):
    """
    This class is identical to its superclass, except for the parse_args
    method (see docstring). It resolves the ambiguity generated when calling
    Blender from the CLI with a python script, and both Blender and the script
    have arguments. E.g., the following call will make Blender crash because
    it will try to process the script's -a and -b flags:
    >>> blender --python my_script.py -a 1 -b 2

    To bypass this issue this class uses the fact that Blender will ignore all
    arguments given after a double-dash ('--'). The approach is that all
    arguments before '--' go to Blender, arguments after go to the script.
    The following calls work fine:
    >>> blender --python my_script.py -- -a 1 -b 2
    >>> blender --python my_script.py --
    """

    def _get_argv_after_doubledash(self):
        """
        Given the sys.argv as a list of strings, this method returns the
        sublist right after the '--' element (if present, otherwise returns
        an empty list).
        """
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx+1:] # the list after '--'
        except ValueError as e: # '--' not in the list:
            return []

    # overrides superclass
    def parse_args(self):
        """
        This method is expected to behave identically as in the superclass,
        except that the sys.argv list will be pre-processed using
        _get_argv_after_doubledash before. See the docstring of the class for
        usage examples and details.
        """
        return super().parse_args(args=self._get_argv_after_doubledash())

def set_shading_mode(mode="SOLID", screens=[]):
    """
    Performs an action analogous to clicking on the display/shade button of
    the 3D view. Mode is one of "RENDERED", "MATERIAL", "SOLID", "WIREFRAME".
    The change is applied to the given collection of bpy.data.screens.
    If none is given, the function is applied to bpy.context.screen (the
    active screen) only. E.g. set all screens to rendered mode:
      set_shading_mode("RENDERED", D.screens)
    """
    screens = screens if screens else [C.screen]
    for s in screens:
        for spc in s.areas:
            if spc.type == "VIEW_3D":
                spc.spaces[0].shading.type = mode
                break # we expect at most 1 VIEW_3D space


def maximize_layout_3d_area():
    """
    TODO: this function assumes Layout is the bpy.context.workspace.
    It does the following:
    1. If there is an area with the given name:
       1.1. Minimizes any other maximized window
       1.2. Maximizes the desired area
    """
    screen_name = "Layout"
    area_name = "VIEW_3D"
    screen = D.screens[screen_name]
    for a in screen.areas:
        if a.type == area_name:
            # If screen is already in some fullscreen mode, revert it
            if screen.show_fullscreen:
                bpy.ops.screen.back_to_previous()
            # Set area to fullscreen (dict admits "window","screen","area")
            bpy.ops.screen.screen_full_area({"screen": screen, "area": a})
            break

###############################################################################
### GLOBALS
###############################################################################

# parser = ArgumentParserForBlender()
# parser.add_argument("-q", "--quack",
#                     action="store_true",
#                     help="Quacks foo times if activated.")
# parser.add_argument("-b", "--bar", type=int, default=10,
#                     help="Number of desired quacks")
# args = parser.parse_args()
# QUACK = args.quack
# BAR = args.bar


INIT_SHADING_MODE = "RENDERED"
INIT_3D_MAXIMIZED = False
# renderer
EEVEE_RENDER_SAMPLES = 1
EEVEE_VIEWPORT_SAMPLES = 1
EEVEE_VIEWPORT_DENOISING = False
# sequencer
FRAME_START = 2  # 1 is T-pose if imported with MakeWalk


# In Blender, x points away from the cam, y to the left and z up
# (right-hand rule). Locations are in meters, rotation in degrees.
# Positive rotation on an axis means counter-clockwise when
# the axis points to the cam. 0,0,0 rotation points straight
# to the bottom.

SUN_NAME = "SunLight"
SUN_LOC = Vector((0.0, 0.0, 10.0))
SUN_ROT = rot_euler_degrees(0, 0, 0)
SUN_STRENGTH = 1.0  # in units relative to a reference sun

CAM_NAME = "Cam"
CAM_LOC = Vector((-9.0, -9.0, 1.6))  # cam is on the front-right
CAM_ROT = rot_euler_degrees(85.0, 0.0, -45.0)  # human-like view at the origin

CAM_LIGHT_NAME = "CamLight"
CAM_LIGHT_LOC = Vector((0.0, 1.0, 0.0))
CAM_LIGHT_WATTS = 40.0  # intensity of the bulb in watts
CAM_LIGHT_SHADOW = False

FLOOR_NAME = "Floor"
FLOOR_SIZE = 10  # in meters
FLOOR_METALLIC = 0.0  # metalic aspect, ratio from 0 to 1
FLOOR_SPECULAR = 0.0  # specular aspect, ratio from 0 to 1
FLOOR_ROUGHNESS = 1.0  # the higher the more light difussion. From 0 to 1
FLOOR_SUBSURFACE_RATIO = 0.5
FLOOR_SUBSURFACE_COLOR = Vector((1.0, 1.0, 1.0, 1.0))  # RGBA (A=1 for opaque)
floor_mat_name = FLOOR_NAME+"Material"
FLOOR_IMG_ABSPATH = '/home/a9fb1e/github-work/human-renderer/blender_data/assets/marble_chess.jpg'

MHX2_ABSPATH = "/home/a9fb1e/github-work/human-renderer/makehuman_data/exported_models/tpose_african.mhx2"
MHX2_NAME = "TposeAfrican"


BVH_ABSPATH = "/home/a9fb1e/github-work/human-renderer/makehuman_data/poses/cmu_motion_captures/01/01_06.bvh"




###############################################################################
### MAIN ROUTINE
###############################################################################

# general settings

# set denoising feature
C.scene.eevee.use_taa_reprojection = EEVEE_VIEWPORT_DENOISING
C.scene.eevee.taa_render_samples = EEVEE_RENDER_SAMPLES
C.scene.eevee.taa_samples = EEVEE_VIEWPORT_SAMPLES
C.scene.frame_start = FRAME_START
# set all 3D screens to RENDERED mode
set_shading_mode(INIT_SHADING_MODE, D.screens)

# set fullscreen
if INIT_3D_MAXIMIZED:
    maximize_layout_3d_area()


# select and delete all objects
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
purge_unused_data()

# add a sun
bpy.ops.object.light_add(type="SUN", location=SUN_LOC, rotation=SUN_ROT)
C.object.name = SUN_NAME
C.object.data.name = SUN_NAME
C.object.data.energy = SUN_STRENGTH

# add a cam
bpy.ops.object.camera_add(location=CAM_LOC, rotation=CAM_ROT)
C.object.name = CAM_NAME
C.object.data.name = CAM_NAME

# add light as a child of cam
bpy.ops.object.light_add(type="POINT", location=CAM_LIGHT_LOC)
C.object.name = CAM_LIGHT_NAME
C.object.data.name = CAM_LIGHT_NAME
C.object.data.energy = CAM_LIGHT_WATTS
C.object.parent = get_obj(CAM_NAME)
C.object.data.use_shadow = False


# add floor
bpy.ops.mesh.primitive_plane_add()
C.object.name = FLOOR_NAME
C.object.data.name = FLOOR_NAME
C.object.scale = (FLOOR_SIZE, FLOOR_SIZE, 0)

# add floor texture
floor_material = bpy.data.materials.new(name=floor_mat_name)
C.object.data.materials.append(floor_material)
floor_material.use_nodes = True
bsdf_inputs = floor_material.node_tree.nodes["Principled BSDF"].inputs
bsdf_inputs["Metallic"].default_value = FLOOR_METALLIC
bsdf_inputs["Specular"].default_value = FLOOR_SPECULAR
bsdf_inputs["Roughness"].default_value = FLOOR_ROUGHNESS
# add image node to floor texture, load the desired image and set it
floor_img_node = floor_material.node_tree.nodes.new("ShaderNodeTexImage")
floor_img_node.location = (-300, 300)
img = bpy.data.images.load(FLOOR_IMG_ABSPATH)
floor_img_node.image = img

# connect image node with BSDF node:
floor_material.node_tree.links.new(floor_img_node.outputs["Color"],
                                   bsdf_inputs["Base Color"])

# expand floor UV to make image be displayed in smaller tiles
floor_uv_vertices = D.meshes[FLOOR_NAME].uv_layers["UVMap"].data
for v in floor_uv_vertices: # collection of MeshUVLoops
    v.uv *= FLOOR_SIZE  # v.uv is a 2D Vector


# mix floor image with subsurface color
subsurface_node = floor_material.node_tree.nodes.new("ShaderNodeValue")
subsurface_color_node = floor_material.node_tree.nodes.new("ShaderNodeRGB")
subsurface_node.location = (-300, 100)
subsurface_color_node.location = (-300, -100)
#
subsurface_node.outputs["Value"].default_value = FLOOR_SUBSURFACE_RATIO
subsurface_color_node.outputs["Color"].default_value = FLOOR_SUBSURFACE_COLOR
#
floor_material.node_tree.links.new(subsurface_node.outputs["Value"],
                                   bsdf_inputs["Subsurface"])
floor_material.node_tree.links.new(subsurface_color_node.outputs["Color"],
                                   bsdf_inputs["Subsurface Color"])


# import makehuman
select_all(action="DESELECT")  # make sure that
select_by_name(MHX2_NAME)      # only human is selected

bpy.ops.import_scene.makehuman_mhx2(filepath=MHX2_ABSPATH)
C.object.name = MHX2_NAME
C.object.data.name = MHX2_NAME


# retarget BVH to human
bpy.ops.mcp.load_and_retarget(filepath=BVH_ABSPATH)  # Assumes selected is a human


# QUESTIONABLE/OPTIONAL STUFF:

# prevent user from selecting any light, cam or floor:
D.objects[SUN_NAME].hide_select = True
D.objects[CAM_NAME].hide_select = True
D.objects[CAM_LIGHT_NAME].hide_select = True
D.objects[FLOOR_NAME].hide_select = True
# start playing sequence
bpy.ops.screen.animation_play()



# hide from ALL viewports.
# As for dec 2018, "eye" functionality not in the API:
# https://devtalk.blender.org/t/what-object-property-does-bpy-ops-object-hide-view-set-actually-toggle/4517/3
# C.object.hide_viewport = True


# bpy.ops.object.mode_set(mode="OBJECT")
# C.object.hide_viewport = True  # hide skeleton from 3d view



# ['Base Color', 'Subsurface', 'Subsurface Radius', 'Subsurface Color', 'Metallic', 'Specular', 'Specular Tint', 'Roughness', 'Anisotropic', 'Anisotropic Rotation', 'Sheen', 'Sheen Tint', 'Clearcoat', 'Clearcoat Roughness', 'IOR', 'Transmission', 'Transmission Roughness', 'Normal', 'Clearcoat Normal', 'Tangent']

# >>> m.node_tree.nodes['Image Texture'].image
# >>> m = C.object.data.materials['FloorMaterial']

# TODO:


# 5. Add N humans in Tpose at specified positions
# TODO: create own workspace? instead of # remove undesired UI

# utest or DELETE every implemented code, used or not
# things like set_shading_mode or maximize_3d_view are to be tested on every window, every screen, every area etc. (e.g. false everywhere except the active one etc).
