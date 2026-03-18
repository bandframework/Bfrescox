from os import PathLike
from pathlib import Path
from typing import Union

import pandas as pd


def parse_fort16(filename: Union[str, PathLike]) -> dict[str, pd.DataFrame]:
    """
    Parse a |frescox| fort.16 output into a dict of DataFrames.  Each
    '@sN ... &' block becomes one entry labeled 'channel_N', with all
    numeric columns and proper names ('Theta', 'sigma', 'iT11', etc.).

    .. todo::
        Should the index of the DataFrames be the angle Theta?

    Args:
        filename:
            Path to the |frescox| fort.16 output file.

    Returns:
        Dictionary with keys 'channel_1', 'channel_2', etc., each containing a
        DataFrame of the corresponding data.  If no valid data blocks are found,
        returns an empty dictionary.
    """
    if not isinstance(filename, (str, PathLike)):
        raise TypeError(f"Invalid filename ({filename})")
    path = Path(filename).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"{path} does not exist or is not a file")
    with open(path, "r") as f:
        content = f.read()
    raw_blocks = content.split("&")  # Split into blocks at "&"
    results = {}
    channel_idx = 1
    for block in raw_blocks:
        lines_all = block.splitlines()
        # Look for header line (columns after '#')
        header = None
        for line in lines_all:
            line_clean = line.strip()
            if line_clean.startswith("#") and "Theta" in line_clean:
                # Remove "for projectile" etc. and split
                assert line_clean.endswith("for projectile")
                line_stripped = line_clean.lstrip("#").rstrip("for projectile")
                header = line_stripped.strip().split()
                assert header[0] == "Theta"
                break
        # Collect numeric rows
        rows = []
        n_elements = -1
        for line in lines_all:
            line_clean = line.strip()
            if not line_clean or line_clean.startswith(("#", "@")):
                continue
            try:
                nums = [float(x) for x in line_clean.split()]
                if n_elements <= 0:
                    n_elements = len(nums)
                assert len(nums) > 0
                assert len(nums) == n_elements
                rows.append(nums)
            except ValueError:
                continue
        if rows:
            df = pd.DataFrame(rows)
            # Assign header if available and lengths match
            if header is not None and len(header) >= df.shape[1]:
                df.columns = header[: df.shape[1]]
            else:
                df.columns = [f"col_{i + 1}" for i in range(df.shape[1])]
            results[f"channel_{channel_idx}"] = df.reset_index(drop=True)
            channel_idx += 1

    return results
