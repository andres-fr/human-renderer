# -*- coding:utf-8 -*-


"""
Utilities for interaction with Blender
"""


__author__ = "Andres FR"


import argparse
import sys
#
import bpy

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
# ## EYE ICON
# ## See https://blenderartists.org/t/show-hide-collection-blender-beta-2-80/1141768
# #############################################################################

def get_viewport_ordered_collections(context):
    def fn(c, out, addme):
        if addme:
            out.append(c)
        for c1 in c.children:
            out.append(c1)
        for c1 in c.children:
            fn(c1, out, False)
    collections = []
    fn(context.scene.collection, collections, True)
    return collections

def get_area_from_context(context, area_type):
    area = None
    for a in context.screen.areas:
        if a.type == area_type:
            area = a
            break
    return area

def set_collection_viewport_visibility(context, collection_name, visibility=True):
    collections = get_viewport_ordered_collections(context)

    collection = None
    index = 0
    for c in collections:
        if c.name == collection_name:
            collection = c
            break
        index += 1

    if collection is None:
        return

    first_object = None
    if len(collection.objects) > 0:
        first_object = collection.objects[0]

    try:
        bpy.ops.object.hide_collection(context, collection_index=index, toggle=True)

        if first_object.visible_get() != visibility:
            bpy.ops.object.hide_collection(context, collection_index=index, toggle=True)
    except:
        context_override = context.copy()
        context_override['area'] = get_area_from_context(context, 'VIEW_3D')

        bpy.ops.object.hide_collection(context_override, collection_index=index, toggle=True)

        if first_object.visible_get() != visibility:
            bpy.ops.object.hide_collection(context_override, collection_index=index, toggle=True)

    return collection


# #############################################################################
# ##
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

    def register(self, key, stroke_mode, op_name,
                 ctrl=True, shift=True, alt=False,
                 context=bpy.context):
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
# ##
# #############################################################################
