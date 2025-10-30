from ._run_frescox_simulation import _run_frescox_simulation
from .information import information


def run_simulation(
    configuration, filename, overwrite=False, mpi_setup=None, cwd=None
):
    """
    Run a |frescox| simulation based on the given simulation
    configuration object.  Results are written to a file with the given
    output filename.  The |frescox| Fortran namelist configuration file
    generated from the configuration object for the simulation is
    written alongside the results file.

    .. todo::
        * Load and return a result object once that class exists.

    :param configuration: :py:class:`Configuration` object that
    specifies the simulation to run
    :param filename: Filename including path of file to write outputs to
    :param overwrite: If False, then an error is raised if either of the
        simulation input or output files exist
    :param mpi_setup: `dict` that provides MPI setup values if
        executable built with MPI; `None`, otherwise.
    :param cwd: Working directory to run the simulation in; if `None`,
        then the current working directory is used
    """
    # This function assumes that all error checking of arguments
    # will be handled by this internal function.
    _run_frescox_simulation(
        information(),
        configuration,
        mpi_setup,
        filename,
        overwrite=overwrite,
        cwd=cwd,
    )
