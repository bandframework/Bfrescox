import csv
from pathlib import Path

from ._run_frescox_simulation import (
    FRESCOX_COREX_SUPPORT,
    FRESCOX_EXE,
    FRESCOX_LAPACK_SUPPORT,
    FRESCOX_MPI_SUPPORT,
    FRESCOX_OPENMP_SUPPORT,
)


def _load_build_information(src_path: Path) -> dict:
    """
    Load all information related to the internal |frescox| installation.

    Parameters:
        src_path : ``pathlib.Path``
            Path to folder that contains the ``bin`` and ``build``
            installation folders.
    Returns:
        dict
            ``dict`` that contains information regarding the |frescox|
            executable used by the package.  An empty ``dict`` indicates
            that no valid internal |frescox| installation was found.
    """
    EXE_PATH = src_path.joinpath("bin", "frescox")
    BUILD_INFO = src_path.joinpath("build", "build_info.csv")

    EXPECTED_KEYS = {
        FRESCOX_MPI_SUPPORT,
        FRESCOX_OPENMP_SUPPORT,
        FRESCOX_LAPACK_SUPPORT,
        FRESCOX_COREX_SUPPORT,
    }

    if (not BUILD_INFO.exists()) or (not EXE_PATH.exists()):
        return {}
    if not BUILD_INFO.is_file():
        raise RuntimeError(f"{BUILD_INFO} is not a file")
    if not EXE_PATH.is_file():
        raise RuntimeError(f"{EXE_PATH} is not a file")

    built_with = {}
    with open(BUILD_INFO, "r") as fptr:
        reader = csv.reader(fptr, delimiter=" ")
        for line in reader:
            key, value = [each for each in line if each != ""]
            assert key not in built_with
            assert isinstance(value, str)
            assert value.lower() in ["true", "false"]
            built_with[key] = value.lower() == "true"

    assert set(built_with) == EXPECTED_KEYS
    built_with[FRESCOX_EXE] = EXE_PATH

    return built_with
