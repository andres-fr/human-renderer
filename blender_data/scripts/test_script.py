
from mathutils import Vector
import bpy
C = bpy.context
D = bpy.data
# this doesn't work inside defs, see
# https://blender.stackexchange.com/questions/23943/operator-class-retrieval
# import bpy.ops as O



# start blender from CLI with this script
# blender <OPTIONAL_BLENDER_FILE> --python <PYTHON_SCRIPT>

###############################################################################
### TUTORIAL
###############################################################################

# bpy.data important fields: objects, scenes, materials
# top-level data containers are so called ID data-blocks. These include Scene,
# Group, Object, Mesh, Screen, World, Armature, Image and Texture, and get
# IDs are the only types that can be serialized in the .blend file.
# e.g. run D.meshes.keys() to see the current meshes.


# hovering over buttons shows the command they relate to. e.g.
# bpy.data.objects["Cube"].location[0]
# Also pressing Ctrl-C while hovering copies command to the clipboard

# add/remove data: use methods of data collections
# mesh = bpy.data.meshes.new(name="MyMesh")
# bpy.data.meshes.remove(mesh)

# custom properties: are saved in the blender files and must be of type
# int,float,string (or arrays of), and dicts of type {str: int/float/str}

# opposed to global operations, the CONTEXT corresponds to active/visible
# elements. It is mainly read-only, can only be modified through the API
# C.scene.objects.active = obj  # instead of bpy.context.object = obj
# If you are writing a user tool normally you want to use the bpy.context since
# the user normally expects the tool to operate on what they have selected.
# For automation you are more likely to use bpy.data since you want to be able
# to access specific data and manipulate it, no matter what the user currently
# has the view set at.

# Operators are tools generally accessed by the user from buttons, menu items
# or key shortcuts. See help-> operator cheat sheet. Many operators are
# constrained to specific context. The best way to check this from Python is:
#     if bpy.ops.view3d.render_border.poll():
#         bpy.ops.view3d.render_border()
# **NOTE: operators are tricky to work with, see for more details:
#         https://docs.blender.org/api/blender2.8/info_gotcha.html

# reload script without reloading blender:
#    import myscript
#    import importlib
#    importlib.reload(myscript)
#    myscript.main()

# use a different Python (different approaches)
# see docs.blender.org/api/blender2.8/info_tips_and_tricks.html
# section drop-into-a-python-interpreter-in-your-script
# * remove the blender/python directory, blender will default to your own
#   (versions must match)
# * append context to sys.path
# * use blender as module (requires rebuilding Blender)


# drawing during script: DISCOURAGED but possible. See
# https://docs.blender.org/api/blender2.8/info_gotcha.html

# Edit mode: it is important to note that edit mode has its own data which is
# only written back when exiting edit-mode. The easiest way around this is to
# have the script check/report edit mode and execute only outside edit mode.
#    py.ops.object.mode_set(mode="EDIT")
#    modes supported by cube: "OBJECT", "EDIT", "SCULPT", "VERTEX_PAINT",
#                             "WEIGHT_PAINT", "TEXTURE_PAINT".
# References have to be reassigned after entering and exiting edit mode:
#    mesh = bpy.context.active_object.data
#    polygons = mesh.polygons
#    bpy.ops.object.mode_set(mode='EDIT')
#    # ...
#    bpy.ops.object.mode_set(mode='OBJECT')
#    # polygons have been re-allocated
#    polygons = mesh.polygons
#    print(polygons)

# bones, pose, armature: EditBones (in edit mode) and Bones (otherwise) can
# be accessed and manipulated with the API. Just make sure to clearly separate
# the code in edit mode from the other modes. PoseBone instances contain
# strictly speaking the armature status rather than bones. Used for animations.
# see https://docs.blender.org/api/blender2.8/info_gotcha.html

# data names: may be altered if empty string, to long, already existing...
# Its better practice not to reference objects by names at all, rather work
# with the references in datastructures.

# Library collisions: try to avoid them. Still, there is a mechanism to
# differentiate between local and library data:
#    # typical name lookup, could be local or library.
#    obj = bpy.data.objects["my_obj"]
#    # library object name look up using a pair where the second argument
#    # is the library path matching bpy.types.Library.filepath
#    obj = bpy.data.objects["my_obj", "//my_lib.blend"]
#    # local object name look up using a pair
#    # where the second argument excludes library data from being returned.
#    obj = bpy.data.objects["my_obj", None]
#    # both the examples above also works for 'get'
#    obj = bpy.data.objects.get(("my_obj", None))


