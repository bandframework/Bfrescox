"""
|bfrescox| is a Python package that builds an internal, barebones |frescox|
binary during installation.  It also provides an interface for using the binary
to configure and run |frescox| simulations using the internal binary as well as
to access results.
"""

from importlib.metadata import version

# ----- Python unittest-based test framework
# Used for automatic test discovery
from .load_tests import load_tests

# Allow users to run full test suite as bfrescox.test()
from .test import test

__version__ = version("bfrescox")
