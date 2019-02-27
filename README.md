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

