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

# After installing blender, copy the import rutine into the blender addons folder
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



### Blender

Install as follows:

1. Download from `https://www.blender.org/download/`
2. Unpack into `<BLENDERPATH>` (e.g. `~/opt/`)
3. Add to PATH in `.bashrc` or `.profile` (e.g. `export PATH=$HOME/opt/blender-2.79b-linux-glibc219-x86_64:$PATH`)
4. now running `blender` will work on any terminal with that environment.

When importing the `MHX2` human model, it will appear whithout textures (all white), but this is normal behaviour for the edit mode. Textures will be included in render mode.

Experiments with the Python console (see https://docs.blender.org/manual/en/latest/editors/python_console.html):


(Blender Python API: `https://docs.blender.org/api/2.79b/`)


https://docs.blender.org/api/2.78a/bpy.types.Object.html#bpy.types.Object.pose


https://docs.blender.org/api/2.78a/bpy.types.Pose.html




```
py.data.objects.keys()
bpy.data.objects["Testmodel"].pose.bones

```
