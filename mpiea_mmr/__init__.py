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
    "location": "View3D > Add > Mesh > Generate",
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
        :param menu_class: Class handle for the Blender UI element where the
           functionality can be triggered.
        :type menu_class: ``bpy.types.{Header, Panel, ...}
        :param bool remove_instead_of_append: If false, element is added
           (usually at ``register`` time). If true, element is removed
           (usually at ``unregister`` time).
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
    currently registered.
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

           register_keymap(bpycontext, "D", "PRESS", MyOperator.bl_idname)

        :param bpy.types.Context context: A context like ``bpy.context``.
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


# #############################################################################
# ## INITIALIZE/REGISTER
# #############################################################################

classes = [ObjectCursorArray]
register_cl, unregister_cl = bpy.utils.register_classes_factory(classes)
kmm = KeymapManager()
omm = OperatorToMenuManager()

def register():
    """
    """
    register_cl()
    omm.register(ObjectCursorArray, bpy.types.VIEW3D_MT_object)
    kmm.register(bpy.context, "D", "PRESS", ObjectCursorArray.bl_idname)


def unregister():
    """
    """
    kmm.unregister()
    omm.unregister()
    unregister_cl()

# classes = [
#     # MCP_PT_Main,
#     # MCP_PT_Utility,
#     # utils.ErrorOperator
# ]



if __name__ == "__main__":
    # This gets executed if calling `blender --python <THIS_FILE>.py`
    register()


print("[Add-on loaded]: ", bl_info["name"], "version", VERSION)







#######
#######
#######
#######
#######




# bl_info = {
#     "name": "Simple Add-on Template",
#     "author": "Marco Mameli",
#     # "location": "View3D > Add > Mesh > Generate",  # in 3D viewport, add->mesh-"Generate Point Cloud"
#     "version": (1, 2, 3),
#     "blender": (2, 80, 0),
#     "description": "Starting point for new add-ons.",
#     "category": "Add Mesh"
#     }
# import bpy
# import bmesh
# from bpy.types import Operator
# from bpy.types import Panel

# def add_pointcloud(self, context, naming):
#     # qui scrivo i miei calcoli
#     obj = context.active_object
#     mycollection = bpy.data.collections.new("MyPointCloudCollection")
#     bpy.context.scene.collection.children.link(mycollection)
#     me = obj.data
#     bm = bmesh.new()
#     bm.from_mesh(me)
#     bmFaces = []

#     for face in bm.faces:
#         faceLocation = face.calc_center_median()
#         print(faceLocation)
#         bmFaces.append(obj.matrix_world @ faceLocation) # la @ è il prodotto vettoriale
#     for vertex in bm.verts:
#         print(vertex.co)
#         bmFaces.append(obj.matrix_world @ vertex.co)
#     me = bpy.data.meshes.new(obj.name + 'Mesh' + naming)
#     ob = bpy.data.objects.new(obj.name + '_PointCloud_' + naming, me)
#     ob.show_name = True
#     bpy.data.collections['MyPointCloudCollection'].objects.link(ob)
#     me.from_pydata(bmFaces, [], [])
#     me.update()
#     ob.select_set(True)

# class OBJECT_OT_add_PointCloud_with_noise(Operator):
#     """ Create a Point Cloud """
#     bl_idname = "object.add_pointcloud_with_noise"
#     bl_label = "Add Mesh object that represent a Point Cloud"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self,context): # operazioni da eseguire
#         # MAI METTERE IL CODICE QUI DENTRO DIRETTAMENTE
#         print("Sono in with noise")
#         add_pointcloud(self, context, "with_noise")

#         return {'FINISHED'}

# class OBJECT_OT_add_PointCloud(Operator):
#     """ Create a Point Cloud """
#     bl_idname = "object.add_mesh_pointcloud"
#     bl_label = "Add Mesh object that represent a Point Cloud"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self,context): # operazioni da eseguire
#         # MAI METTERE IL CODICE QUI DENTRO DIRETTAMENTE
#         print("sono in no noise")
#         add_pointcloud(self, context, "no_noise")

#         return {'FINISHED'}

#     def draw(self,context):
#         layout = self.layout

#         scene = context.scene

#         layout.label(text="Pointcloud option")

#         row = layout.row()
#         row.prop(scene, "frame_star")

#         layout.label(text="Big Button:")
#         row = layout.row()
#         row.scale_y = 1.0
#         row.operator("object.add_pointcloud_with_noise")

# # creo il bottone da aggiungere al menu di blender
# def add_pointcloud_button(self, context):
#     print(">>>>>>>>>>>>>>>>>>", self)
#     self.layout.operator(OBJECT_OT_add_PointCloud.bl_idname, text="Generate Point Cloud",
#                          icon='PLUGIN')

# # creo il link al manuale
# def add_pointcloud_manual_map():
#         url_manual_prefix=""
#         url_manual_mapping = (("bpy.ops.mesh.add_pointcloud", "editors/edview/object"),)
#         return url_manual_prefix, url_manual_mapping

# # Options panel for addon
# class OBJECT_PT_add_PointCloud_properties(Panel):
#     bl_label = "Properties Layout"
#     bl_idname = "SCENE_PT_layout_PointCloud_properties"
#     bl_space_type = 'PROPERTIES'
#     bl_region_type = 'WINDOW'
#     bl_context = "scene"

#     def draw(self,context):
#         layout = self.layout

#         scene = context.scene

#         layout.label(text="Pointcloud option")

#         row = layout.row()
#         row.prop(scene, "frame_star")

#         layout.label(text="Big Button:")
#         row = layout.row()
#         row.scale_y = 3.0
#         row.operator("render.render")


# classes = (OBJECT_OT_add_PointCloud, OBJECT_PT_add_PointCloud_properties, OBJECT_OT_add_PointCloud_with_noise)
# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)
#     bpy.utils.register_manual_map(add_pointcloud_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.append(add_pointcloud_button)


# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls)
#     bpy.utils.register_manual_map(add_pointcloud_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.remove(add_pointcloud_button)


# if __name__ == "__main__":
#     register()




# print("[Add-on loaded]: ", bl_info["name"], "version", bl_info["version"])
