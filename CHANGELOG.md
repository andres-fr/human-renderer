# CHANGELOG
All notable changes to this project will be documented in this file.

* The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) where:
  - Versions adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`MAJOR.MINOR.PATCH`)
  - Dates are in `DD/MM/YYYY` format





## [[Unreleased](https://github.com/andres-fr/human-renderer/compare/0.1.0...HEAD)]

### Added
- Added autodoc functionality to infrastructure.
- Design and implementation of add-on as an Operator+Panel API with functionality for scene building, custom UI and advanced editing [ONGOING]
- Iplementation of apps as startup scripts that use the implemented API [ONGOING]
- Added Travis CI [ONGOING]

## [0.1.0] - 27/02/2019

### Added
- Provided python structure for testing, build, autodoc, and GH releases


## TODO:

- Working on script reimplementation, scene building done (untested) up to floor. Remaining:
  * API coverage for makehuman interaction (clean and comprehensive please)
  * API coverage for "eye icon"
  * API coverage for multi-channel, multi-object sounds (multiple channels per object? children objects?)
  * API coverage for sequence processing, synchronization etc
  * API coverage for serialization (blender file, objects, sounds, also: Efficient storage of the retargeted human models!).
  * API coverage for advanced UI editing (own workspace etc)



- Design: ops can't be easily called at addon register time. Cleanest way is probably to
  1. Have all api-like functionality in the regular add-on
  2. Have apps as separate "standalone" scripts somewhere separated, to be called via `blender --python`
  3. The scripts should contain args, and all the args should also be accessible via UI, so that args can be corrected, and also have good default arguments so that a naked call to the script loads a reasonable scene.

- reimplement scene_builder script:
  * Plugin-neutral functionality goes to the blender utils as regular python
  * Ops that are potentially exposed to the user go as Operators
  * Modularize UI as a collection of Panels, hosting Operators
  * Plugin-specific scene building etc goes in the scene_builder.main function. It grabs Operators, utils and other specific functionality defined in the builder module itself.


- utest everything, codecov >90%?

- Travis script, from fresh OS to utest, coverage, autodoc. TEST ON AN OPEN REPO! (make dummy blender repo?):
  1. Download Blender 2.80 into home, and set .bashrc env variable so `blender` command works
  2. Run script that checks Blender up: py version, existence of folders... all assumptions must be represented and needed info gathered
  2. Install Python3-DEV (matching version) and copy the python include into blender. Also install other apt packages
  3. Install pip for blender and pip install requirements
  4. Pull the add-on repo (automatic?) and create symlinks on the addon folder, for the addon and utest.
  5. All should work at this point? MAKE SURE that if a CI script "fails", Blender propagates the exception.

Regarding OPEN REPO probably a good idea to create a standard template for Blender. See https://github.com/osiriswrecks/blender-addon-template/blob/master/ui.py
also see https://blenderartists.org/t/code-template-for-blender-add-ons/682339


- insert sound sources in scene
- Get proper specs for Mali data format, and integrate it into MakeWalk via Python parser (with JSON schema or similar).
- Make Blender "standalone": define proper UI to work on maximized 3d view only?
  * add panel (or pop-up) with "tips" and any useful info for the user
  

-----------------------------------------


* Render sequences in a headless way, from terminal. Using GPU as fast as possible (headless OpenGL rendering not possible yet? https://developer.blender.org/T54638)
   
* add details about MH export: include skeleton, hide textures under clothes, low poly eyes, **T-SHAPE** (important), no shoes, units in meters, export as binary.

TODO: talk about bvh, the approach of MW, existing issues, and how to retarget.


* Proper usage of poll in UI (operators, panels).


* Advanced UI example: `2.80/scripts/startup/bl_ui/space_view3d.py`
