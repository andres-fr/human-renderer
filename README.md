[![Build Status](https://travis-ci.com/andres-fr/human-renderer.svg?token=cUXVqzsqAP4ZpSpN77Kh&branch=master)](https://travis-ci.com/andres-fr/human-renderer)

# human-renderer


### run all tests:

```
python -m unittest discover -s utest -t . -p "*_test.py" -v
```

### Bump version:

After a satisfactory commit do:

```
bump2version {major | minor | patch}
```

And then a push will automatically trigger the tag release.

### Build package:

```
python setup.py clean --all
rm -r *.egg-info
python setup.py sdist bdist_wheel
```


### Build docs:

Args help: `sphinx-quickstart -h`

Run this in the repo root:

```
rm -r docs/
version=`grep "current_version" .bumpversion.cfg | cut -d'=' -f2 | xargs`
sphinx-quickstart -q -p humanrenderer -a "Andres FR" --makefile --batchfile --ext-autodoc --ext-mathjax --ext-viewcode --ext-githubpages -d version=$version -d release=$version docs/
# sadly the following is needed to change the html_theme flag
sed -i '/html_theme/d' docs/conf.py # remove the html_theme line
sed -i '1r ci_scripts/sphinx_doc_config.txt' docs/conf.py # add the desired config after line 1
echo "" >> docs/conf.py # add newline at EOF to pass flake8
sphinx-apidoc -f humanrenderer -o docs/
make -C docs clean && make -C docs latexpdf && make -C docs html
 ```


