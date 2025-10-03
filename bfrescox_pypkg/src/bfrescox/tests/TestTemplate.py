"""
Template of unittest test case
"""

import inspect
import unittest

from pathlib import Path

import bfrescox

_PKG_ROOT = Path(inspect.getfile(bfrescox)).resolve().parent

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDoNothing(self):
        self.assertTrue(True)
