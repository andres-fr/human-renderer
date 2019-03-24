# CHANGELOG
All notable changes to this project will be documented in this file.

* The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) where:
  - Versions adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`MAJOR.MINOR.PATCH`)
  - Dates are in `DD/MM/YYYY` format





## [[Unreleased](https://github.com/andres-fr/human-renderer/compare/0.1.0...HEAD)]

### Added
- Scene builder script with sun, cam, lightcam, floor, human, textures and bvh sequence.
- converted script to an add-on with all infrastructure working [ONGOING]

## [0.1.0] - 27/02/2019

### Added
- Provided CI structure for testing, build, autodoc, and GH releases


## TODO:


- autodoc fails because no bpy. fix that (try using SPHINXBUILD   = ~/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/python/bin/sphinx-build # sphinx-build)

- rewrite docstrings in extended "rich-syntax" style


- once this is done, check if doing small changes to the package automatically updates upon blender start-up. If positive, we have a clean workflow.

- Then integrate all existing functionality of the script in a structured way. Check that all works on the CI

- probably a good idea to create a standard template for Blender. See https://github.com/osiriswrecks/blender-addon-template/blob/master/ui.py
also see https://blenderartists.org/t/code-template-for-blender-add-ons/682339



-----------------------------------------



- Get proper specs for Mali data format, and integrate it into MakeWalk via Python parser (with JSON schema or similar).


Integrated workflow:
   0. See `blender --help` for some CLI interaction
   1. Render sequences in a headless way, from terminal. Using GPU as fast as possible (headless OpenGL rendering not possible yet? https://developer.blender.org/T54638)
   
* TODO: add details about MH export: include skeleton, hide textures under clothes, low poly eyes, **T-SHAPE** (important), no shoes, units in meters, export as binary.

TODO: talk about bvh, the approach of MW, existing issues, and how to retarget.

