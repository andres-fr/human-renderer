# -*- coding:utf-8 -*-


"""
Utilities for interaction with Blender
"""


__author__ = "Andres FR"


import argparse
import sys


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
        :param argv: Expected to be sys.argv (or alike).
        :returns: The argv sublist after the first ``'--'`` element (if
           present, otherwise returns an empty list).
        :type argv: list of str
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