# Multithreading: So far, no work towards thread-safety for python scripts
# has been done, so better avoid. And in any case, make sure the threads
# finish before the script. Enforce that by always using join()

# Undo/redo: invalidates all bpy.types.ID instances (Object, Scene, Mesh,
# Lamp… etc). Try it: cube = C.objects["Cube"] gets invalidated after undo.
# Avoid interactive usage while holding references!

# Remove: The API allows for profilactic deleting of non-used data via
# the remove() method. Deleted references throw exception instead of crashing.
#    mesh = bpy.data.meshes.new(name="MyMesh")
#    bpy.data.meshes.remove(mesh)

# sys.exit() may exit Blender and look like a crash! try to avoid. Some
# libraries, like argparse, sys.exit when invalid arguments. Workaround
# see https://docs.blender.org/api/blender2.8/info_gotcha.html


# Mathutils: support for vectors, quaternion, eulers, matrix and color types.
# all operations that apply on vectors can also apply on collections like lists
# tuples etc. Example of matrix*vector multiplication:
#     bpy.context.object.matrix_world * bpy.context.object.data.verts[0].co
# the copy() method drops the reference, useful to avoid side effects:
#    location_cp = bpy.context.object.location.copy()

# Animations: An important concept is "KEYFRAMES". An object has a collection
# of per-frame states, and interpolates between them. Small sample:
#    obj = bpy.context.object
#    obj.location[2] = 0.0
#    obj.keyframe_insert(data_path="location", frame=10.0, index=2)
#    obj.location[2] = 1.0
#    obj.keyframe_insert(data_path="location", frame=20.0, index=2)
# Each ID block may have its own .animation_data field.

# Extending Blender UI in scripts is discouraged, because the reference to the
# defined class gets lost. Best practice is to extend via modules (e.g. addons)


###############################################################################
### HELPERS
###############################################################################

def update_scene():
    """
    Sometimes changes don't show up due to lazy evaluation. This function
    triggers scene update and recalculation of all changes.
    """
    C.scene.update()

def set_debug_mode(debug=True):
    """
    Set debug mode to the given value (expected boolean). Iff true, debug.
    """
    bpy.app.debug_wm = value

def run_python_script(filepath):
    """
    Run python script FROM BLENDER CONSOLE.
    """
    with open(filepath, "r") as f:
        exec(compile(f.read(), filepath, "exec"))

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

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

def delete_selected():
    bpy.ops.object.delete()



def register_class(op_clss):
    """
    Call this once to let Blender know about the given class.
    Parameter: a class (not an instance) of type bpy.types.
    Operator, Panel...
    """
    bpy.utils.register_class(op_clss)

def unregister_class(op_clss):
    """
    Call this once to let Blender forget about the given class.
    Parameter: a class (not an instance) of type bpy.types.
    Operator, Panel...
    """
    bpy.utils.unregister_class(op_clss)


###############################################################################
### UI
###############################################################################

class SimpleOperator(bpy.types.Operator):
    """
    A simple Blender operator, to be registered with bpy.utils.register_class.
    The class members with the bl_ prefix are documented in the API reference.
    """
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.scene.objects:
            print(ob)
        return {'FINISHED'}


class HelloWorldPanel(bpy.types.Panel):
    """
    Creates a Panel in the Properties->Object window.
    The class members with the bl_ prefix are documented in the API reference.
    """
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        """
        This method is automatically called by Blender, and refreshed upon any
        changes.
        """
        layout = self.layout

        obj = context.object
        # rows can be simple labels, static or dynamic
        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')
        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        # prompt user to edit a specific property
        row = layout.row()
        row.prop(obj, "name")
        # user can trigger operators too
        row = layout.row()
        row.operator("mesh.primitive_cube_add")





###############################################################################
### MAIN ROUTINE
###############################################################################


import argparse
import sys

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

parser = ArgumentParserForBlender()


parser.add_argument("-q", "--quack",
                    action="store_true",
                    help="Quacks foo times if activated.")
parser.add_argument("-b", "--bar", type=int, default=10,
                    help="Number of desired quacks")
args = parser.parse_args()
QUACK = args.quack
BAR = args.bar

if QUACK:
    print("QUACK "*BAR)



register_class(HelloWorldPanel)

#d = C.collection.objects
#cube = d["Cube"]
#cube.location = Vector((0.0, 0.0, 4.0))
#cube.dimensions = Vector((1.0, 1.0, 3.0))
#print(">>>>", cube.name)






deselect_all()
select_by_name("Cube", "Camera", "Light")
deselect_by_name("Cube")
# print(">>>>>>>>>>", bpy.ops.object)
# delete_selected()

