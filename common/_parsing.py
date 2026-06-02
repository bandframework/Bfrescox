"""
Internal parsing functions for |frescox| output files
"""

from os import PathLike
from pathlib import Path
from typing import Union


def _read_results_lines(filename: Union[str, PathLike]) -> list[str]:
    """
    Read all lines from a |frescox| results file.

    Args:
        filename (Union[str, PathLike]): Path to the |frescox| results
            file.

    Returns:
        List[str]: lines of the file.

    Raises:
        TypeError: If filename is not a string or Path.
        ValueError: If the file does not exist.
    """
    if not isinstance(filename, (str, PathLike)):
        raise TypeError(f"Invalid filename ({filename})")
    fname = Path(filename).resolve()
    if not fname.is_file():
        raise FileNotFoundError(f"{fname} does not exist or is not a file")
    with open(fname, "r") as f:
        return f.readlines()
