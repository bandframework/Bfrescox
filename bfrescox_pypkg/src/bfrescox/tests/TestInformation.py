"""
Automatic unittest of information() function
"""

import unittest
from pathlib import Path

import bfrescox


class TestInformation(unittest.TestCase):
    def testInformation(self):
        info = bfrescox.information()
        self.assertTrue(isinstance(info, dict))

        expected = {
            bfrescox.FRESCOX_EXE,
            bfrescox.FRESCOX_MPI_SUPPORT,
            bfrescox.FRESCOX_OPENMP_SUPPORT,
            bfrescox.FRESCOX_LAPACK_SUPPORT,
            bfrescox.FRESCOX_COREX_SUPPORT,
        }
        self.assertEqual(expected, set(info))

        frescox_exe = info[bfrescox.FRESCOX_EXE]
        self.assertTrue(isinstance(frescox_exe, Path))
        self.assertTrue(frescox_exe.is_file())

        # Confirm bare-bones
        support = [
            bfrescox.FRESCOX_MPI_SUPPORT,
            bfrescox.FRESCOX_OPENMP_SUPPORT,
            bfrescox.FRESCOX_LAPACK_SUPPORT,
            bfrescox.FRESCOX_COREX_SUPPORT,
        ]
        for key in support:
            self.assertFalse(info[key])
