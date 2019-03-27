#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Init file for the add-on.

To install it, make sure Blender's Python is able to find it under
addon_utils.paths(), and that the Blender version matches to make it
installable.

Alternatively, run this init file as a script from Blender.
"""


# __author__ = "Andres FR"

# import bpy
# #
# # from . import blender_utils
# # from . import dance_scene as ds


# name = "mpiea_mmr"  # for packaging via setup.py
# VERSION = "0.1.2"  # automatically managed by bumpversion


# # required by blender plugins
# # (see https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo)
# bl_info = {
#     "name": "MPIEA MultiModalRenderer",
#     "author": "Andres FR",
#     "support": "TESTING",
#     "blender": (2, 80, 0),
#     "location": "View3D > Add > Mesh > Generate",
#     # "location": "View3D > Tools > MakeWalk",
#     "description": "Scene building and rendering of 3D video+audio sequences",
#     # "warning": "",
#     # 'wiki_url': "",
#     "category": "MPIEA"}



# # #############################################################################
# # ## UI
# # #############################################################################

# # class ObjectSelectPanel(bpy.types.Panel):
# #     bl_idname = "OBJECT_PT_select"
# #     bl_label = "Select"
# #     bl_space_type = 'PROPERTIES'
# #     bl_region_type = 'WINDOW'
# #     bl_context = "object"
# #     bl_options = {'DEFAULT_CLOSED'}

# #     @classmethod
# #     def poll(cls, context):
# #         return (context.object is not None)

# #     def draw_header(self, context):
# #         layout = self.layout
# #         obj = context.object
# #         layout.prop(obj, "select", text="")

# #     def draw(self, context):
# #         layout = self.layout

# #         obj = context.object
# #         row = layout.row()
# #         row.prop(obj, "hide_select")
# #         row.prop(obj, "hide_render")

# #         box = layout.box()
# #         box.label("Selection Tools")
# #         box.operator("object.select_all").action = 'TOGGLE'
# #         row = box.row()
# #         row.operator("object.select_all").action = 'INVERT'
# #         row.operator("object.select_random")

# # class ObjectCursorArray(bpy.types.Operator):
# #     """
# #     Object Cursor Array
# #     """
# #     bl_idname = "object.cursor_array"
# #     bl_label = "Cursor Array"
# #     bl_options = {'REGISTER', 'UNDO'}

# #     total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

# #     def execute(self, context):
# #         """
# #         """
# #         scene = context.scene
# #         cursor = scene.cursor_location
# #         obj = scene.objects.active

# #         for i in range(self.total):
# #             obj_new = obj.copy()
# #             scene.objects.link(obj_new)

# #             factor = i / self.total
# #             obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

# #         return {'FINISHED'}


# # def menu_func(self, context):
# #     """
# #     """
# #     self.layout.operator(ObjectCursorArray.bl_idname)

# # # store keymaps here to access after registration
# # addon_keymaps = []


# # def register():
# #     bpy.utils.register_class(ObjectCursorArray)
# #     bpy.types.VIEW3D_MT_object.append(menu_func)

# #     # handle the keymap
# #     wm = bpy.context.window_manager
# #     # Note that in background mode (no GUI available), keyconfigs are not available either,
# #     # so we have to check this to avoid nasty errors in background case.
# #     kc = wm.keyconfigs.addon
# #     if kc:
# #         km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
# #         kmi = km.keymap_items.new(ObjectCursorArray.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
# #         kmi.properties.total = 4
# #         addon_keymaps.append((km, kmi))

# # def unregister():
# #     # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
# #     # Can avoid strange issues like keymap still referring to operators already unregistered...
# #     # handle the keymap
# #     for km, kmi in addon_keymaps:
# #         km.keymap_items.remove(kmi)
# #     addon_keymaps.clear()

# #     bpy.utils.unregister_class(ObjectCursorArray)
# #     bpy.types.VIEW3D_MT_object.remove(menu_func)



# # #############################################################################
# # ## INITIALIZE/REGISTER
# # #############################################################################

# classes = [] # [ObjectSelectPanel]

# # classes = [
# #     # MCP_PT_Main,
# #     # MCP_PT_Utility,
# #     # utils.ErrorOperator
# # ]


# register, unregister = bpy.utils.register_classes_factory(classes)

# # def register():
# #     """
# #     """
# #     # my_module.initialize()  # some modules may require this
# #     for cls in classes:
# #         bpy.utils.register_class(cls)


# # def unregister():
# #     """
# #     """
# #     # my_module.uninitialize()
# #     for cls in classes:
# #         bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
#     # This gets executed if calling `blender --python <THIS_FILE>.py`
#     register()


