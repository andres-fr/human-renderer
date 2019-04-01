# -*- coding:utf-8 -*-


"""
Utilities for interaction with Blender
"""


__author__ = "Andres FR"

from os.path import abspath, dirname, join
import argparse
import sys
from math import radians  # degrees
#
from mathutils import Vector, Euler  # mathutils is a blender package
import bpy
#
from . import __path__ as PACKAGE_ROOT_PATH


# #############################################################################
# ## ENVIRONMENT
# #############################################################################

def asset_path(*path_elements):
    """
    A convenience path wrapper to find assets in this repository. Retrieves
    the absolute path, given the OS-agnostic path relative to the package
    root path (by bysically joining the path elements via ``os.path.join``).
    E.g., the following call retrieves the absolute path for
    ``<PACKAGE_ROOT>/a/b/test.txt``::

       asset_path("a", "b", "test.txt")

    :params strings path_elements: From left to right, the path nodes,
       the last one being the filename.
    :rtype: str
    """
    p = tuple(PACKAGE_ROOT_PATH) + path_elements
    return join(*p)


class ArgumentParserForBlender(argparse.ArgumentParser):
    """
    This class is identical to its superclass, except for the parse_args
    method (see docstring). It resolves the ambiguity generated when calling
    Blender from the CLI with a python script, and both Blender and the script
    have arguments. E.g., the following call will make Blender crash because
    it will try to process the script's -a and -b flags:
    ::

       blender --python my_script.py -a 1 -b 2

    To bypass this issue this class uses the fact that Blender will ignore all
    arguments given after a double-dash ('--'). The approach is that all
    arguments before '--' go to Blender, arguments after go to the script.
    The following CLI calls work fine:
    ::

       blender --python my_script.py -- -a 1 -b 2
       blender --python my_script.py --
    """

    def get_argv_after_doubledash(self, argv):
        """
        :param list<str> argv: Expected to be sys.argv (or alike).
        :returns: The argv sublist after the first ``'--'`` element (if
           present, otherwise returns an empty list).
        :rtype: list of str

        .. note::
           Works with any *ordered* collection of strings (e.g. list, tuple).
        """
        try:
            idx = argv.index("--")
            return argv[idx+1:]  # the list after '--'
        except ValueError:  # '--' not in the list:
            return []

    # overrides superclass
    def parse_args(self):
        """
        This method is expected to behave identically as in the superclass,
        except that the sys.argv list will be pre-processed using
        get_argv_after_doubledash before. See the docstring of the class for
        usage examples and details.

        .. note::
           By default, `argparse.ArgumentParser` will call `sys.exit()` when
           encountering an error. Blender will react to that shutting down,
           making it look like a crash. Make sure the arguments are correct!
        """
        argv_after_dd = self.get_argv_after_doubledash(sys.argv)
        return super().parse_args(args=argv_after_dd)


# #############################################################################
# ## UI CONFIG HELPERS
# #############################################################################

class OperatorToMenuManager(list):
    """
    This class implements functionality for adding/removing operators
    into Blender UI menus. It also behaves like a regular list, holding
    the currently registered items. Usage example:
    ::

       omm = OperatorToMenuManager()
       # In register():
       omm.register(MyOperator, bpy.types.VIEW3D_MT_object)
       # ... in unregister():
       omm.unregister
    """

    def register(self, op_class, menu_class):
        """
        :param bpy.types.Operator op_class: (Sub)class handle with desired
           functionality.
        :param menu_class: Class handle for the Blender GUI where the
           functionality can be triggered.
        :type menu_class: bpy.types.{Header, Panel, ...}

        .. note::
           ``op_class`` must define the ``bl_idname`` and ``bl_label`` fields.
        """
        op_name, op_label = op_class.bl_idname, op_class.bl_label

        def menu_fn(self, context):
            """Small wrapper needed by the API"""
            self.layout.operator(op_name, text=op_label)

        menu_class.append(menu_fn)
        self.append((menu_class, menu_fn))

    def unregister(self):
        """
        Removes every mapped operator from every menu class in this collection,
        then empties the collection.
        """

        for menu_class, menu_fn in self:
            menu_class.remove(menu_fn)
        self.clear()


