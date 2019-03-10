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

- find the specs for the "default" HM skeleton format, and a Python parser (with JSON schema or similar).
- find Python functionality for setting an arbitrary skeleton pose and test on blender console



* we have good intuitition about BHV, its sources and the way MH and Blender import it. For poses and sequences
* Same goes for the generation and export of MHX2 poses
* we just got to know makewalk and probably installed it OK

1. Flexible MHX2-BHV workflow:
   1. Find out how to render bare BHV sequences in blender, and export something like a video with minimal aesthetics
   2. Render same sequence but with a human from MH: Use makewalk?

2. Integrated workflow:
   1. Render sequences in a headless way, from terminal. Using GPU as fast as possible
   2. Store 3D-navigable sequences, then integrate into Qt?
