from os import PathLike
from pathlib import Path
from typing import Union

import pandas as pd


def parse_fort16(filename: Union[str, PathLike]) -> dict[str, pd.DataFrame]:
    """
    Parse out scattering cross sections results from the given |frescox|
    ``fort.16`` output file.  Each '@sN ... &' block becomes one entry labeled
    'channel_N', with all numeric columns and proper names ('Theta', 'sigma',
    'iT11', etc.).

    .. todo::
        * Convert asserts to error messages where we might be surprised by
          different formatting.
        * Parse out (Partition, Excit, near/far) information for each data
          block for testing.  Consider using that so that we can return a single
          DataFrame with a MultiIndex.  If not, should the index of the
          DataFrames be the angle Theta?
        * It looks like we should always expect to get Theta and sigma data.
          Should the column names for those include the units, which we are
          sanity checking here?

    Args:
        filename:
            Path to the |frescox| ``fort.16`` output file

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
        # Split into blocks at "&"
        raw_blocks = f.read().split("&")

    results = {}
    channel_idx = 1
    for block in raw_blocks:
        lines_all = block.splitlines()

        # Strip off blank line at end associated with &
        assert lines_all[-1].strip() == ""
        lines_all = lines_all[:-1]

        # Look for header information that indicates that block contains cross
        # section data
        header = []
        has_correct_xaxis = False
        has_correct_yaxis = False
        for hdr_index, line in enumerate(lines_all):
            line_clean = line.strip()
            if line_clean.startswith("@xaxis"):
                # This has the benefit of confirming units
                expected = ['label', '"Scattering', 'angle', '(degrees)"']
                axis_info = line_clean.lstrip("@xaxis").strip().split()
                has_correct_xaxis = (axis_info == expected)
            elif line_clean.startswith("@yaxis"):
                # This has the benefit of confirming units
                expected = ['label', '"Cross', 'section', '(mb/sr)"']
                axis_info = line_clean.lstrip("@yaxis").strip().split()
                has_correct_yaxis = (axis_info == expected)
            elif line_clean.startswith("#") and "Theta" in line_clean:
                assert line_clean.endswith("for projectile")
                line_stripped = line_clean.lstrip("#").rstrip("for projectile")
                header = line_stripped.strip().split()
                assert header[0] == "Theta"
                assert header[1] == "sigma"
                # We expect the xaxis and yaxis lines to appear, if at all,
                # before the header line.  So we are OK to break out of this
                # loop.
                break

        # We are only expecting cross section data for now.
        if not header:
            assert block.strip() == ""
            continue

        # x and y axis information is only printed with the first block holding
        # cross section data.
        if not results:
            assert has_correct_xaxis
            assert has_correct_yaxis
            assert hdr_index == 11
        else:
            assert not has_correct_xaxis
            assert not has_correct_yaxis
            assert hdr_index == 4

        # We expect numeric data only after the header line and on each line
        rows = []
        n_elements = -1
        for i, line in enumerate(lines_all):
            line_clean = line.strip()

            if i <= hdr_index:
                assert not line_clean or line_clean.startswith(("#", "@"))
                continue

            try:
                nums = [float(x) for x in line_clean.split()]
                if n_elements <= 0:
                    n_elements = len(nums)
                    assert n_elements > 0
                assert len(nums) == n_elements
                rows.append(nums)
            except ValueError as exc:
                raise ValueError(
                    f"Error parsing cross section data in {filename}"
                ) from exc
        assert rows

        df = pd.DataFrame(rows)

        # Frescox can print out more column names than columns of data
        assert len(header) >= df.shape[1]
        df.columns = header[:df.shape[1]]
        results[f"channel_{channel_idx}"] = df.reset_index(drop=True)

        channel_idx += 1

    return results
