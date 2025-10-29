import csv

# TODO: This assumes in a package
from ._run_frescox_simulation import (
    FRESCOX_EXE,
    FRESCOX_MPI_SUPPORT,
    FRESCOX_OPENMP_SUPPORT,
    FRESCOX_LAPACK_SUPPORT,
    FRESCOX_COREX_SUPPORT,
)


def load_build_information(src_path):
    """
    This function is written under the assumption that it is integrated in and
    being called through a package.  It, therefore, can **not** be called as a
    standalone function.

    Load all information related to the internal |frescox| installation.

    .. todo::
        * Ok that this isn't a standalone since it is explicitly getting
          information about an installation in a package?

    :param src_path: Path to folder that contains the ``bin`` and ``build``
        installation folders
    :return: ``dict`` that contains information regarding the |frescox|
        executable used by the package.  An empty ``dict`` indicates that no
        valid internal |frescox| installation was found.
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
    elif not BUILD_INFO.is_file():
        raise RuntimeError(f"{BUILD_INFO} is not a file")
    elif not EXE_PATH.is_file():
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
