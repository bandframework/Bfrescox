import csv
from os import PathLike
from typing import Union
from pathlib import Path

from ._run_frescox_simulation import (
    FRESCOX_COREX_SUPPORT,
    FRESCOX_EXE,
    FRESCOX_LAPACK_SUPPORT,
    FRESCOX_MPI_SUPPORT,
    FRESCOX_OPENMP_SUPPORT,
)


def _load_build_information(src_path: Union[str, PathLike]) -> dict:
    """
    Load all information related to the internal |frescox| installation.

    Args:
        src_path (Union[str, PathLike]): Path to folder that contains the
            ``bin`` and ``build`` installation folders.
    Returns:
        dict : contains information regarding the |frescox| executable
            used by the package.  An empty ``dict`` indicates that no
            valid internal |frescox| installation was found.
    """

    if not isinstance(src_path, (str, PathLike)):
        raise TypeError(
            f"Expected 'src_path' to be of type 'str' or 'PathLike[str]', "
            f"got '{type(src_path)}'"
        )

    src_path = Path(src_path).resolve()

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
