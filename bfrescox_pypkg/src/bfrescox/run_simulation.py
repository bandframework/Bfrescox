import copy
import warnings

from .information import information
from ._run_frescox_simulation import (
    run_frescox_simulation,
    FRESCOX_MPI_SUPPORT, FRESCOX_OPENMP_SUPPORT,
    FRESCOX_LAPACK_SUPPORT,
    FRESCOX_COREX_SUPPORT
)


def run_simulation(configuration, filename, overwrite=False, external=None):
    """
    Run a |frescox| simulation based on the given simulation configuration
    object.  Results are written to a file with the given output filename.  The
    |frescox| Fortran namelist configuration file generated from the
    configuration object for the simulation is written alongside the results
    file.

    .. todo::
        * Load and return a result object once that class exists.

    :param configuration: :py:class:`Configuration` object that specifies the
        simulation to run
    :param filename: Filename including path of file to write outputs to
    :param overwrite: If True, then an error is raised if either of the
        simulation input or output files exist
    :param external: (|bfrescox| only) **EXPERT USERS ONLY**
    """
    # Assume for now that external installations will not be using MPI
    NO_MPI_PLEASE = None

    frescox = information()
    if (not frescox) and (external is None):
        msg = (
            "Invalid Frescox installation and no external installation provided"
        )
        raise ValueError(msg)

    if external is not None:
        # If users want to use an external installation built with MPI, could we
        # ask them to supply the MPI setup information in external and pull that
        # out here?
        msg = "Using user-provided external Frescox installation"
        if not frescox:
            msg += "\nOverriding the existing internal installation"
        warnings.warn(msg)
        frescox = copy.deepcopy(external)
    else:
        assert not frescox[FRESCOX_MPI_SUPPORT]
        assert not frescox[FRESCOX_OPENMP_SUPPORT]
        assert not frescox[FRESCOX_LAPACK_SUPPORT]
        assert not frescox[FRESCOX_COREX_SUPPORT]

    # This function assumes that all error checking of arguments will be handled
    # by this internal function.  This includes the case of incorrectly
    # providing an MPI-based external installation.
    run_frescox_simulation(frescox, configuration, NO_MPI_PLEASE,
                           filename, overwrite)
