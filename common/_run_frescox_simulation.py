import os
import subprocess as sbp
from numbers import Integral
from os import PathLike
from pathlib import Path
from typing import Union

from .Configuration import Configuration

# Keys for Frescox executable configuration dictionary
FRESCOX_EXE = "frescox_exe"
# These should match the keys in build_info.template that the Frescox build
# system uses to write its configuration values to file.
FRESCOX_MPI_SUPPORT = "supports_mpi"
FRESCOX_OPENMP_SUPPORT = "supports_openmp"
FRESCOX_LAPACK_SUPPORT = "supports_lapack"
FRESCOX_COREX_SUPPORT = "supports_corex"

# MPI setup keys
MPI_N_PROCESSES = "n_processes"


def _run_frescox_simulation(
    frescox: dict,
    config: Configuration,
    filename: Union[str, PathLike],
    overwrite: bool,
    mpi_setup: dict,
    cwd: Union[str, PathLike],
):
    """
    Run a |frescox| simulation using the given |frescox| installation,
    simulation configuration, and MPI setup.  stdout is written to disk
    using the given output filename. Other outputs are written to disk
    based on the |frescox| output settings. The |frescox| Fortran
    namelist configuration file generated from the configuration object
    for the simulation is written alongside the results file.

    .. todo::
        * Load and return a result object once that class exists.
        * System level tests will check the general functionality of
        this code.  However, we need to write a set of tests that
        confirm correct detection and management of bad inputs.
        * Allow for the case that a user is required to use a system's
        own program for starting MPI programs (e.g., jsrun).

    Args:
        frescox (dict): Dictionary that fully characterizes a |frescox|
            installation
        config (Configuration): |bfrescox| :py:class:`Configuration`
            object that specifies the simulation to execute
        filename (Union[str, PathLike]): Filename including path of file
            to write outputs to
        overwrite (bool): If False, then an error is raised if either
            the input or output files exist
        mpi_setup (dict): Dictionary that provides MPI setup values if
            given |frescox| installation built with MPI; ``None``,
            otherwise.
        cwd (Union[str, PathLike]): directory to run the simulation in.

    Raises:
        TypeError
            If any of the arguments are of incorrect type
        ValueError
            If any of the argument values are invalid
        RuntimeError
            If output file already exists and overwrite is False, or if
            OpenMP is to be used but OMP_NUM_THREADS environment variable
            is not set, or if the |frescox| executable fails during execution
    """
    # ----- ERROR CHECK ARGUMENTS
    if not isinstance(frescox, dict):
        raise TypeError(f"Invalid frescox specification ({frescox})")

    frescox_exe = Path(frescox[FRESCOX_EXE]).resolve()
    use_mpi = frescox[FRESCOX_MPI_SUPPORT]
    use_omp = frescox[FRESCOX_OPENMP_SUPPORT]
    if not frescox_exe.is_file():
        msg = "Frescox executable does not exist or is not a file ({})"
        raise TypeError(msg.format(frescox_exe))
    if not isinstance(use_mpi, bool):
        raise TypeError("MPI support specification is not a boolean")
    if not isinstance(use_omp, bool):
        raise TypeError("OpenMP support specification is not a boolean")
    if use_omp and ("OMP_NUM_THREADS" not in os.environ):
        msg = (
            "OMP_NUM_THREADS environment variable is not set "
            "for use with OpenMP-enabled Frescox installation"
        )
        raise RuntimeError(msg)

    if not isinstance(config, Configuration):
        msg = "Configuration information not given as a Configuration object"
        raise TypeError(msg)

    n_mpi_procs = None
    if (not use_mpi) and (mpi_setup is not None):
        msg = "MPI specification provided for non-MPI Frescox installation"
        raise ValueError(msg)
    if use_mpi:
        if not isinstance(mpi_setup, dict):
            raise TypeError("MPI setup information is not a dictionary")
        if MPI_N_PROCESSES not in mpi_setup:
            raise ValueError(f"{MPI_N_PROCESSES} not provided in MPI setup")

        n_mpi_procs = mpi_setup[MPI_N_PROCESSES]
        if not isinstance(n_mpi_procs, Integral):
            raise TypeError("Number of MPI processes must be an integer")
        if n_mpi_procs < 1:
            msg = "Number of MPI processes ({}) must be positive integer"
            raise ValueError(msg.format(n_mpi_procs))

    if not isinstance(filename, (str, PathLike)):
        raise TypeError(f"Invalid output filename ({filename})")

    if not isinstance(overwrite, bool):
        raise TypeError("Given overwrite argument is not a boolean")

    if not isinstance(cwd, (str, PathLike)):
        raise TypeError(f"Invalid working directory ({cwd})")
    fname_in = Path(cwd).resolve().joinpath("frescox.in")
    config.write_to_nml(fname_in, overwrite)

    # ----- CHECK STATE OF FILES & WRITE INPUT
    fname_out = Path(filename).resolve()
    if fname_out.exists():
        if overwrite:
            os.remove(fname_out)
        else:
            raise RuntimeError(f"Output file ({fname_out}) already exists")

    # ----- RUN SIMULATION
    if use_mpi:
        cmd = [
            "mpirun",
            "-np",
            str(n_mpi_procs),
            str(frescox_exe),
            str(fname_in),
        ]

        try:
            with open(fname_out, "w") as fptr_stdout:
                results = sbp.run(
                    cmd,
                    stdout=fptr_stdout,
                    stderr=sbp.STDOUT,
                    check=True,
                    cwd=cwd,
                )
            assert results.returncode == 0
        except sbp.CalledProcessError as err:
            print()
            msg = "Unable to run command (Return code {})"
            print(msg.format(err.returncode))
            print(" ".join(err.cmd))
            raise
    else:
        cmd = [str(frescox_exe)]

        try:
            with open(fname_out, "w") as fptr_stdout:
                with open(fname_in, "r") as fptr_stdin:
                    results = sbp.run(
                        cmd,
                        stdin=fptr_stdin,
                        stdout=fptr_stdout,
                        stderr=sbp.STDOUT,
                        check=True,
                        cwd=cwd,
                    )
            assert results.returncode == 0
        except sbp.CalledProcessError as err:
            print()
            msg = "Unable to run command (Return code {})"
            print(msg.format(err.returncode))
            print(" ".join(err.cmd))
            raise