class KeymapManager(list):
    """
    This class implements functionality for registering/deregistering keymaps
    into Blender. It also behaves like a regular list, holding the keymaps
    currently registered. To inspect the registered keymaps simply iterate
    the instance.
    """

    KEYMAP_NAME = "Object Mode"  # ATM not well documented in the API
    KEYMAP_SPACE_TYPE = "EMPTY"  # ATM not well documented in the API

    def register(self, context, key, stroke_mode, op_name,
                 ctrl=True, shift=True, alt=False):
        """
        Adds a new keymap to this collection, and to the config in
        ``context.window_manager.keyconfigs.addon``. See the API for details:

        | https://docs.blender.org/api/blender2.8/bpy.types.KeyMap.html
        | https://docs.blender.org/api/blender2.8/bpy.types.KeyMapItem.html
        | https://docs.blender.org/manual/de/dev/advanced/keymap_editing.html

        .. warning:
           For the moment, the keymap was confirmed to work only if
           ``name="Object Mode"`` and ``space_type="EMPTY"``

        Usage example:
        ::

           kmm = KeymapManager()
           kmm.register(bpy.context, "D", "PRESS", MyOperator.bl_idname)

        :param bpy.types.Context context: The Blender context to work in.
        :param str key: See bpy.types.KeyMapItem.key_modifier
        :param str stroke_mode: See bpy.types.KeyMapItem.value
        :param str op_name: Name of a valid operation in ``bpy.ops``
           (usually the ``bl_idname``)
        :param booleans ctrl, shift, alt: Modifiers of the ``key``
        :returns: None
        """
        wm = context.window_manager
        kc = wm.keyconfigs.addon # this is None in background mode
        if kc:
            km = kc.keymaps.new(name=self.KEYMAP_NAME,
                                space_type=self.KEYMAP_SPACE_TYPE)
            kmi = km.keymap_items.new(op_name, key, stroke_mode,
                                      ctrl=ctrl, shift=shift, alt=alt)
            self.append((km, kmi))

    def unregister(self):
        """
        Removes every mapped item from every keymap in this collection, and
        then empties the collection.
        """
        for km, kmi in self:
            km.keymap_items.remove(kmi)
        self.clear()


#############################################################################
## MATH
#############################################################################

def rot_euler_degrees(rot_x, rot_y, rot_z, order="XYZ"):
    """
    Returns an Euler rotation object with the given rotations (in degrees)
    and rotation order.
    """
    return Euler((radians(rot_x), radians(rot_y), radians(rot_z)), order)


#############################################################################
## MISC
#############################################################################

# def update_scene():
#     """
#     Sometimes changes don't show up due to lazy evaluation. This function
#     triggers scene update and recalculation of all changes.
#     """
#     bpy.context.scene.update()


# def save_blenderfile(filepath):
#     """
#     Saves blender file (usually to D.filepath)
#     """
#     bpy.ops.wm.save_as_mainfile(filepath=filepath)


def open_blenderfile(filepath):
    """
     blender file
    """
    bpy.ops.wm.open_mainfile(filepath=filepath)


def set_render_resolution_percentage(p=100):
    """
    """
    D.scenes[0].render.resolution_percentage = p


# def get_obj(obj_name):
#     """
#     Actions like undo or entering edit mode invalidate the object references.
#     This function returns a reference that is always valid, assuming that the
#     given obj_name is a key of bpy.data.objects.
#     """
#     return D.objects[obj_name]


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


# def select_all(action="SELECT"):
#     """
#     Action can be SELECT, DESELECT, INVERT, TOGGLE
#     """
#     bpy.ops.object.select_all(action=action)


# def delete_selected():
#     """
#     """
#     bpy.ops.object.delete()