# print("[Add-on loaded]: ", bl_info["name"], "version", VERSION)


#######
#######
#######
#######
#######

# # required by blender plugins
# # (see https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo)
# bl_info = {
#     "name": "MPIEA MultiModalRenderer",
#     "author": "Andres FR",
#     "support": "TESTING",
#     "blender": (2, 80, 0),
#     "location": "View3D > Add > Mesh > Generate",
#     # "location": "View3D > Tools > MakeWalk",
#     "description": "Scene building and rendering of 3D video+audio sequences",
#     # "warning": "",
#     # 'wiki_url': "",
#     "category": "MPIEA"}



bl_info = {
    "name": "Simple Add-on Template",
    "author": "Marco Mameli",
    # "location": "View3D > Add > Mesh > Generate",  # in 3D viewport, add->mesh-"Generate Point Cloud"
    "version": (1, 2, 3),
    "blender": (2, 80, 0),
    "description": "Starting point for new add-ons.",
    "category": "Add Mesh"
    }
import bpy
import bmesh
from bpy.types import Operator
from bpy.types import Panel

def add_pointcloud(self, context, naming):
    # qui scrivo i miei calcoli
    obj = context.active_object
    mycollection = bpy.data.collections.new("MyPointCloudCollection")
    bpy.context.scene.collection.children.link(mycollection)
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmFaces = []

    for face in bm.faces:
        faceLocation = face.calc_center_median()
        print(faceLocation)
        bmFaces.append(obj.matrix_world @ faceLocation) # la @ è il prodotto vettoriale
    for vertex in bm.verts:
        print(vertex.co)
        bmFaces.append(obj.matrix_world @ vertex.co)
    me = bpy.data.meshes.new(obj.name + 'Mesh' + naming)
    ob = bpy.data.objects.new(obj.name + '_PointCloud_' + naming, me)
    ob.show_name = True
    bpy.data.collections['MyPointCloudCollection'].objects.link(ob)
    me.from_pydata(bmFaces, [], [])
    me.update()
    ob.select_set(True)

class OBJECT_OT_add_PointCloud_with_noise(Operator):
    """ Create a Point Cloud """
    bl_idname = "object.add_pointcloud_with_noise"
    bl_label = "Add Mesh object that represent a Point Cloud"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context): # operazioni da eseguire
        # MAI METTERE IL CODICE QUI DENTRO DIRETTAMENTE
        print("Sono in with noise")
        add_pointcloud(self, context, "with_noise")

        return {'FINISHED'}

class OBJECT_OT_add_PointCloud(Operator):
    """ Create a Point Cloud """
    bl_idname = "object.add_mesh_pointcloud"
    bl_label = "Add Mesh object that represent a Point Cloud"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context): # operazioni da eseguire
        # MAI METTERE IL CODICE QUI DENTRO DIRETTAMENTE
        print("sono in no noise")
        add_pointcloud(self, context, "no_noise")

        return {'FINISHED'}

    def draw(self,context):
        layout = self.layout

        scene = context.scene

        layout.label(text="Pointcloud option")

        row = layout.row()
        row.prop(scene, "frame_star")

        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("object.add_pointcloud_with_noise")

# creo il bottone da aggiungere al menu di blender
def add_pointcloud_button(self, context):
    print(">>>>>>>>>>>>>>>>>>", self)
    self.layout.operator(OBJECT_OT_add_PointCloud.bl_idname, text="Generate Point Cloud",
                         icon='PLUGIN')

# creo il link al manuale
def add_pointcloud_manual_map():
        url_manual_prefix=""
        url_manual_mapping = (("bpy.ops.mesh.add_pointcloud", "editors/edview/object"),)
        return url_manual_prefix, url_manual_mapping

# Options panel for addon
class OBJECT_PT_add_PointCloud_properties(Panel):
    bl_label = "Properties Layout"
    bl_idname = "SCENE_PT_layout_PointCloud_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self,context):
        layout = self.layout

        scene = context.scene

        layout.label(text="Pointcloud option")

        row = layout.row()
        row.prop(scene, "frame_star")

        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")


classes = (OBJECT_OT_add_PointCloud, OBJECT_PT_add_PointCloud_properties, OBJECT_OT_add_PointCloud_with_noise)
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_manual_map(add_pointcloud_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_pointcloud_button)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.register_manual_map(add_pointcloud_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_pointcloud_button)


if __name__ == "__main__":
    register()




print("[Add-on loaded]: ", bl_info["name"], "version", bl_info["version"])
