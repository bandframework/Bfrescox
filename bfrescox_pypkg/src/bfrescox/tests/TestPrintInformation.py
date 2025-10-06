"""
Automatic unittest of print_information() function
"""

import unittest

import bfrescox


class TestPrintInformation(unittest.TestCase):
    def testPrintInformation(self):
        # We can only ensure that this isn't raising exceptions
        #
        # TODO: Is there a way to suppress this output?  If we can get it as a
        # string and confirm that contents aren't empty, that would be even
        # better.
        bfrescox.print_information()
