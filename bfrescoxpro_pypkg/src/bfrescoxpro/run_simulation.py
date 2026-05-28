from os import PathLike
from pathlib import Path
from typing import Optional, Union

from ._run_frescox_simulation import _run_frescox_simulation
from .Configuration import Configuration
from .information import information


def run_simulation(
    configuration: Configuration,
    filename: Union[str, PathLike],
    overwrite: Optional[bool] = False,
    mpi_setup: Optional[dict] = None,
    cwd: Optional[Union[str, PathLike]] = None,
):
    """
    Run a |frescox| simulation based on the given simulation configuration
    object. Standard output and error are written to a file with the given
    output filename.  Other outputs are written to disk based on the |frescox|
    output settings.  The |frescox| Fortran namelist configuration file
    generated from the configuration object for the simulation is written
    alongside the output file.

    Args:
        configuration:
            :py:class:`Configuration` object that specifies the simulation to
            run.
        filename:
            Filename including path of file to write |frescox| stdout/stderr
            logging to
        overwrite:
            If False, then an error is raised if either of the simulation input
            or output files exist
        mpi_setup:
            Dictionary specifying MPI setup
        cwd:
            Pre-existing directory to run the simulation in.  If None, the
            current working directory is used.
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
