# -*- coding:utf-8 -*-


"""
Example app that uses the functionality of the ``MPIEA MultiModalRenderer``
add-on for Blender.

1. Make sure the add-on is installed and working
2. Run script with ``blender --python <SCRIPT_PATH> -- <SCRIPT_ARGS...>``
"""


__author__ = "Andres FR"


# import os

# import argparse
# import sys
# from math import radians  # degrees
# #
# from mathutils import Vector, Euler  # mathutils is a blender package
# import bpy
# #
# from . import __path__ as PACKAGE_ROOT_PATH

# import json
# import jsonschema

#
import bpy
import aud  # audaspace
import mpiea_mmr as mmr


# #############################################################################
# ## GLOBALS/HELPERS
# #############################################################################

# class PositionListValidator():
#     """
#     This class defines the JSON schema for a list of numbers like
#     ``[(x1, y1), (x2, y2), ...]``, and provides a method to validate input
#     strings.
#     """

#     SCHEMA = {"title": "XY_position_schema",
#               "type": "array",
#               "description": "array of zero or more elements",
#               "items": {
#                   "type": "array",
#                   "description": "array of two numbers",
#                   "minItems": 2, "maxItems": 2,
#                   "items": [{"type": "number", "description": "x-position"},
#                             {"type": "number", "description": "y-position"}]
#                        }
#               }

#     @classmethod
#     def validate_str(clss, data):
#         """
#         Converts the given data to JSON and then validates it against
#         self.SCHEMA.

#         :param data: The input to be converted to JSON and validated
#         :type data: str
#         :returns: None
#         :raises Exception: If the input data is illegal or invalid.
#         """
#         j = json.loads(data)
#         jsonschema.validate(j, clss.SCHEMA)

TPOSE_AFRICAN_PATH = mmr.blender_utils.resolve_path("data", "makehuman_models",
                                                    "exported",
                                                    "tpose_african.mhx2")




BVH_MALI_SNIPPET = mmr.blender_utils.resolve_path("data", "mali_dataset",
                                                  "mocap",
                                                  "SAG_D1-003_(snippet)_slate03_2-35-44.759.bvh")
                                                  # "SAG_D1-003_(snippet)_slate01_2-23-29.701.bvh")


SOME_BVH_PATH = mmr.blender_utils.resolve_path("data", "bvh_files",
                                               "cmu_motion_captures", "01",
                                               "01_06.bvh")

WAVPATH_1 = mmr.blender_utils.resolve_path("data", "mali_dataset",
                                           "audio", "SAG_D1_10_Voc-1.wav")

WAVPATH_2 = mmr.blender_utils.resolve_path("data", "mali_dataset",
                                           "audio", "SAG_D1_10_M-Jem-2.wav")



def import_makehuman(context, name, mhx2_abspath, xy_pos=(0, 0),
                     bvh_abspath=None):
    """
    This is not in the library because it directly uses the MHX2 plugin.

    TODO: maybe to make this load quicker, load the assets into a class
    at beginning and let the class manage scene interaction via factories
    etc. Mimick the 'select hierarchy' -> copy functionality.
    """
    # make sure nothing else is selected before starting
    ### bpy.ops.object.select_all(action="DESELECT")
    # import  MHX2
    bpy.ops.import_scene.makehuman_mhx2(filepath=mhx2_abspath)
    human = context.object
    human.location = (xy_pos) + (0.07,)  # elevate a little
    context.object.name = name
    context.object.data.name = name
    # optionally apply BVH to it
    frame_range = None  # if BVH set, this is a Vector(start, end)
    if bvh_abspath is not None:
        # Assumes context.object is a MHX2
        bpy.ops.mcp.load_and_retarget(filepath=bvh_abspath)
        frame_range = human.animation_data.action.frame_range
    return human, frame_range


def play_some_sounds():
    """
    https://docs.blender.org/api/blender2.8/aud.html?highlight=audio
    """
    device = aud.Device()
    snd1 = aud.Sound(WAVPATH_1)
    snd2 = aud.Sound(WAVPATH_2)
    #
    handle1  = device.play(snd1)
    handle1.location = (-1, 0, 0)
    #
    handle2  = device.play(snd2)
    handle2.location = (1, 0, 0)
    # position not relative to listener?
    handle1.relative = False
    handle2.relative = False
    # TODO: set this to the viewer position interactively
    device.listener_location = 0, 0, 0
    # device.listener_orientation = 0, 0, 0, 0  # quaternion

# #############################################################################
# ## MAIN ROUTINE
# #############################################################################