# def set_mode(mode="OBJECT"):
#     """
#     """
#     bpy.ops.object.mode_set(mode=mode)



def set_shading_mode(mode="SOLID", screens=[]):
    """
    Performs an action analogous to clicking on the display/shade button of
    the 3D view. Mode is one of "RENDERED", "MATERIAL", "SOLID", "WIREFRAME".
    The change is applied to the given collection of bpy.data.screens.
    If none is given, the function is applied to bpy.context.screen (the
    active screen) only. E.g. set all screens to rendered mode::

       set_shading_mode("RENDERED", D.screens)
    """
    screens = screens if screens else [bpy.context.screen]
    for s in screens:
        for spc in s.areas:
            if spc.type == "VIEW_3D":
                spc.spaces[0].shading.type = mode
                break # we expect at most 1 VIEW_3D space



def get_area_by_type(context, area_type="VIEW_3D"):
    """
    If the given ``context`` contains an area of the given ``area_type``,
    returns the area. Otherwise returns None
    """
    for a in context.screen.areas:
        if a.type == area_type:
            return a
    # if no area of given type was found
    return None


class PurgeUnusedData():
    """
    Blender objects point to data. E.g., a lamp points to a given data lamp
    object. Removing the objects doesn't remove the data, which may lead to
    data blocks that aren't being used by anyone. Given a collection
    of categories returned by the ``get_categories`` method, this function
    removes all datablocks with zero users.
    .. note::

       The order of the given categories may affect the result (e.g.
       deleting some parent data before the children may be problematic.
       See https://blender.stackexchange.com/a/102046

    .. note::
       The categories have to be returned by a method at runtime, since at
       the time of registering ``bpy.data`` is not accessible and won't
       compile.
    """

    def get_categories(self):
        """
        :returns: A list of ``bpy.data.*`` categories like ``bpy.data.meshes``.
        """
        categories = [bpy.data.meshes, bpy.data.materials, bpy.data.textures,
                      bpy.data.images, bpy.data.curves, bpy.data.lights,
                      bpy.data.cameras, bpy.data.screens,
                      #bpy.data.workspaces, bpy.data.brushes,
                      bpy.data.sounds]
        return categories

    def __call__(self):
        """
        See class docstring.
        """
        for cat in self.get_categories():
            for block in cat:
                if block.users == 0:
                    cat.remove(block)


def add_sun(context, sun_name, sun_loc, sun_rot, sun_strength):
    """
    Adds a sun object to the given context, with the given features.

    :param bpy.types.Context context: The Blender context to work in.
    :param str sun_name: The desired name for the object and its corresponding
       data block. Note that if not unique, Blender will append a number.
    :param Vector sun_loc: The ``mathutils.Vector(x,y,z)`` initial location.
    :param Euler sun_rot: The ``mathutils.Euler`` initial rotation.
    :param float sun_strength: light intensity relative a reference sun (i.e.
       ``1.0`` means "one sun" of intensity).
    :returns: None
    """
    bpy.ops.object.light_add(type="SUN", location=sun_loc, rotation=sun_rot)
    # since we just added the sun, it should be in context.object
    context.object.name = sun_name
    context.object.data.name = sun_name
    context.object.data.energy = sun_strength


