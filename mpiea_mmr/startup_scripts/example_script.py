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

SOME_BVH_PATH = mmr.blender_utils.resolve_path("data", "bvh_files",
                                               "cmu_motion_captures", "01",
                                               "01_06.bvh")

def import_makehuman(context, name, mhx2_abspath, xy_pos=(0, 0),
                     bvh_abspath=None):
    """
    """
    # make sure nothing else is selected before starting
    bpy.ops.object.select_all(action="DESELECT")
    # import  MHX2
    bpy.ops.import_scene.makehuman_mhx2(filepath=mhx2_abspath)
    context.object.name = name
    context.object.data.name = name
    # optionally apply BVH to it
    if bvh_abspath is not None:
        # Assumes context.object is a MHX2
        bpy.ops.mcp.load_and_retarget(filepath=bvh_abspath)



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
                        type=str, nargs="*", #  default=SOME_BVH_PATH,
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


    # TODO: some operator fails here because of poll. Check that...
    # # position the humans:
    # for i, xy_tuple in enumerate(zip(human_pos[::2], human_pos[1::2]), 1):
    #     import_makehuman(bpy.context, "Hooman_"+str(i),
    #                      args["mhx2_path"], xy_tuple, SOME_BVH_PATH) # args["bvh_path"]
    #     print("<<<", xy_tuple)

    # for x, y in args["human_positions"]:
    #     print(">>>>>>>>><", x, y)
    # PositionListValidator.validate_str(args["human_positions"])


    # animation config:
    bpy.context.scene.frame_start = args["sequence_startframe"]
    bpy.context.scene.frame_end = args["sequence_endframe"]
    if args["play_sequence"]:
        bpy.ops.screen.animation_play()



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Blender absorbs any error except for SystemExit ones.
        # This code makes Blender abort if anything goes wrong with the script.
        print("\n\nException of type", e.__class__.__name__)
        print(e)
        print("Aborting Blender because script failed...\n")
        raise SystemExit
