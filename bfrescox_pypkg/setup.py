# IMPORTANT
# * Please ensure that all changes made here to the Python and external package
#   dependencies/versions are also made in a consistent way in tox.ini and
#   GitHub actions.
#
# Since the package's version is set automatically by setuptools-scm, there is
# no need to handle version manually here.
#
# Refer to documentation in pyproject.toml for more information regarding this
# file and how to maintain it.

import os
import sys
import shutil

import subprocess as sbp

from pathlib import Path
from setuptools import (
    setup, Command
)
from setuptools.command.build import build as _build

# ----- HARDCODED VALUES
PKG_ROOT = Path(__file__).resolve().parent
PY_SRC_PATH = PKG_ROOT.joinpath("src", "bfrescox")
MESON_BUILD_PATH = PKG_ROOT.joinpath("meson")

# Names of Frescox products to include
EXE_NAMES = ["frescox"]

# Package metadata
PYTHON_REQUIRES = ">=3.9"
CODE_REQUIRES = ["numpy>=1.21", "pandas>=1.3"]
TEST_REQUIRES = []
INSTALL_REQUIRES = CODE_REQUIRES + TEST_REQUIRES

PACKAGE_DATA = {
    "bfrescox":
        [f"bin/{exe}" for exe in EXE_NAMES] +
        ["build/build_info.csv"]
}

PROJECT_URLS = {
    "Source": "https://github.com/bandframework/Bfrescox",
    "Documentation": "http://Bfrescox.readthedocs.io",
    "Tracker": "https://github.com/bandframework/Bfrescox/issues"
}


# ----- CUSTOM COMMAND TO BUILD FRESCOX BINARIES
class build(_build):
    sub_commands = ([("build_frescox", None)])


class build_frescox(Command):
    description = "Build the Frescox software package"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self, *args, **kwargs):
        if shutil.which("meson", mode=os.F_OK | os.X_OK) is None:
            print()
            print("Please install the Meson build system & add meson to path")
            print()
            sys.exit(1)

        # To build debug versions with more output,
        # * use --buildtype=debug
        # * consider adding arguments such as --warnlevel and --werror to
        #   SETUP_CMD
        # * Remove "--quiet" from INSTALL_CMD
        # * Use python -m pip install -v ...
        SETUP_CMD = ["meson", "setup", "--wipe", "--clearcache",
                     "--buildtype=release", "builddir",
                     f"-Dprefix={PY_SRC_PATH}",
                     "--warnlevel", "0"]
        # Since this is Fortran code from older standards and I suspect that it
        # uses implict variables, I don't want to assume that the Meson build
        # system's tools for determining interfile dependencies can figure out
        # how to compile files in parallel.  Force serial builds.
        COMPILE_CMD = ["meson", "compile", "-v", "-j", "1", "-C", "builddir"]
        INSTALL_CMD = ["meson", "install", "--quiet", "-C", "builddir"]

        # Install the binaries within the Python source files and so that they
        # are included in the wheel build based on PACKAGE_DATA
        cwd = Path.cwd()
        os.chdir(MESON_BUILD_PATH)
        for cmd in [SETUP_CMD, COMPILE_CMD, INSTALL_CMD]:
            try:
                sbp.run(cmd,
                        stdin=sbp.DEVNULL, capture_output=False,
                        check=True)
            except sbp.CalledProcessError as err:
                print()
                msg = "[meson build] Unable to run command (Return code {})"
                print(msg.format(err.returncode))
                print("[meson build] " + " ".join(err.cmd))
                sys.exit(2)
        os.chdir(cwd)


cmdclass = {
    'build': build,
    'build_frescox': build_frescox
}


# ----- SPECIFY THE PACKAGE
def readme_md():
    fname = PKG_ROOT.joinpath("README.md")
    with open(fname, "r", encoding="utf8") as fptr:
        return fptr.read()


setup(
    name='bfrescox',
    author="Kyle Beyer, Manuel Catacora-Rios, and Jared O'Neal",
    author_email="beyerk@frib.msu.edu",
    maintainer="Kyle Beyer",
    maintainer_email="beyerk@frib.msu.edu",
    description="Run Frescox through Python",
    long_description=readme_md(),
    long_description_content_type="text/markdown",
    url=PROJECT_URLS["Source"],
    project_urls=PROJECT_URLS,
    license="BSD-2-Clause",
    package_dir={"": "src"},
    package_data=PACKAGE_DATA,
    cmdclass=cmdclass,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ]
)
