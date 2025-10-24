import re
from pathlib import Path

import numpy as np


def parse_valid_keys(
    template_path: Path,
):
    """
    Read in a template nml file, identify all '@key@' placeholders, and return
    a set of the keys found.

    Parameters:
        template_path (Path): Path to the template NML file.

    Returns:
        Set of keys found in the template file.
    """

    with open(template_path, "r") as fptr:
        input_nml = fptr.readlines()

    to_replace = set()
    for line in input_nml:
        matches = np.array(re.findall(r"@(\w+)@", line))
        if matches is not None and len(matches) > 0:
            to_replace.update([match.lstrip("@").rstrip("@") for match in matches])

    return to_replace


def fill_in_template_file(
    template_path: Path,
    output_path: Path,
    parameters: dict,
    overwrite: bool = False,
):
    """
    Read in a template nml file, replace '@key@' placeholders with corresponding
    values from parameters, and write result to output_path.

    For example, if one has a Frescox template file with a line like this:
    ```
    &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
    ```

    Then the `parameters` dict should have the keys `V`, `r`, `a`, `W`, `rw`, and `aw`.

    Placeholders may be repeated in multiple places in the template file. For example,
    `@V@` may appear multiple times; all instances will be replaced with the value of
    `parameters['V']`.

    Parameters:
        template_path (Path): Path to the template NML file.
        output_path (Path): Path to write the modified NML file.
        parameters (dict): Dictionary of parameters to replace in the template. Keys
            should match placeholders in the template, corresponding values are
            the desired replacements in the output file.
        overwrite (bool): Whether to overwrite output_path if it already exists.

    Raises:
        ValueError: If keys exist in the template that are not in `parameters`.
        ValueError: If keys exist in `parameters` that are not in the template file
    """

    with open(template_path, "r") as fptr:
        input_nml = fptr.readlines()
    valid_keys = parse_valid_keys(template_path)

    if Path(output_path).exists() and (not overwrite):
        raise RuntimeError(f"{output_path} already exists")

    to_replace = [f"@{p}@" for p in parameters.keys()]
    replaced_keys = set()
    with open(output_path, "w") as fptr:
        for line in input_nml:
            updated = line
            for key in to_replace:
                if key in line:
                    name = key.lstrip("@").rstrip("@")
                    replaced_keys.add(name)
                    updated = updated.replace(key, str(parameters[name]))
            fptr.write(updated)

    keys_not_replaced = set(parameters.keys()) - replaced_keys
    if len(keys_not_replaced) > 0:
        raise ValueError(
            f"Keys {keys_not_replaced} were in `parameters` but were not found in "
            f"template file {template_path}"
        )
    keys_not_in_parameters = valid_keys - set(parameters.keys())
    if len(keys_not_in_parameters) > 0:
        raise ValueError(
            f"Keys {keys_not_in_parameters} were found in template file {template_path}"
            "but were not in `parameters`"
        )
