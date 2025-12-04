"""
Automatic unittests of Configuration class
"""

import inspect
import json
import os
import shutil
import unittest
from pathlib import Path

import bfrescoxpro
import f90nml

INSTALL_PATH = Path(inspect.getfile(bfrescoxpro)).resolve().parent
TEMPLATES_PATH = INSTALL_PATH.joinpath("PkgData").resolve()
DATA_PATH = INSTALL_PATH.joinpath("tests", "TestData").resolve()


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        fname_suite = DATA_PATH.joinpath("TestSuite_UserProvidedTemplate.json")
        with open(fname_suite, "r") as fptr:
            self.__suite = json.load(fptr)

        self.__dir = Path.cwd().joinpath("delete_me_please")
        self.__nml = self.__dir.joinpath("frescox.in")

        # Setup clean directory
        self._clean_tmp_dir()

    def tearDown(self):
        if self.__dir.exists():
            shutil.rmtree(self.__dir)

    def _clean_tmp_dir(self):
        if self.__dir.is_file():
            os.remove(self.__dir)
        elif self.__dir.is_dir():
            shutil.rmtree(self.__dir)
        os.mkdir(self.__dir)

    def testFromMethod(self):
        for template, specification in self.__suite.items():
            template_fname = DATA_PATH.joinpath(specification["Template"])
            output_fname = self.__dir.joinpath("from_template.nml")

            for test_name, test_info in specification["Tests"].items():
                # Reestablish empty directory for each test
                self._clean_tmp_dir()

                fname_nml = DATA_PATH.joinpath(test_info["NML"])
                expected = f90nml.read(fname_nml).todict()

                template_parameters = test_info["TemplateParameters"]

                cfgs_all = [
                    bfrescoxpro.Configuration.from_NML(fname_nml),
                    bfrescoxpro.Configuration.from_template(
                        template_fname,
                        output_fname,
                        template_parameters,
                        overwrite=False,
                    ),
                ]
                for cfg in cfgs_all:
                    if self.__nml.exists():
                        os.remove(self.__nml)
                    cfg.write_to_nml(self.__nml)
                    self.assertTrue(self.__nml.is_file())

                    result = f90nml.read(self.__nml).todict()
                    self.assertEqual(expected, result)
