"""
Utilities for parsing FrescoX performance results into a DataFrame.
"""

from pathlib import Path

import pandas as pd

from _parsing import _read_results_lines


def performance_results(filename: Path):
    """
    Parse FrescoX performance results into a DataFrame.

    Parameters:
    filename : Path
        Path to the FrescoX output file.

    Returns:
    pd.DataFrame
        DataFrame with index as rank and columns 'walltime_sec' and 'cpu_time_sec'.

    Raises:
    RuntimeError
        If an invalid performance result line is encountered.
    """
    lines = _read_results_lines(filename)

    START_STR = "Total CPU"
    COLUMNS = ["walltime_sec", "cpu_time_sec"]

    timings = []
    indices = []
    for line in lines:
        if line.strip().startswith(START_STR):
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
