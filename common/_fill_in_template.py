"""
Module to fill in template NML files with specified parameters.
"""

import re
from os import PathLike
from pathlib import Path
from typing import Union

import numpy as np

from ._parsing import _read_results_lines


def parse_valid_keys(template_path: Union[str, PathLike]):
    """
    Read in a template nml file, identify all '@key@' placeholders, and
    return a set of the keys found.

    Args:
        template_path (Union[str, PathLike]): Path to the template NML
            file.

    Returns:
        Set of keys found in the template file.
    """
    input_nml = _read_results_lines(template_path)

    to_replace = set()
    for line in input_nml:
        matches = np.array(re.findall(r"@(\w+)@", line))
        if matches is not None and len(matches) > 0:
            to_replace.update(
                [match.lstrip("@").rstrip("@") for match in matches]
            )

    return to_replace


def fill_in_template_file(
    template_path: Union[str, PathLike],
    output_path: Union[str, PathLike],
    parameters: dict,
    overwrite: bool,
):
    """
    Read in a template nml file, replace '@key@' placeholders with
    corresponding values from `parameters`, and write result to
    `output_path`. The set of possible keys in the template file must
    exactly match the keys in `parameters`, or a ValueError will be
    raised.

    For example, if one has a |frescox| template file with a line like
    this defining a potential:
    ```
    &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
    &POT kp=1 type=2  p1=@Vs@ p2=@rw@ p3=@aw@ p4=@Ws@ p5=@rw@ p6=@aw@ /
    ```

    Then the `parameters` dict should have the keys `V`, `r`, `a`,
    `W`, `rw`, `aw`, `Vs` and `Ws`. Notice that `rw` and `aw` are
    used in multiple places in the template file. The corresponding
    values in `parameters` will be substituted into each location
    where the placeholder appears.

    .. todo::
        * This has hardcoded formatting for writing parameter values to file.
        As with template generation, this package should not pretend to know
        what precision is needed by all applications.  Rather, it should write
        all values in full precision.
        * Should all parameter values always be written as floats?

    Args:
        template_path (Union[str, PathLike]): Path to the template NML
            file.
        output_path (Union[str, PathLike]): Path to write the modified
            NML file.
        parameters (dict): Dictionary of parameters to replace in
            the template. Keys should match placeholders in the
            template, but should not include the `@` characters.
            Corresponding values are the desired replacements
            in the output file.
        overwrite (bool): Whether to overwrite output_path if it already
            exists.

    Raises:
        ValueError: If keys in template file do not match keys in
            `parameters`.
        RuntimeError: If output_path already exists and overwrite is
            False.
    """
    valid_keys = parse_valid_keys(template_path)
    if valid_keys != set(parameters.keys()):
        raise ValueError(
            f"Keys in template file {template_path} do not "
            "match keys in `parameters`:\n"
            "  Keys that are in template but not in parameters:"
            f" {valid_keys - set(parameters.keys())}\n"
            "  Keys that are in parameters but not in template:"
            f" {set(parameters.keys()) - valid_keys}"
        )

    if not isinstance(output_path, (str, PathLike)):
        raise TypeError("output_path must be str or PathLike")

    fname_out = Path(output_path).resolve()
    if fname_out.is_dir():
        raise IsADirectoryError(
            f"Filename ({fname_out}) corresponds to pre-existing directory"
        )
    elif fname_out.exists() and (not overwrite):
        raise FileExistsError(f"{fname_out} already exists")

    input_nml = _read_results_lines(template_path)

    to_replace = [f"@{p}@" for p in parameters.keys()]
    with open(fname_out, "w") as fptr:
        for line in input_nml:
            updated = line
            for key in to_replace:
                if key in line:
                    name = key.lstrip("@").rstrip("@")
                    updated = updated.replace(key, f"{parameters[name]:1.9f}")
            fptr.write(updated)
