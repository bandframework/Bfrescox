from pathlib import Path

from _parsing import _read_results_lines


def parallelization_setup(filename: Path):
    """
    Parse FrescoX parallelization setup from output file.
    Parameters:
    filename : Path
        Path to the FrescoX output file.

    Returns:
    tuple or None
        If parallelization info is found, returns a tuple (n_mpi_procs, n_threads),
        where n_threads is -1 for pure MPI runs. If no parallelization info is found,
        returns None.
    Raises:
    RuntimeError
        If an invalid parallelization logging is encountered.
    """
    lines = _read_results_lines(filename)

    MPI_START_STR = "Calculation with"
    OMP_START_STR = "Requested number of OpenMP threads:"

    mpi_n_found = 0
    mpi_n_procs = -1
    omp_n_found = 0
    omp_n_threads = -1
    omp_n_procs = -1

    for line in lines:
        if line.strip().startswith(OMP_START_STR):
            omp_n_found += 1

            result = line.strip().lstrip(OMP_START_STR).split()
            assert len(result) == 19
            omp_n_threads = int(result[0])
            assert result[1] == "(out"
            assert result[2] == "of"
            assert result[3] == "node"
            assert result[4] == "limit"
            assert result[5] == "of"
            assert int(result[6]) >= 1
            assert result[7] == "processors)"
            assert result[8] == "in"
            assert result[9] == "each"
            assert result[10] == "of"
            omp_n_procs = int(result[11])
            assert result[12] == "MPI"
            assert result[13] == "sets"
            assert result[14] == "with"
            assert int(result[15]) == 1
            assert result[16] == "helpers"
            assert result[17] == "per"
            assert result[18] == "set"

            assert omp_n_threads >= 1
            assert omp_n_procs >= 1

        elif line.strip().startswith(MPI_START_STR):
            mpi_n_found += 1

            result = line.strip().lstrip(MPI_START_STR).split()
            assert len(result) == 8
            mpi_n_procs = int(result[0])
            assert result[1] == "MPI"
            assert result[2] == "nodes"
            assert result[3] == "and"
            assert result[4] == "temporary"
            assert result[5] == "files"
            assert result[6] == "in"

            assert mpi_n_procs >= 1

    if (mpi_n_found == 0) and (omp_n_found == 0):
        return None
    elif omp_n_found == 1:
        assert mpi_n_found in [0, 1]
        if mpi_n_found == 1:
            assert mpi_n_procs == omp_n_procs
        n_threads = omp_n_threads
        n_mpi_procs = omp_n_procs
    elif mpi_n_found == 1:
        assert omp_n_found == 0
        n_threads = -1
        n_mpi_procs = mpi_n_procs
    else:
        raise RuntimeError("Invalid parallelization logging")

    return n_mpi_procs, n_threads
