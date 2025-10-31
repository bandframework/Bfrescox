"""
Automatic system-level tests of package using Elastic scattering template
"""

import inspect
import json
import os
import shutil
import unittest
from pathlib import Path

import bfrescoxpro
import numpy as np
from bfrescoxpro import parse_differential_xs

INSTALL_PATH = Path(inspect.getfile(bfrescoxpro)).resolve().parent
TEMPLATES_PATH = INSTALL_PATH.joinpath("PkgData").resolve()
DATA_PATH = INSTALL_PATH.joinpath("tests", "TestData").resolve()


class TestElasticProblems(unittest.TestCase):
    def setUp(self):
        fname_suite = DATA_PATH.joinpath("TestSuite_UserProvidedTemplate.json")
        with open(fname_suite, "r") as fptr:
            self.__suite = json.load(fptr)

        self.__dir = Path.cwd().joinpath("delete_me_please")
        self.__nml = self.__dir.joinpath("test.nml")
        self.__fname_out = self.__dir.joinpath("test.out")
        self.__info = bfrescoxpro.information()

    def tearDown(self):
        if self.__dir.exists():
            shutil.rmtree(self.__dir)

    def _clean_tmp_dir(self):
        if self.__dir.is_file():
            os.remove(self.__dir)
        elif self.__dir.is_dir():
            shutil.rmtree(self.__dir)
        os.mkdir(self.__dir)

    def testAllProblems(self):
        for template, specification in self.__suite.items():
            template_fname = DATA_PATH.joinpath(specification["Template"])
            output_fname = self.__dir.joinpath("test_{template}.nml")

            for test_name, test_info in specification["Tests"].items():
                # Reestablish empty directory for each test
                self._clean_tmp_dir()

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
                    cfg, self.__fname_out, mpi_setup=mpi_setup, cwd=self.__dir
                )
                self.assertTrue(self.__fname_out.is_file())

                # Check all results against official baselines
                # TODO this should be factored out for use in other test suites
                for quantity, quantity_info in test_info["Results"].items():
                    if quantity.lower() == "differential_xs_absolute_mb_per_sr":
                        results_df = parse_differential_xs.absolute_mb_per_sr(
                            self.__fname_out
                        )
                    elif (
                        quantity.lower()
                        == "differential_xs_ratio_to_rutherford"
                    ):
                        results_df = parse_differential_xs.ratio_to_rutherford(
                            self.__fname_out
                        )
                    else:
                        msg = f"Unknown physical quantity {quantity}"
                        raise ValueError(msg)

                    rel_diff_tolr = 0.0
                    abs_diff_tolr = 0.0

                    baseline = quantity_info["Baseline"]
                    if "AbsDiffThreshold" in quantity_info:
                        abs_diff_tolr = quantity_info["AbsDiffThreshold"]
                    if "RelDiffThreshold" in quantity_info:
                        rel_diff_tolr = quantity_info["RelDiffThreshold"]

                    self.assertTrue(abs_diff_tolr >= 0.0)
                    self.assertTrue(rel_diff_tolr >= 0.0)

                    expected = np.loadtxt(
                        fname=DATA_PATH.joinpath(baseline), delimiter=","
                    )
                    self.assertEqual(2, expected.ndim)
                    self.assertEqual(2, expected.shape[1])

                    self.assertEqual(len(expected), len(results_df))
                    self.assertEqual(1, len(results_df.columns))

                    deg = expected[:, 0]
                    self.assertEqual(set(deg), set(results_df.index))
                    result_data = results_df.loc[deg, quantity].values
                    if (abs_diff_tolr == 0.0) and (rel_diff_tolr == 0.0):
                        self.assertTrue(all(result_data == expected[:, 1]))
                    else:
                        if abs_diff_tolr > 0.0:
                            np.testing.assert_allclose(
                                result_data,
                                expected[:, 1],
                                rtol=0.0,
                                atol=abs_diff_tolr,
                            )
                        if rel_diff_tolr > 0.0:
                            np.testing.assert_allclose(
                                result_data,
                                expected[:, 1],
                                rtol=rel_diff_tolr,
                                atol=0.0,
                            )