def add_cam(context, cam_name, cam_loc, cam_rot,
            light_name="CamLight", light_loc=Vector((0.0, 1.0, 0.0)),
            light_watts=40.0, light_shadow=False):
    """
    Adds a camera object (and optionally a point light attached to it) to the
    given context, with the given features.

    :param bpy.types.Context context: The Blender context to work in.
    :param str cam_name: The desired name for the object and its corresponding
       data block. Note that if not unique, Blender will append a number.
    :param Vector cam_loc: The ``mathutils.Vector(x,y,z)`` initial location.
    :param Euler cam_rot: The ``mathutils.Euler`` initial rotation.

    :param str light_name: (Optional). The desired name for the object and its
       corresponding data block. Note that if not unique, Blender will append a
       number.
    :param Vector light_loc: (Optional). The ``mathutils.Vector(x,y,z)``
       initial location.
    :param Euler light_rot: (Optional). The ``mathutils.Euler`` initial
       rotation.
    :param float light_watts: (Optional). Cam light intensity in Watts.
    :param bool light_shadow: (Optional).Whether the cam light causes shadows.

    :returns: None

    .. note::
       The camera light is optional. If any of the ``light_*`` parameters is
       ``None``, it won't be added.
    """
    # add a cam
    bpy.ops.object.camera_add(location=cam_loc, rotation=cam_rot)
    context.object.name = cam_name
    context.object.data.name = cam_name
    if ((light_name is None) or (light_loc is None)
       or (light_watts is None) or (light_shadow is None)):
        return None
    else:
        # add light as a child of cam
        bpy.ops.object.light_add(type="POINT", location=light_loc)
        context.object.name = light_name
        context.object.data.name = light_name
        context.object.data.energy = light_watts
        context.object.parent = context.scene.objects[cam_name]
        context.object.data.use_shadow = light_shadow


def add_floor(context, name, size, metallic=0.0, specular=0.0, roughness=1.0,
              subsurf_ratio=0.0, subsurf_color=Vector((1.0, 1.0, 1.0, 1.0)),
              texture_img_abspath=None, texture_img_tilesize=1.0):
    """
    Adds a square mesh at zero height,(representing the floor) to the given
    context, with the given features. It adds a colored subsurface to the mesh,
    as well as some "material" options, and optionally a texture from an image.

    :param str name: The desired name for the object and its corresponding
       data block. Note that if not unique, Blender will append a number.
    :param float size: Side length of the square, in meters.

    :param float metallic: From ``0`` (not metallic) to ``1`` (fully metallic).
    :param float specular: From ``0`` (not specular) to ``1`` (fully specular).
    :param float specular: From ``0`` (not rough) to ``1`` (fully rough).

    :param float subsurf_ratio: Subsurface mix, from ``0`` (no subsurface)
       to ``1``.
    :param mathutils.Vector subsurf_color: 4-dimensional float RGBA with values
       from ``0`` (black/transparent) to ``1`` (full color/opaque).

    :param str texture_img_abspath: (Optional), absolute path to an image to
       load as tiled texture onto the plane.
    :param float texture_img_tilesize: (Optional), positive float. The size
       ratio for the tiled image texture: the bigger this number, the bigger
       the tiles on the plane will be.

    :returns: None

    .. note::
       The texture image is optional. If any of the ``texture_*`` parameters is
       ``None``, it won't be added.
    """
    # add floor
    bpy.ops.mesh.primitive_plane_add()
    plane = context.object
    plane.name = name
    plane.data.name = name
    plane.scale = (size * 0.5, size * 0.5, 0)  # because plane is 2x2

    # add floor texture
    floor_material = bpy.data.materials.new(name="Material")
    context.object.data.materials.append(floor_material)
    floor_material.use_nodes = True
    bsdf_inputs = floor_material.node_tree.nodes["Principled BSDF"].inputs
    bsdf_inputs["Metallic"].default_value = metallic
    bsdf_inputs["Specular"].default_value = specular
    bsdf_inputs["Roughness"].default_value = roughness

    # mix floor texture with subsurf color
    subsurf_node = floor_material.node_tree.nodes.new("ShaderNodeValue")
    subsurf_color_node = floor_material.node_tree.nodes.new("ShaderNodeRGB")
    subsurf_node.location = (-300, 100)
    subsurf_color_node.location = (-300, -100)
    #
    subsurf_node.outputs["Value"].default_value = subsurf_ratio
    subsurf_color_node.outputs["Color"].default_value = subsurf_color
    #
    floor_material.node_tree.links.new(subsurf_node.outputs["Value"],
                                       bsdf_inputs["Subsurface"])
    floor_material.node_tree.links.new(subsurf_color_node.outputs["Color"],
                                       bsdf_inputs["Subsurface Color"])

    # optionally add image to texture
    if (texture_img_abspath is None) or (texture_img_tilesize is None):
        return None
    else:
        img_node = floor_material.node_tree.nodes.new("ShaderNodeTexImage")
        img_node.location = (-300, 300)
        img = bpy.data.images.load(texture_img_abspath)
        img_node.image = img
        # connect image node with BSDF node:
        floor_material.node_tree.links.new(img_node.outputs["Color"],
                                           bsdf_inputs["Base Color"])

        # expand floor UV to make image be displayed in smaller tiles
        floor_uv_vertices = plane.data.uv_layers["UVMap"].data
        for v in floor_uv_vertices: # collection of MeshUVLoops
            v.uv *= size * 0.5 / texture_img_tilesize # v.uv is a 2D Vector



