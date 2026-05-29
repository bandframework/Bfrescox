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
MPI_LAUNCHER = "launcher"
MPI_LAUNCHER_ARGS = "launcher_args"
MPI_ENV = "env"


def _run_command(cmd, fname_out, cwd_path=None, env=None):
    try:
        with open(fname_out, "w") as fptr_stdout:
            results = sbp.run(
                cmd,
                stdin=sbp.DEVNULL,
                stdout=fptr_stdout,
                stderr=sbp.STDOUT,
                check=True,
                cwd=cwd_path,
                env=env,
            )
        assert results.returncode == 0
    except sbp.CalledProcessError as err:
        print()
        print(f"Unable to run command (Return code {err.returncode})")
        print(" ".join(err.cmd))
        print(f"Working directory: {cwd_path}")
        print(f"Output file: {fname_out}")

        if fname_out.exists():
            print()
            print("===== Captured frescox output =====")
            print(fname_out.read_text(errors="replace"))
            print("===== End captured frescox output =====")

        raise


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
    simulation configuration, and MPI setup.  Standard output and error are
    written to disk using the given output filename. Other outputs are written
    to disk based on the |frescox| output settings. The |frescox| Fortran
    namelist configuration file generated from the configuration object for the
    simulation is written alongside the results file.

    This function performs all of its own error checking of arguments.

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
            to write |frescox| stdout/stderr logging to
        overwrite (bool): If False, then an error is raised if either
            the input or output files exist
        mpi_setup (dict): Dictionary that provides MPI setup values if
            given |frescox| installation built with MPI; ``None``,
            otherwise.
        cwd (Union[str, PathLike]): pre-existing directory to run the simulation
            in.

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
    supports_mpi = frescox[FRESCOX_MPI_SUPPORT]
    use_omp = frescox[FRESCOX_OPENMP_SUPPORT]
    if not frescox_exe.is_file():
        msg = "Frescox executable does not exist or is not a file ({})"
        raise FileNotFoundError(msg.format(frescox_exe))
    if not isinstance(supports_mpi, bool):
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
    mpi_launcher = None
    mpi_launcher_args = []
    mpi_env = {}

    if (not supports_mpi) and (mpi_setup is not None):
        raise ValueError(
            "MPI specification provided for non-MPI Frescox installation"
        )

    run_with_mpi = supports_mpi and mpi_setup is not None

    if run_with_mpi:
        if not isinstance(mpi_setup, dict):
            raise TypeError("MPI setup information is not a dictionary")

        if MPI_N_PROCESSES not in mpi_setup:
            raise ValueError(f"{MPI_N_PROCESSES} not provided in MPI setup")

        n_mpi_procs = mpi_setup[MPI_N_PROCESSES]
        if not isinstance(n_mpi_procs, Integral):
            raise TypeError("Number of MPI processes must be an integer")
        if n_mpi_procs < 1:
            raise ValueError(
                f"Number of MPI processes ({n_mpi_procs}) must be positive"
            )

        mpi_launcher = mpi_setup.get(
            MPI_LAUNCHER,
            os.environ.get("BFRESCOX_MPIEXEC", "mpiexec"),
        )
        if not isinstance(mpi_launcher, str) or not mpi_launcher:
            raise TypeError(f"{MPI_LAUNCHER} must be a non-empty string")

        mpi_launcher_args = mpi_setup.get(MPI_LAUNCHER_ARGS, [])
        if not isinstance(mpi_launcher_args, list) or not all(
            isinstance(arg, str) for arg in mpi_launcher_args
        ):
            raise TypeError(f"{MPI_LAUNCHER_ARGS} must be a list of strings")

        mpi_env = mpi_setup.get(MPI_ENV, {})
        if not isinstance(mpi_env, dict) or not all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in mpi_env.items()
        ):
            raise TypeError(f"{MPI_ENV} must be a dict[str, str]")

    if not isinstance(filename, (str, PathLike)):
        raise TypeError(f"Invalid output filename ({filename})")
    fname_out = Path(filename).resolve()
    if fname_out.is_dir():
        raise IsADirectoryError(
            f"Output file ({fname_out}) corresponds to a pre-existing directory"
        )
    elif fname_out.exists():
        assert fname_out.is_file()
        if overwrite:
            os.remove(fname_out)
        else:
            raise FileExistsError(f"Output file ({fname_out}) already exists")

    if not isinstance(overwrite, bool):
        raise TypeError("Given overwrite argument is not a boolean")

    if not isinstance(cwd, (str, PathLike)):
        raise TypeError(f"Invalid working directory ({cwd})")
    cwd_path = Path(cwd).resolve()
    if not cwd_path.is_dir():
        raise NotADirectoryError(
            f"Working directory ({cwd}) does not exist or is not a directory"
        )

    # ----- WRITE INPUT
    fname_in = cwd_path.joinpath("frescox.in")
    config.write_to_nml(fname_in, overwrite)

    # ----- RUN SIMULATION
    env = os.environ.copy()

    if run_with_mpi:
        env.update(mpi_env)
    else:
        env = os.environ.copy()

    if mpi_setup is not None and not supports_mpi:
        raise ValueError("MPI setup provided for non-MPI Frescox installation")

    if run_with_mpi:
        cmd = [
            mpi_launcher,
            "-np",
            str(n_mpi_procs),
            *mpi_launcher_args,
            str(frescox_exe),
            str(fname_in),
        ]
    else:
        cmd = [
            str(frescox_exe),
            str(fname_in),
        ]

    _run_command(cmd, fname_out, cwd_path=cwd_path, env=env)
