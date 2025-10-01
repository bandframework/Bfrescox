from importlib.metadata import version

# ----- Python unittest-based test framework
# Used for automatic test discovery
from .load_tests import load_tests

# Allow users to run full test suite as bfrescox.test()
from .test import test

__version__ = version("bfrescox")
