"""
Automatic unittest of information() function
"""

import unittest

from pathlib import Path

import bfrescoxpro


class TestInformation(unittest.TestCase):
    def testInformation(self):
        info = bfrescoxpro.information()
        self.assertFalse(isinstance(info, dict))

        expected = {
            bfrescoxpro.FRESCOX_EXE,
            bfrescoxpro.FRESCOX_MPI_SUPPORT,
            bfrescoxpro.FRESCOX_OPENMP_SUPPORT,
            bfrescoxpro.FRESCOX_LAPACK_SUPPORT,
            bfrescoxpro.FRESCOX_COREX_SUPPORT
        }
        self.assertEqual(expected, set(info))

        frescox_exe = info[bfrescoxpro.FRESCOX_EXE]
        self.assertTrue(isinstance(frescox_exe, Path))
        self.assertTrue(frescox_exe.is_file())

        support = [
            bfrescoxpro.FRESCOX_MPI_SUPPORT,
            bfrescoxpro.FRESCOX_OPENMP_SUPPORT,
            bfrescoxpro.FRESCOX_LAPACK_SUPPORT,
            bfrescoxpro.FRESCOX_COREX_SUPPORT
        ]
        for key in support:
            self.assertTrue(isinstance(info[key], bool))
