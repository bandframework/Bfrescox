import os
import subprocess as sbp
from numbers import Integral
from pathlib import Path

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


def _run_frescox_simulation(frescox, config, mpi_setup, filename, overwrite, cwd=None):
    """
    Run a |frescox| simulation using the given |frescox| installation,
    simulation configuration, and MPI setup.  Results are written to
    disk using the given output filename.  The |frescox| Fortran
    namelist configuration file generated from the configuration object
    for the simulation is written alongside the results file.

    While this function will likely reside in the private interface of
    Python packages, we assume that some users might call it directly.
    Therefore, this function performs its own error checking of
    arguments.  A nice side effect of this is that the wrapper functions
    in the packages likely don't need to perform any error checking.

    :param frescox: ``dict`` that fully characterizes a |frescox|
        installation
    :param config: |bfrescox| :py:class:`Configuration` object that
        specifies the simulation to execute
    :param mpi_setup: ``dict`` that provides MPI setup values if given
        |frescox| installation built with MPI; ``None``, otherwise.
    :param filename: Filename including path of file to write outputs to
    :param overwrite: If False, then an error is raised if either the
        input or output files exist
    :params cwd: Current working directory to run the simulation in.  If
        None, the current working directory of the calling process is used.
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
    elif not isinstance(use_mpi, bool):
        raise TypeError("MPI support specification is not a boolean")
    elif not isinstance(use_omp, bool):
        raise TypeError("OpenMP support specification is not a boolean")
    elif use_omp and ("OMP_NUM_THREADS" not in os.environ):
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
    elif use_mpi:
        if not isinstance(mpi_setup, dict):
            raise TypeError("MPI setup information is not a dictionary")
        elif MPI_N_PROCESSES not in mpi_setup:
            raise ValueError(f"{MPI_N_PROCESSES} not provided in MPI setup")

        n_mpi_procs = mpi_setup[MPI_N_PROCESSES]
        if not isinstance(n_mpi_procs, Integral):
            raise TypeError("Number of MPI processes must be an integer")
        elif n_mpi_procs < 1:
            msg = "Number of MPI processes ({}) must be positive integer"
            raise ValueError(msg.format(n_mpi_procs))

    if not isinstance(filename, (str, Path)):
        raise TypeError(f"Invalid output filename ({filename})")

    if not isinstance(overwrite, bool):
        raise TypeError("Given overwrite argument is not a boolean")

    # ----- CHECK STATE OF FILES & WRITE INPUT
    fname_out = Path(filename).resolve()
    if fname_out.exists():
        if overwrite:
            os.remove(fname_out)
        else:
            raise RuntimeError(f"Output file ({fname_out}) already exists")

    if cwd is None:
        cwd = Path.cwd()
    elif not isinstance(cwd, (str, Path)):
        raise TypeError(f"Invalid working directory ({cwd})")
    fname_in = Path(cwd).resolve().joinpath("frescox.in")
    config.write_to_nml(fname_in, overwrite)

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
