"""
Automatic system-level tests of package using Elastic scattering template
"""

import inspect
import json
import os
import pickle
import shutil
import unittest
from pathlib import Path

import bfrescoxpro

from .utils import compare_arrays

INSTALL_PATH = Path(inspect.getfile(bfrescoxpro)).resolve().parent
TEMPLATES_PATH = INSTALL_PATH.joinpath("PkgData").resolve()
DATA_PATH = INSTALL_PATH.joinpath("tests", "TestData").resolve()


class TestElasticProblems(unittest.TestCase):
    def setUp(self):
        fname_suite = DATA_PATH.joinpath("TestSuite_Elastic.json")
        with open(fname_suite, "r") as fptr:
            self.__suite = json.load(fptr)

        self.__dir = Path.cwd().joinpath("delete_me_please")
        os.mkdir(self.__dir)
        self.__testdir = self.__dir.joinpath("test")
        self.__fname_out = self.__testdir.joinpath("test.out")
        self.__info = bfrescoxpro.information()
        self.maxDiff = None

    def tearDown(self):
        if self.__dir.exists():
            shutil.rmtree(self.__dir)

    def _clean_test_dir(self):
        if self.__testdir.is_file():
            os.remove(self.__testdir)
        elif self.__testdir.is_dir():
            shutil.rmtree(self.__testdir)
        os.mkdir(self.__testdir)

    def testAllProblems(self):
        for template, specification in self.__suite.items():
            expected_template_fname = DATA_PATH.joinpath(
                specification["Template"]
            )
            template_fname = self.__dir.joinpath(f"{template}.template")
            output_fname = self.__testdir.joinpath(f"{template}.nml")

            # generate template file
            bfrescoxpro.generate_elastic_template(
                template_fname, **specification["ProblemConfig"]
            )

            # Verify generated template matches expected template
            with open(template_fname, "r") as fptr_generated:
                generated_content = fptr_generated.read()
            with open(expected_template_fname, "r") as fptr_expected:
                expected_content = fptr_expected.read()

            self.assertEqual(generated_content, expected_content)

            # run all tests for generated template
            for _, test_info in specification["Tests"].items():
                # Reestablish empty directory for each test
                self._clean_test_dir()

                template_parameters = test_info["TemplateParameters"]

                mpi_setup = None
                if self.__info["supports_mpi"]:
                    pro_setup = test_info["ProSetup"]
                    mpi_setup = {"n_processes": pro_setup["nMpiProcs"]}

                if self.__info["supports_openmp"]:
                    pro_setup = test_info["ProSetup"]
                    n_threads = pro_setup["nOmpThreads"]
                    os.environ["OMP_NUM_THREADS"] = str(n_threads)

                cfg = bfrescoxpro.Configuration.from_template(
                    template_fname,
                    output_fname,
                    template_parameters,
                    overwrite=False,
                )
                self.assertFalse(self.__fname_out.is_file())
                bfrescoxpro.run_simulation(
                    cfg,
                    self.__fname_out,
                    mpi_setup=mpi_setup,
                    cwd=self.__testdir,
                )
                self.assertTrue(self.__fname_out.is_file())

                # Check all results against official baelines
                for quantity, quantity_info in test_info["Results"].items():
                    fname = DATA_PATH.joinpath(quantity_info["Baseline"])
                    with open(fname, "rb") as fptr:
                        expected = pickle.load(fptr)

                    rel_diff_tolr = 0.0
                    abs_diff_tolr = 0.0

                    if "AbsDiffThreshold" in quantity_info:
                        abs_diff_tolr = quantity_info["AbsDiffThreshold"]
                    if "RelDiffThreshold" in quantity_info:
                        rel_diff_tolr = quantity_info["RelDiffThreshold"]

                    if quantity.lower() == "fort.16":
                        results = bfrescoxpro.parse_fort16(
                            self.__testdir / "fort.16"
                        )
                        assert expected.keys() == results.keys()
                        for key in expected.keys():
                            compare_arrays(
                                results[key],
                                expected[key],
                                abs_diff_tolr,
                                rel_diff_tolr,
                            )
                    else:
                        msg = f"Unknown physical quantity {quantity}"
                        raise ValueError(msg)
