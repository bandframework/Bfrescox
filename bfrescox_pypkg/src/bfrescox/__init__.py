"""
|bfrescox| is a Python package that builds an internal, barebones |frescox|
binary during installation.  It also provides an interface for using the binary
to configure and run |frescox| simulations using the internal binary as well as
to access results.
"""

from importlib.metadata import version

from ._run_frescox_simulation import (
    FRESCOX_COREX_SUPPORT,
    FRESCOX_EXE,
    FRESCOX_LAPACK_SUPPORT,
    FRESCOX_MPI_SUPPORT,
    FRESCOX_OPENMP_SUPPORT,
)
from .Configuration import Configuration
from .generate_elastic_template import generate_elastic_template
from .generate_inelastic_template import generate_inelastic_template
from .information import information
from .load_tests import load_tests
from .parse_differential_xs import absolute_mb_per_sr, ratio_to_rutherford
from .parse_parallelization_setup import parse_parallelization_setup
from .parse_performance_results import parse_performance_results
from .print_information import print_information
from .run_simulation import run_simulation

# Allow users to run full test suite as bfrescox.test()
from .test import test

__version__ = version("bfrescox")
