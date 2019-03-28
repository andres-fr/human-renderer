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


# class DAZ_PT_Setup(bpy.types.Panel):
#     bl_label = "Setup"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "DAZ Runtime"



class MY_PANEL_PT_MyPanel(bpy.types.Panel):
    # bl_idname = "MY_PANEL_PT_MyPanel"
    bl_label = "Selection Manager"
    bl_space_type = "VIEW_3D" # 'PROPERTIES'
    bl_region_type = "UI" # 'WINDOW'
    # bl_context = "object"
    # bl_options = {'DEFAULT_CLOSED'}
    # bl_options = {'REGISTER', 'UNDO'}
    bl_category = "DAZ Runtime"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        """
        Draw UI elements into the panel’s header UI layout
        """
        layout = self.layout
        obj = context.object
        fn = lambda self, context: obj.select_set(state=True)
        self.append(fn)
        ###layout.prop(fn, text="quackkk")
        # layout.prop(obj, "select_set", text="")
        # bpy.ops.object.select_all(action="DESELECT")

    def draw(self, context):
        layout = self.layout

        obj = context.object
        row = layout.row()
        row.prop(obj, "hide_select")
        row.prop(obj, "hide_render")

        box = layout.box()
        box.label(text="Selection Tools")
        box.operator("object.select_all").action = 'TOGGLE'
        row = box.row()
        row.operator("object.select_all").action = 'INVERT'
        row.operator("object.select_random")



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
        :param menu_class: Class handle for the Blender GUI where the
           functionality can be triggered.
        :type menu_class: ``bpy.types.{Header, Panel, ...}

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

    To inspect the registered keymaps:
    ::

       wm = context.window_manager
       km_items = wm.keyconfigs.addon.keymaps[KEYMAP_NAME].keymap_items
       # km_items is a dict containing the op_name -> km binding.
       # To see the key and stroke_mode:
       km_item = km_items.values()[0]  # some item
       key, stroke = km_item.type, km_item.value
      # Default operator properties can be customized for a specific keymap:
       km_item.properties.<PROP> = 3.14  # <PROP> was defined in the Operator
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

           register_keymap(bpy.context, "D", "PRESS", MyOperator.bl_idname)

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

classes = [ObjectCursorArray, MY_PANEL_PT_MyPanel]
register_cl, unregister_cl = bpy.utils.register_classes_factory(classes)
kmm = KeymapManager()
omm = OperatorToMenuManager()

def register():
    """
    Main register function, called on startup by Blender
    """
    register_cl()
    omm.register(ObjectCursorArray, bpy.types.VIEW3D_MT_object)
    kmm.register(bpy.context, "D", "PRESS", ObjectCursorArray.bl_idname)


def unregister():
    """
    Main unregister function, called on shutdown by Blender
    """
    kmm.unregister()
    omm.unregister()
    unregister_cl()


if __name__ == "__main__":
    # This gets executed if calling `blender --python <THIS_FILE>.py`
    register()


print("[Add-on loaded]: ", bl_info["name"], "version", VERSION)
