import os
import shutil
import warnings
import platform

import subprocess as sbp

from .information import information
from ._run_frescox_simulation import (
    FRESCOX_EXE,
    FRESCOX_MPI_SUPPORT, FRESCOX_OPENMP_SUPPORT,
    FRESCOX_LAPACK_SUPPORT,
    FRESCOX_COREX_SUPPORT
)


def print_information():
    """
    Print information about the |frescox| executables used internally by the
    package.

    If ``otool`` is installed in macOS systems or ``ldd`` in unix-based systems,
    then |frescox| external dependences are listed.
    """
    built_with = information()
    frescox_exe = built_with[FRESCOX_EXE]

    os_name = platform.system()

    print("Frescox executable")
    print("-" * 80)
    if os_name.lower() == "darwin":
        if shutil.which("otool", mode=(os.F_OK | os.X_OK)):
            try:
                reply = sbp.run(
                    ["otool", "-L", str(frescox_exe)],
                    capture_output=True,
                    check=True
                )
                stdout = reply.stdout.decode()
                assert stdout != ""
                print(stdout)
                assert reply.returncode == 0
                assert reply.stderr.decode() == ""
            except Exception:
                print(frescox_exe)
                msg = "Unable to get external dependence info with otool"
                warnings.warn(msg)
        else:
            print(frescox_exe)
    elif os_name.lower() == "linux":
        if shutil.which("ldd", mode=(os.F_OK | os.X_OK)):
            try:
                reply = sbp.run(
                    ["ldd", str(frescox_exe)],
                    capture_output=True,
                    check=True
                )
                stdout = reply.stdout.decode()
                assert stdout != ""
                print(frescox_exe)
                print(stdout)
                assert reply.returncode == 0
                assert reply.stderr.decode() == ""
            except Exception:
                print(frescox_exe)
                msg = "Unable to get external dependence info with ldd"
                warnings.warn(msg)
        else:
            print(frescox_exe)
    else:
        print(frescox_exe)

    print()
    if built_with[FRESCOX_MPI_SUPPORT]:
        print("\tBuilt with MPI")
    else:
        print("\tNo MPI parallelization")
    if built_with[FRESCOX_OPENMP_SUPPORT]:
        print("\tBuilt with OpenMP support")
    else:
        print("\tNo OpenMP parallelization")
    if built_with[FRESCOX_LAPACK_SUPPORT]:
        print("\tBuilt with external BLAS/LAPACK")
    else:
        print("\tBuilt with internal BLAS/LAPACK")
    if built_with[FRESCOX_COREX_SUPPORT]:
        print("\tBuilt with corex capabilities")
    else:
        print("\tNo corex capablilities")