def parse_args():
    """
    This function creates, configures and uses an ``ArgumentParserForBlender``
    to parse the script arguments given after the double-dash in a call like
    ``blender --python <SCRIPT_PATH> -- <SCRIPT_ARGS...>.

    :returns: A dictionary of ``'parameter_name': parameter_value`` pairs.
    :raises SystemExit: If the argument parser encounters any problem.
    """
    parser = mmr.blender_utils.ArgumentParserForBlender()
    parser.add_argument("-b", "--create_basic_scene",
                        action="store_true",
                        help="Cleans initial scene and creates a basic one.")
    parser.add_argument("-f", "--view3d_fullscreen",
                        action="store_true",
                        help="Sets the View3D to fullscreen mode.")

    parser.add_argument("-P", "--play_sequence",
                        action="store_true",
                        help="Triggers play button upon start.")
    parser.add_argument("-S", "--sequence_startframe",
                        type=int, default=0,
                        help="Non-negative, sequence starts at this frame")
    parser.add_argument("-E", "--sequence_endframe",
                        type=int, default=250,
                        help="Sequence ends here (can't be less than start).")

    parser.add_argument("-p", "--human_positions",
                        type=float, nargs="*",
                        help="A list of 'x1 y1 x2 y2 ...' position pairs \
                        where humans will be generated.")
    parser.add_argument("-H", "--mhx2_path",
                        type=str, default=TPOSE_AFRICAN_PATH,
                        help="path to the MHX2 human model to load")
    parser.add_argument("-B", "--bvh_path",
                        type=str, nargs="*",
                        help="paths to the BVH files to load (one per given \
                        xy position pair).")


    args = parser.parse_args()
    return vars(args)


def main():
    """
    """
    # parse CLI arguments
    try:
        args = parse_args()
    except SystemExit as se:
        print(se)  # Print the cause of error before crashing
        raise se  # This makes blender crash
    # check CLI arguments consistency
    human_pos = args["human_positions"]
    assert (len(human_pos) % 2) == 0,\
        "Number of human positions 'x1 y1 x2 y2 ...' must be pair!"
    assert 0 <= args["sequence_startframe"] <= args["sequence_endframe"],\
        "Required: 0 <= start_frame <= end_frame"
    # optionally replace original scene with basic scene
    if args["create_basic_scene"]:
        for a in bpy.data.screens["Layout"].areas:
            if a.type == "VIEW_3D":
                bpy.ops.scene.clean_purge_and_create_basic_scene()
    #
    if args["view3d_fullscreen"]:
        bpy.ops.screen.maximize_view_3d()


    # position the humans:
    humans = []
    mocap_initframe = 0 # args["sequence_startframe"]
    mocap_endframe = 0 # args["sequence_endframe"]
    for i, xy_tuple in enumerate(zip(human_pos[::2], human_pos[1::2]), 1):
        bvh = BVH_MALI_SNIPPET if i == 1 else None
        h, fr = import_makehuman(bpy.context, "hooman_"+str(i),
                                 args["mhx2_path"], xy_tuple, bvh)
        if fr is not None:
            beg, end = fr
            mocap_initframe = min(mocap_initframe, beg)
            mocap_endframe = max(mocap_endframe, end)
        humans.append(h)



    ### play_some_sounds()

    # animation config:
    bpy.context.scene.frame_start = mocap_initframe # args["sequence_startframe"]
    bpy.context.scene.frame_end = mocap_endframe # args["sequence_endframe"]
    # bpy.context.scene.McpStartFrame = args["sequence_startframe"]
    # bpy.context.scene.McpEndFrame = args["sequence_endframe"]


    if args["play_sequence"]:
        bpy.ops.screen.animation_play()



if __name__ == "__main__":
    ### main()
    try:
        main()
    except Exception as e:
        # Blender absorbs any error except for SystemExit ones.
        # This code makes Blender abort if anything goes wrong with the script.
        print("\n\nException of type", e.__class__.__name__)
        print(e)
        print("Aborting Blender because script failed...\n")
        raise SystemExit




# TODO:
# 1. fix human thing (see above) try doing interactively and then from script. DONE
# * mocap only loading 158?? This has to do with frame_range: https://blender.stackexchange.com/questions/27889/how-to-find-number-of-animated-frames-in-a-scene-via-python
#   it seems ok, the retargetting compresses the info to the available fps

# 2. add music at given position. first in the script, then create an operator
#   -> it is possible to position the music using audaspace. TODO: position relative to view matrix
#   -> it is possible to load a stripe and then adjust from the video editor, but this is not audaspace? try to merge both...
#
# 3. add video?
# 3.load MPIEA human and music, show how to sync/find cues:
#        it is possible to sync audio and mocap with the video and nonlinear anim. editors

# 4. add required






#       >>>>> 2 1 250 1 1581      # if set becomes 2 0 0 1 1581
#        >>>>> 3 0 5000 10 1581  # if set becomes 3 0 0 10 1581






# import matplotlib.pyplot as plt
# import multiprocessing as mp
# import numpy


# def worker(q):
#     fig=plt.figure()
#     ax=fig.add_subplot(111)
#     ln, = ax.plot([], [])
#     fig.canvas.draw()   # draw and show it
#     plt.show(block=False)
#     i = 0
#     while True:
#         obj = q.get()
#         n = obj + 0
#         print("sub : got:", n)
#         lnx, lny = ln.get_xdata(), ln.get_ydata()
#         ln.set_xdata(numpy.append(lnx, i))
#         ln.set_ydata(numpy.append(lny, n))
#         ax.relim()
#         ax.autoscale_view(True,True,True)
#         fig.canvas.draw()
#         i += 1


# queue = mp.Queue()
# p = mp.Process(target=worker, args=(queue,))
# p.start()


# # queue.put(C.scene.frame_current)
