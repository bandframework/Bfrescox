from os import PathLike
from pathlib import Path
from typing import Optional

from ._run_frescox_simulation import _run_frescox_simulation
from .Configuration import Configuration
from .information import information


def run_simulation(
    configuration: Configuration,
    filename: str | PathLike[str],
    overwrite: bool = False,
    mpi_setup: Optional[dict] = None,
    cwd: Optional[str | PathLike[str]] = None,
):
    """
    Run a |frescox| simulation based on the given simulation
    configuration object.  Results are written to a file with the given
    output filename.  The |frescox| Fortran namelist configuration file
    generated from the configuration object for the simulation is
    written alongside the results file.

    Args:
        configuration (Configuration): :py:class:`Configuration` object
        that specifies the simulation to run
        filename (str | PathLike[str]): Filename including path of file
        to write outputs to
        overwrite (bool): If False, then an error is raised if either of
        the simulation input or output files exist
        mpi_setup (dict, optional): Dictionary specifying MPI setup cwd
        (str | PathLike[str]): directory to run the simulation in.  If
        None, the current working directory is used.

    Raises:
        ValueError: If no valid internal or external |frescox|
            installation is found
    """
    if cwd is None:
        cwd = Path.cwd()
    # This function assumes that all error checking of arguments
    # will be handled by this internal function.
    _run_frescox_simulation(
        information(),
        configuration,
        filename,
        overwrite,
        mpi_setup,
        cwd,
    )