# #############################################################################



# # general settings

# # set denoising feature
# C.scene.eevee.use_taa_reprojection = EEVEE_VIEWPORT_DENOISING
# C.scene.eevee.taa_render_samples = EEVEE_RENDER_SAMPLES
# C.scene.eevee.taa_samples = EEVEE_VIEWPORT_SAMPLES
# C.scene.frame_start = FRAME_START
# # set all 3D screens to RENDERED mode
# set_shading_mode(INIT_SHADING_MODE, D.screens)




# # import makehuman
# select_all(action="DESELECT")  # make sure that
# select_by_name(MHX2_NAME)      # only human is selected

# bpy.ops.import_scene.makehuman_mhx2(filepath=MHX2_ABSPATH)
# C.object.name = MHX2_NAME
# C.object.data.name = MHX2_NAME


# # retarget BVH to human
# bpy.ops.mcp.load_and_retarget(filepath=BVH_ABSPATH)  # Assumes selected is a human


# # QUESTIONABLE/OPTIONAL STUFF:

# # prevent user from selecting any light, cam or floor:
# D.objects[SUN_NAME].hide_select = True
# D.objects[CAM_NAME].hide_select = True
# D.objects[CAM_LIGHT_NAME].hide_select = True
# D.objects[FLOOR_NAME].hide_select = True
# # start playing sequence
# bpy.ops.screen.animation_play()






# # #############################################################################
# # ## EYE ICON
# # ## See https://blenderartists.org/t/show-hide-collection-blender-beta-2-80/1141768
# # #############################################################################

# def get_viewport_ordered_collections(context):
#     def fn(c, out, addme):
#         if addme:
#             out.append(c)
#         for c1 in c.children:
#             out.append(c1)
#         for c1 in c.children:
#             fn(c1, out, False)
#     collections = []
#     fn(context.scene.collection, collections, True)
#     return collections

# def get_area_from_context(context, area_type):
#     area = None
#     for a in context.screen.areas:
#         if a.type == area_type:
#             area = a
#             break
#     return area

# def set_collection_viewport_visibility(context, collection_name, visibility=True):
#     collections = get_viewport_ordered_collections(context)

#     collection = None
#     index = 0
#     for c in collections:
#         if c.name == collection_name:
#             collection = c
#             break
#         index += 1

#     if collection is None:
#         return

#     first_object = None
#     if len(collection.objects) > 0:
#         first_object = collection.objects[0]

#     try:
#         bpy.ops.object.hide_collection(context, collection_index=index, toggle=True)

#         if first_object.visible_get() != visibility:
#             bpy.ops.object.hide_collection(context, collection_index=index, toggle=True)
#     except:
#         context_override = context.copy()
#         context_override["area"] = get_area_from_context(context, 'VIEW_3D')

#         bpy.ops.object.hide_collection(context_override, collection_index=index, toggle=True)

#         if first_object.visible_get() != visibility:
#             bpy.ops.object.hide_collection(context_override, collection_index=index, toggle=True)

#     return collection
