"""
Automatic unittest of print_information() function
"""

import io
import unittest

from contextlib import redirect_stdout

import bfrescoxpro


class TestPrintInformation(unittest.TestCase):
    def testPrintInformation(self):
        # Capture stdout so that message doesn't clutter test output and we can
        # test message content
        with redirect_stdout(io.StringIO()) as buffer:
            bfrescoxpro.print_information()
        self.assertNotEqual("", buffer.getvalue())
