from pathlib import Path
from typing import Optional

from ._run_frescox_simulation import _run_frescox_simulation
from .Configuration import Configuration
from .information import information


def run_simulation(
    configuration: Configuration,
    filename: Path,
    overwrite: bool = False,
    mpi_setup: Optional[dict] = None,
    cwd: Optional[Path] = None,
):
    """
    Run a |frescox| simulation based on the given simulation
    configuration object.  Results are written to a file with the given
    output filename.  The |frescox| Fortran namelist configuration file
    generated from the configuration object for the simulation is
    written alongside the results file.

    .. todo::
        * Load and return a result object once that class exists.

    Parameters:
        configuration (Configuration): :py:class:`Configuration` object
        that specifies the simulation to run
        filename (Path): Filename including path of file to write
            outputs to
        overwrite (bool): If False, then an error is raised if either of the
            simulation input or output files exist
        mpi_setup (dict, optional): Dictionary specifying MPI setup
        cwd (Path, optional): Current working directory to run the
            simulation in.  If None, the current working directory of
            the calling process is used. Defaults to None.
    Raises:
        ValueError: If no valid internal or external |frescox|
            installation is found
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
