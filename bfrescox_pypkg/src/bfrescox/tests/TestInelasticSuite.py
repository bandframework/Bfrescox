import inspect
import json
import os
import shutil
import unittest
from pathlib import Path

import bfrescox
import pandas as pd

from .utils import compare_arrays

INSTALL_PATH = Path(inspect.getfile(bfrescox)).resolve().parent
DATA_PATH = INSTALL_PATH.joinpath("tests", "TestData").resolve()


class TestInelasticProblems(unittest.TestCase):
    def setUp(self):
        fname_suite = DATA_PATH.joinpath("TestSuite_Inelastic.json")
        with open(fname_suite, "r") as fptr:
            self.__suite = json.load(fptr)

        self.__dir = Path.cwd().joinpath("delete_me_please")
        os.mkdir(self.__dir)
        self.__testdir = self.__dir.joinpath("test")
        self.__fname_out = self.__testdir.joinpath("test.out")

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
            bfrescox.generate_inelastic_template(
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

                cfg = bfrescox.Configuration.from_template(
                    template_fname,
                    output_fname,
                    template_parameters,
                    overwrite=False,
                )
                self.assertFalse(self.__fname_out.is_file())
                bfrescox.run_simulation(
                    cfg, self.__fname_out, cwd=self.__testdir
                )
                self.assertTrue(self.__fname_out.is_file())

                # Check all results against official baselines
                for quantity, quantity_info in test_info["Results"].items():
                    fname = DATA_PATH.joinpath(quantity_info["Baseline"])

                    rel_diff_tolr = 0.0
                    abs_diff_tolr = 0.0

                    if "AbsDiffThreshold" in quantity_info:
                        abs_diff_tolr = quantity_info["AbsDiffThreshold"]
                    if "RelDiffThreshold" in quantity_info:
                        rel_diff_tolr = quantity_info["RelDiffThreshold"]

                    if quantity.lower() == "fort.16":
                        df_baseline = pd.read_csv(fname)
                        expected = {
                            ch: grp.drop(
                                columns="channel"
                            ).reset_index(drop=True)
                            for ch, grp in df_baseline.groupby(
                                "channel", sort=False
                            )
                        }
                        results = bfrescox.parse_fort16(
                            self.__testdir / "fort.16"
                        )
                        self.assertEqual(expected.keys(), results.keys())
                        for key in expected.keys():
                            compare_arrays(
                                results[key],
                                expected[key],
                                abs_diff_tolr,
                                rel_diff_tolr,
                            )
                    else:
                        msg = f"Unknown results file type {quantity}"
                        raise ValueError(msg)
