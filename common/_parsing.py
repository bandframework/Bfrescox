"""
Internal parsing functions for FrescoX output files
"""

from pathlib import Path


def _read_results_lines(filename: Path):
    """
    Read all lines from a FrescoX results file.

    Parameters:
    filename : Path
        Path to the FrescoX results file.

    Returns:
    list of str
        Lines of the file.

    Raises:
    TypeError: If filename is not a string or Path.
    ValueError: If the file does not exist.
    """
    if (not isinstance(filename, str)) and (not isinstance(filename, Path)):
        raise TypeError(f"Invalid filename ({filename})")
    path = Path(filename).resolve()
    if not path.is_file():
        raise ValueError(f"{path} does not exist or is not a file")
    with open(path, "r") as f:
        return f.readlines()
