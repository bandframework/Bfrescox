"""
Functions to parse differential cross section results from |frescox|
stdout. This module is part of the package public interface, so they can
be called like so `bfrescox.parse_differential_xs.<function in this
file>(filename)`.
"""

from os import PathLike

import pandas as pd

from ._parsing import _read_results_lines


def absolute_mb_per_sr(filename: str | PathLike[str]) -> pd.DataFrame:
    """
    Parse the absolute cross section (mb/sr) from a |frescox| results
    file.

    Args:
        filename  (str | PathLike[str]): Path to the |frescox| results file.

    Returns:
        pd.DataFrame: DataFrame with degree as index and absolute cross
        section as column.

    Raises:
        TypeError: If filename is not a string or Path.
        ValueError: If the file does not exist.
    """

    lines_all = _read_results_lines(filename)

    index = []
    ratio = []
    for line in lines_all:
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

    df = pd.DataFrame(
        data=ratio, index=index, columns=["differential_xs_absolute_mb_per_sr"]
    )
    df.index.name = "angle_degrees"

    return df


def ratio_to_rutherford(filename: str | PathLike[str]) -> pd.DataFrame:
    """
    Parse the ratio to Rutherford cross section from a |frescox| results
    file.

    Args:
        filename  (str | PathLike[str]): Path to the |frescox| results file.

    Returns:
        pd.DataFrame: DataFrame with degree as index and Rutherford
        ratio as column.

    Raises:
        TypeError: If filename is not a string or Path.
        ValueError: If the file does not exist.
    """
    lines_all = _read_results_lines(filename)

    index = []
    ratio = []
    for i, line in enumerate(lines_all):
        if "/R" in line:
            assert "X-S" in lines_all[i - 1]
            result = lines_all[i - 1].split()
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
            ratio.append(float(result[3]))

    df = pd.DataFrame(
        data=ratio,
        index=index,
        columns=["differential_xs_ratio_to_rutherford"],
    )
    df.index.name = "angle_degrees"

    return df
