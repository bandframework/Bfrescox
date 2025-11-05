from os import PathLike
from pathlib import Path

import pandas as pd


def parse_fort16(filename: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    """
    Parse a |frescox| fort.16 output into a dict of DataFrames.  Each
    '@sN ... &' block becomes one entry labeled channel_N, with all
    numeric columns and proper names (Theta, sigma, iT11, etc.).

    Args:
        filename (str | PathLike[str]): Path to the |frescox| fort.16
                                        output file.

    Returns:
        dict[pd.DataFrame]: Dictionary with keys 'channel_1',
                            'channel_2', etc., each containing a
                            DataFrame of the corresponding data.

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
        content = f.read()
    raw_blocks = content.split("&")  # Split into blocks at "&"
    results = {}
    channel_idx = 1
    for block in raw_blocks:
        lines_all = block.splitlines()
        # Look for header line (columns after '#')
        header = None
        for line in lines_all:
            if line.strip().startswith("#") and "Theta" in line:
                # Remove "for projectile" etc. and split
                assert line.startswith("#")
                assert "for projectile" in line
                header = line.strip("# ").replace("for projectile", "").split()
                assert header is not None
                break
        # Collect numeric rows
        rows = []
        for line in lines_all:
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
            if header is not None and len(header) >= df.shape[1]:
                df.columns = header[: df.shape[1]]
            else:
                df.columns = [f"col_{i + 1}" for i in range(df.shape[1])]
            results[f"channel_{channel_idx}"] = df.reset_index(drop=True)
            channel_idx += 1
    return results
