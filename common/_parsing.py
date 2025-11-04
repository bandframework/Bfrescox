"""
Internal parsing functions for |frescox| output files
"""

from os import PathLike
from pathlib import Path


def _read_results_lines(filename: str | PathLike[str]) -> list[str]:
    """
    Read all lines from a |frescox| results file.

    Args:
        filename (str | PathLike[str]): Path to the |frescox| results
            file.

    Returns:
        List[str]: lines of the file.

    Raises:
        TypeError: If filename is not a string or Path.
        ValueError: If the file does not exist.
    """
    if not isinstance(filename, (str, PathLike)):
        raise TypeError(f"Invalid filename ({filename})")
    path = Path(filename).resolve()
    if not path.is_file():
        raise ValueError(f"{path} does not exist or is not a file")
    with open(path, "r") as f:
        return f.readlines()
