[![Build Status](https://travis-ci.com/andres-fr/human-renderer.svg?token=cUXVqzsqAP4ZpSpN77Kh&branch=master)](https://travis-ci.com/andres-fr/human-renderer)

# human-renderer


### run all tests:

```
# with coverage:
python ci_scripts/utest_with_coverage.py -n humanrenderer -p 99.9
# without coverage:
python -m unittest discover -s utest -t . -p "*_test.py" -v
```

### Bump version:

Regular work is performed on the `dev` branch. After a milestone commit, merge into `master` and tag it before pushing with:

```
bump2version {major | minor | patch}
```

And then a push will automatically trigger the tagged release.

### Build package:

```
python setup.py clean --all
rm -r *.egg-info
python setup.py sdist bdist_wheel
```


### Build docs:


```
./ci_scripts/make_sphinx_docs.sh humanrenderer "Andres Fernandez Rodriguez"
```


### Branching:

Travis builds get triggered on `master` and tagged builds only. Regular work can be done on a `dev` branch:

```
# create branch right after a commit:
git checkout -b dev
# work normally on it...
...
# track the new branch if you want to implicitly push to it:
git push -u origin dev # the first time, then `git push`

# once a milestone is reached, merge into master:
xx
```



## Setup:



### Blender

Install as follows:

1. Download from `https://www.blender.org/download/`
2. Unpack into `<BLENDERPATH>` (e.g. `~/opt/`)
3. Add to PATH in `.bashrc` or `.profile` (e.g. `export PATH=$HOME/opt/blender-2.79b-linux-glibc219-x86_64:$PATH`)
4. now running `blender` will work on any terminal with that environment.

### Makehuman

Install

```
sudo add-apt-repository ppa:makehuman-official/makehuman-11x
sudo apt update
sudo apt install makehuman
# run with makehuman, or (for specific python interpreter):
python2 /usr/share/makehuman/makehuman.py
```

Also for best compatibility with render, models should be exported in [MHX2 format](https://thomasmakehuman.wordpress.com/2014/10/09/mhx2/). This is also not straightforward: Download and unpack this software: `https://www.dropbox.com/s/jrscejsv9uk8ch5/mhx2_stable_026.zip` (this repo holds a copy in `legacy`). Further instructions are in the `README` file inside:


```
# copy the export routine into the makehuman plugins folder
sudo cp -r 9_export_mhx2/ /usr/share/makehuman/plugins/

# Copy the import rutine into the blender addons folder
cp -r import_runtime_mhx2/ ~/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib


# Open Blender and enable the MHX2 importer. Select File > User Preferences. In the window that opens, select the Addons tab and then the MakeHuman category. Enable MakeHuman: Import-Runtime: MakeHuman eXchange 2 (.mhx2), and Save User Settings.

# In the File tab, enable Auto Run Python Scripts and Save User Settings.

# Select File > Import > MakeHuman (.mhx2), and navigate to the mhx2 file exported from MakeHuman.

# By default, the exported character is imported into Blender as it appears in MakeHuman. However, if Override Export Data is selected, the character will be rebuilt according to the options that appear.
```

Also note: at the moment of writing, there is a bug in the official version `1.1.1`, which is incompatible with `numpy>1.12` (see [this post](http://www.makehumancommunity.org/forum/viewtopic.php?p=44716#p44716)) and throws an exception when trying to export a model. For this reason, and because MH runs on Python2, it is convenient to create a virtual environment just for MH usage:

```
conda update -n base -c defaults conda
conda create -n makehuman_env python=2.7 anaconda
conda activate makehuman_env
conda install pyopengl
conda install pyqt=4
conda install numpy=1.12
```

Still, this didn't work because a newer version was installed with `pip --user`, and this has precedence in the `sys.path` list, so the newer version was still loading (this can be checked with `import numpy as np; np.__version__; np.__file__`). Removing the `pip` installation worked:

1. Open `makehuman` in the virtual environment
2. Create a model for a human, select the `Default` skeleton under `Pose/Animate`.
3. Save and export as `MHX2` format.
4. Import in blender as described. When importing the `MHX2` human model, it will appear whithout textures (all white), but this is normal behaviour for the edit mode. Textures will be included in render mode.


# EXPERIMENTS

### Experiments with the Python console (see https://docs.blender.org/manual/en/latest/editors/python_console.html):


(Blender Python API: `https://docs.blender.org/api/2.79b/`)


https://docs.blender.org/api/2.78a/bpy.types.Object.html#bpy.types.Object.pose


https://docs.blender.org/api/2.78a/bpy.types.Pose.html




```
py.data.objects.keys()
bpy.data.objects["Testmodel"].pose.bones

```


## Pose serialization


### 1. BVH
The [BVH](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html) (copy of the link stored under `makehuman_data/BVH_format_explanation.html`) is a format for serialization of skeleton poses. It allows different structures, and the specification of sequences. It is a standard for motion capture compatible with MH, Blender and other editors.

Saved models (`.mhm`) include a line beginning with the `pose` keyword, pointing to the corresponding BVH (built-in poses are in `/usr/share/makehuman/data/poses/`). An example of such `.bvh` is stored under `makehuman_data/poses`.

[This link](https://sites.google.com/a/cgspeed.com/cgspeed/motion-capture/cmu-bvh-conversion) also points to thousands of BVH motion captures (small subset copied to this repo). Importing and playing them in Blender works out-of-the-box.

### 2. MHX2

Makehuman features different kinds of skeletons, the "Default" being the most detailled one. The file `/usr/share/makehuman/data/rigs/default.mhskel` contains the default skeleton definition (a copy is stored in this repo). Models exported as `.mhx2` include a `"skeleton"` entry, that implements the schema defined in `default.mhskel`. It provides the following entries for each bone: `name, parent, head_xyz, parent_xyz, roll_coeff`. Note the following:
    * This file can become very large due to the inefficient storage of the `vertices` information. Saving it as binary helps.
    * The XYZ system in Blender is `(right, deep, upwards)` (see [here](http://www.makehumancommunity.org/forum/viewtopic.php?p=35265&sid=4593dc12911e0b45b9f0342f6a4828d1#p35265)). **Probably** the 3-element vectors for head and tail stand for `(right, upwards, front)`, given `def zup(co): return Vector((co[0], -co[2], co[1]))` defined in `import_rutine_mhx2/utils.py` and used in `importer.py -> buildSkeleton`. I couldn't find any doc to confirm this, experiments will do.
    * It is unclear whether this format stores sequences


Load mhx2 into blender:

```
bpy.ops.import_scene.makehuman_mhx2(filepath="~/Desktop/myfile.mhx2")
bpy.ops.import_scene.makehuman_mhx2(filepath="~/github-work/human-renderer/makehuman_data/exported_models/testmodel.mhx2")
```





Related MH files:
  * `/usr/share/makehuman/plugins/3_libraries_skeleton/skeletonlibrary.py`
  * `/usr/share/makehuman/shared/skeleton.py`. The `Bone` class is the node of a tree, and has interesting methods like `getMatrix, get_roll_to, copy_normal...`. Docstring:

```
General skeleton, rig or armature class.
A skeleton is a hierarchic structure of bones, defined between a head and tail
joint position. Bones can be detached from each other (their head joint doesn't
necessarily need to be at the same position as the tail joint of their parent
bone).

A pose can be applied to the skeleton by setting a pose matrix for each of the
bones, allowing static posing or animation playback.
The skeleton supports skinning of a mesh using a list of vertex-to-bone
assignments.
```


BVH files are readily available, e.g. `http://www.makehumancommunity.org/content/figure_skating_sit_spin`. The `.mhm` saved models contain the `pose` pointing to the corresponding BVH (built-in poses are in `/usr/share/makehuman/data/poses/`). An example is stored under `makehuman_data/poses`.

There are some OS iniciatives to parse BVH:

* MH itself
* https://github.com/omimo/PyMO



Before evaluating which one is best, further assessment about the blender sequence rendering and python integration is needed.


### Blender sequences:




`bpy.ops.import_anim.bvh(filepath="/home/a9fb1e/github-work/human-renderer/makehuman_data/poses/cmu_motion_captures/01/01_06.bvh")`





## Makewalk:


To control MHX2 models using BHV within Blender, different sources suggest using the MakeWalk plugin. The PPA doesn't offer it, neither any official page. Older releases seem to have it included: `http://files.jwp.se/archive/releases/1.1.1/` (a copy is saved into this repo):
    1. Extract the makewalk folder and copy it into Blender's plugins folder (e.g. `~/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib`)
    2. Activate it in `Blender -> File -> User Preferences -> Add-ons` and save
    3. 


Set frame end:

```
bpy.data.scenes[0].frame_end = 1234 # the one for the player
bpy.context.scene.McpEndFrame = 2345 # the one for makewalk?
```

png images to mp4:

```
ffmpeg -i %04d.png -vf "transpose=2" output.mp4

```


## HEADLESS BLENDER:

See https://blender.stackexchange.com/questions/31255/can-blender-render-on-systems-without-a-gui
CLI docs: https://docs.blender.org/manual/en/latest/render/workflows/command_line.html

```
blender --background myblend.blend -x 1 -f $n

blender -b myBlenderFile.blend -a

```
