# -*- coding:utf-8 -*-


"""
Main app file
"""

from time import time
#
from humanrenderer.foo_module import Foo


__author__ = "Andres FR"


def do_loop(clss, memsize, loopsize):
    """
    Create a Foo instance and loop it.
    """
    print("called do_loop:", (clss.__name__, memsize, loopsize))
    x = clss(memsize)
    t = time()
    x.loop(loopsize)
    print("  do_loop took", time()-t, "seconds")


if __name__ == "__main__":
    MEMSIZE = 1000000
    LOOPSIZE = 100
    do_loop(Foo, MEMSIZE, LOOPSIZE)


# run all tests:
# python -m unittest discover -s utest -t . -p "*_test.py" -v


# bump version: after a satisfactory commit do:
# bump2version {major | minor | patch}
