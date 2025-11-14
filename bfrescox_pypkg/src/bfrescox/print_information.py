import os
import shutil
import warnings
import platform

import subprocess as sbp

from .information import information
from ._run_frescox_simulation import FRESCOX_EXE


def print_information():
    """
    Print information about the |frescox| executable used internally by the
    package.

    If ``otool`` is installed in macOS systems or ``ldd`` in unix-based systems,
    then |frescox| external dependences are listed.
    """
    built_with = information()
    if built_with:
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
                        check=True,
                    )
                    stdout = reply.stdout.decode()
                    assert stdout != ""
                    # This prints the binary's name
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
            print(frescox_exe)
            if shutil.which("ldd", mode=(os.F_OK | os.X_OK)):
                try:
                    reply = sbp.run(
                        ["ldd", str(frescox_exe)],
                        capture_output=True,
                        check=True,
                    )
                    stdout = reply.stdout.decode()
                    assert stdout != ""
                    print(stdout)
                    assert reply.returncode == 0
                    assert reply.stderr.decode() == ""
                except Exception:
                    msg = "Unable to get external dependence info with ldd"
                    warnings.warn(msg)
        else:
            print(frescox_exe)
    else:
        # This is **not** necessarily an error since this package allows for
        # "hollow" installations.
        warnings.warn("Internal Frescox executable is missing")
