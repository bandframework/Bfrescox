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

from pathlib import Path
from setuptools import setup

# ----- HARDCODED VALUES
_PKG_ROOT = Path(__file__).resolve().parent

# Package metadata
PYTHON_REQUIRES = ">=3.9"
CODE_REQUIRES = []
TEST_REQUIRES = []
INSTALL_REQUIRES = CODE_REQUIRES + TEST_REQUIRES

PACKAGE_DATA = {
    "bfrescox": []
}

PROJECT_URLS = {
    "Source": "https://github.com/bandframework/Bfrescox",
    "Documentation": "http://Bfrescox.readthedocs.io",
    "Tracker": "https://github.com/bandframework/Bfrescox/issues"
}


# ----- SPECIFY THE PACKAGE
def readme_md():
    fname = _PKG_ROOT.joinpath("README.md")
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
