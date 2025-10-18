import pandas as pd

from pathlib import Path


def read_fort16(path: Path) -> dict[str, pd.DataFrame]:
    """
    Parse a FrescoX fort.16 output into a dict of DataFrames.
    Each '@sN ... &' block becomes one entry labeled channel_N,
    with all numeric columns and proper names (Theta, sigma, iT11, etc.).
    """
    with open(path, "r") as f:
        content = f.read()
    raw_blocks = content.split("&")  # Split into blocks at "&"
    results = {}
    channel_idx = 1
    for block in raw_blocks:
        lines = block.splitlines()
        # Look for header line (columns after '#')
        header = None
        for line in lines:
            if line.strip().startswith("#") and "Theta" in line:
                # Remove "for projectile" etc. and split
                header = (
                    line.strip("# ").replace("for projectile", "").split()
                )
                break
        # Collect numeric rows
        rows = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith(("#", "@")):
                continue
            try:
                nums = [float(x) for x in line.split()]
                rows.append(nums)
            except ValueError:
                continue
        if rows:
            df = pd.DataFrame(rows)
            # Assign header if available and lengths match
            if header and len(header) >= df.shape[1]:
                df.columns = header[:df.shape[1]]
            else:
                df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
            results[f"channel_{channel_idx}"] = df.reset_index(drop=True)
            channel_idx += 1
    return results



# ---------- IO ----------

def read_results_lines(filename: Path) :
    if (not isinstance(filename, str)) and (not isinstance(filename, Path)):
        raise TypeError(f"Invalid filename ({filename})")
    path = Path(filename).resolve()
    if not path.is_file():
        raise ValueError(f"{path} does not exist or is not a file")
    with open(path, "r") as f:
        return f.readlines()

# ---------- Parsers ----------

def parallelization_setup(filename: Path):
    lines = read_results_lines(filename)  # assumes this helper exists

    MPI_START_STR = "Calculation with"
    OMP_START_STR = "Requested number of OpenMP threads:"

    mpi_n_found = 0
    mpi_n_procs = -1
    omp_n_found = 0
    omp_n_threads = -1
    omp_n_procs = -1

    for line in lines:
        if (line.strip().startswith(OMP_START_STR)):
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

        elif (line.strip().startswith(MPI_START_STR)):
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


def performance_results(filename: Path):
    lines = read_results_lines(filename)  # assumes helper exists

    START_STR = "Total CPU"
    COLUMNS = ["walltime_sec", "cpu_time_sec"]

    timings = []
    indices = []
    for line in lines:
        if (line.strip().startswith(START_STR)):
            result = line.strip().lstrip(START_STR).split()

            rank = int(result[0])
            assert result[1] == "time"
            assert result[2] == "="
            cpu_time_sec = float(result[3])

            n_items = len(result)
            if n_items == 5:
                # Serial or MPI
                assert result[4] == "seconds"
                wtime_sec = cpu_time_sec
            elif n_items == 12:
                # OpenMP or MPI+OpenMP result
                assert result[4] == "seconds,"
                assert result[5] == "Wall"
                assert result[6] == "time"
                assert result[7] == "="
                wtime_sec = float(result[8])
                assert result[9] == "seconds:"
                assert 0.0 <= float(result[10]) <= 100.0
                assert result[11] == "%"
            else:
                raise RuntimeError(f"Invalid performance result ({line})")

            assert rank >= 0
            assert wtime_sec > 0.0
            assert cpu_time_sec > 0.0

            indices.append(rank)
            timings.append((wtime_sec, cpu_time_sec))

    df = pd.DataFrame(data=timings, index=indices, columns=COLUMNS)
    df.index.name = "rank"
    # TODO: Some timing lines aren't printed on their own line.
    # Put in NaNs.

    return df


def cross_sections_mbsr(filename:Path):
    lines = read_results_lines(filename)

    index = []
    ratio = []
    for line in lines:
        if ('X-S' in line):
            result = line.split()
            # Sanity check parsing including expected units
            assert len(result) == 6
            assert result[1].strip() == "deg.:"
            assert result[2].strip() == "X-S"
            assert result[3].strip() == "="
            assert result[5].strip() == "mb/sr,"
            index.append(float(result[0]))
            ratio.append(float(result[4]))

    df = pd.DataFrame(data=ratio, index=index,
                      columns=["sigma_omega_ratio"])
    df.index.name = "degree"

    return df


def cross_sections_R2R(filename: Path):
    lines = read_results_lines(filename)

    index = []
    Rutherford = []
    for i, line in enumerate(lines):
        if "/R" in line:
            assert "X-S" in lines[i-1]
            result = lines[i-1].split()
            assert len(result) == 6
            index.append(float(result[0]))
            assert result[1].strip() == "deg.:"
            assert result[2].strip() == "X-S"
            assert result[3].strip() == "="
            float(result[4])
            assert result[5].strip() == "mb/sr,"

            result = line.split()
            assert len(result) == 4
            assert result[0].strip() == "+"
            assert result[1].strip() == "/R"
            assert result[2].strip() == "="
            Rutherford.append(float(result[3]))

    df = pd.DataFrame(data=Rutherford, index=index,
                      columns=["Rutherford"])
    df.index.name = "degree"

    return df
