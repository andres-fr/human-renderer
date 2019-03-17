
from mathutils import Vector
import bpy
C = bpy.context
D = bpy.data
# this doesn't work inside defs, see
# https://blender.stackexchange.com/questions/23943/operator-class-retrieval
# import bpy.ops as O

import makewalk

print(makewalk.bl_info)

# start blender from CLI with this script
# blender <OPTIONAL_BLENDER_FILE> --python <PYTHON_SCRIPT>

###############################################################################
### TUTORIAL
###############################################################################

# bpy.data important fields: objects, scenes, materials

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


###############################################################################
### MAIN ROUTINE
###############################################################################

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

