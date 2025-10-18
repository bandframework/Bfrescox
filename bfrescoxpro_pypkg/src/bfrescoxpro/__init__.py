"""
|bfrescoxpro| is a Python package that can be used by power users to build a
customized internal |frescox| binary during installation.  It also provides an
interface for using the binary to configure and run |frescox| simulations using
the internal binary as well as to access results.
"""

from importlib.metadata import version

from ._run_frescox_simulation import (
    FRESCOX_EXE,
    FRESCOX_MPI_SUPPORT, FRESCOX_OPENMP_SUPPORT,
    FRESCOX_LAPACK_SUPPORT,
    FRESCOX_COREX_SUPPORT
)

from .information import information
from .print_information import print_information
from .run_simulation import run_simulation

from .Configuration import Configuration
from .Result import (
    read_fort16,
    read_results_lines,
    parallelization_setup,
    performance_results,
    cross_sections_mbsr,
    cross_sections_R2R,
)
from .generate_inelastic_template import generate_inelastic_template
from .generate_elastic_template import generate_elastic_template

# ----- Python unittest-based test framework
# Used for automatic test discovery
from .load_tests import load_tests

# Allow users to run full test suite as bfrescox.test()
from .test import test

__version__ = version("bfrescoxpro")
