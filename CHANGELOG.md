# CHANGELOG
All notable changes to this project will be documented in this file.

* The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) where:
  - Versions adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`MAJOR.MINOR.PATCH`)
  - Dates are in `DD/MM/YYYY` format





## [[Unreleased](https://github.com/andres-fr/human-renderer/compare/0.1.0...HEAD)]

### Added
- 

## [0.1.0] - 27/02/2019

### Added
- Provided CI structure for testing, build, autodoc, and GH releases


## TODO:

At this point we have a satisfactory scene with a sequence being rendered reasonably fast within Blender
- Get proper specs for Mali data format, and integrate it into MakeWalk via Python parser (with JSON schema or similar).


Integrated workflow:
   0. See `blender --help` for some CLI interaction
   1. Render sequences in a headless way, from terminal. Using GPU as fast as possible (headless OpenGL rendering not possible yet? https://developer.blender.org/T54638)
   2. Store 3D-navigable sequences, then integrate into Qt? https://www.kdab.com/exporting-3d-content-qt-3d-blender/
   3. Editing of sequences within Python (interactively?)

