"""
Parse differential cross section results from FrescoX output files.
"""

from pathlib import Path

import pandas as pd

from _parsing import _read_results_lines


def absolute_mb_per_sr(filename: Path):
    """
    Parse the absolute cross section (mb/sr) from a FrescoX results file.

    Parameters:
    filename : Path
        Path to the FrescoX results file.
    Returns:
        pd.DataFrame: DataFrame with degree as index and absolute cross section as column.
    """
    lines = _read_results_lines(filename)

    index = []
    ratio = []
    for line in lines:
        if "X-S" in line:
            result = line.split()
            # Sanity check parsing including expected units
            assert len(result) == 6
            assert result[1].strip() == "deg.:"
            assert result[2].strip() == "X-S"
            assert result[3].strip() == "="
            assert result[5].strip() == "mb/sr,"
            index.append(float(result[0]))
            ratio.append(float(result[4]))

    df = pd.DataFrame(data=ratio, index=index, columns=["sigma_omega_ratio"])
    df.index.name = "degree"

    return df


def ratio_to_rutherford(filename: Path):
    """
    Parse the ratio to Rutherford cross section from a FrescoX results file.

    Parameters:
    filename : Path
        Path to the FrescoX results file.
    Returns:
        pd.DataFrame: DataFrame with degree as index and Rutherford ratio as column.
    """
    lines = _read_results_lines(filename)

    index = []
    Rutherford = []
    for i, line in enumerate(lines):
        if "/R" in line:
            assert "X-S" in lines[i - 1]
            result = lines[i - 1].split()
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

    df = pd.DataFrame(data=Rutherford, index=index, columns=["Rutherford"])
    df.index.name = "degree"

    return df
