# -*- coding:utf-8 -*-


"""
Blender script
"""


import argparse
import sys
from math import radians, degrees

from mathutils import Vector, Euler  # mathutils is a blender package
import bpy
C = bpy.context
D = bpy.data

# this doesn't work inside defs, see
# https://blender.stackexchange.com/questions/23943/operator-class-retrieval
# import bpy.ops as O


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


def purge_unused_data(categories=[D.meshes, D.materials, D.textures, D.images,
                                  D.curves, D.lights, D.cameras]):
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
CAM_LOC = Vector((-5.0, -5.0, 1.6))  # cam is on the front-right
CAM_ROT = rot_euler_degrees(85.0, 0.0, -45.0)  # human-like view at the origin

CAM_LIGHT_NAME = "CamLight"
CAM_LIGHT_LOC = Vector((0.0, 1.0, 0.0))
CAM_LIGHT_WATTS = 45.0  # intensity of the bulb in watts

FLOOR_NAME = "Floor"
FLOOR_SIZE = 10  # in meters
FLOOR_METALLIC = 0.0  # metalic aspect, ratio from 0 to 1
FLOOR_SPECULAR = 0.01  # specular aspect, ratio from 0 to 1
FLOOR_ROUGHNESS = 0.2  # the higher the more light difussion. From 0 to 1
floor_mat_name = FLOOR_NAME+"Material"
FLOOR_IMG_ABSPATH = '/home/a9fb1e/github-work/human-renderer/blender_data/assets/marble_chess.jpg' 
###############################################################################
### MAIN ROUTINE
###############################################################################

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
link_from = floor_img_node.outputs["Color"]
link_to =  bsdf_inputs["Base Color"]
floor_material.node_tree.links.new(link_from, link_to)

# print(">>>>>>>>>>>>", floor_material.node_tree.links.keys())
# try:
#     img = bpy.data.images.load(path)
# except:
#     raise NameError("Cannot load image %s" % path)


# floor_material.diffuse_color = (1, 0, 0, 0) #change color


# ['Base Color', 'Subsurface', 'Subsurface Radius', 'Subsurface Color', 'Metallic', 'Specular', 'Specular Tint', 'Roughness', 'Anisotropic', 'Anisotropic Rotation', 'Sheen', 'Sheen Tint', 'Clearcoat', 'Clearcoat Roughness', 'IOR', 'Transmission', 'Transmission Roughness', 'Normal', 'Clearcoat Normal', 'Tangent']

# >>> m.node_tree.nodes['Image Texture'].image
# >>> m = C.object.data.materials['FloorMaterial']

# TODO: the script should:

# 4. Add a plane with the chess material
# 5. Add N humans in Tpose at specified positions
# 6. Load BVH sequences into humans
# register_class(HelloWorldPanel)

