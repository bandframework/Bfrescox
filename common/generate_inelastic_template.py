import re
from fractions import Fraction
from os import PathLike
from pathlib import Path
from typing import List, Union

import numpy as np

from ._utils import _validate_spin

TEMPLATE_FILE_PATH = Path(__file__).parent / "templates/inelastic.template"


def _expand_type11_pX(text: str, L_list) -> str:
    """
    For each line like:
      &POT kp=1 type=11          pX=DELTA_LAMBDA_X /
    replace with:
      &POT kp=1 type=11 p0=@delta_0@ p2=@delta_2@ ... /
        (for 0, 2, ... in L_list)

    Args:
        text (str): The original template content as a string.
        L_list (List[int]): List of multipole transition orders.

    Returns:
        str: The modified template content with expanded &POT lines.
    """
    if not L_list:
        return text
    parts = " ".join(f"p{int(L)}=@delta_{int(L)}@" for L in L_list)
    pattern = re.compile(
        r"(?m)^\s*&POT\s+kp=1\s+type=11\b.*\bpX=DELTA_LAMBDA_X\s*/\s*$"
    )
    return pattern.sub(f"&POT kp=1 type=11 {parts} /", text)


def _setup_inelastic_system_template(
    template: str, values_et: np.ndarray, values_jt: np.ndarray, bandt_vals
) -> str:
    """
    Modify the template content in memory with new &STATES sections.
    This ensures that the placeholder line for &STATES is removed and
    replaced.

    Args:
        template (str): The original template content as a string.
        values_et (np.ndarray): Array of excitation energies for the
            target states.
        values_jt (np.ndarray): Array of total angular momenta for the
            target states.
        bandt_vals (np.ndarray): Array of parity values for the target
            states (1 for positive, 0 for negative).

    Returns:
        str: The modified template content with updated &STATES
            sections.
    """
    # Split the template into lines for easier manipulation
    lines = template.splitlines()

    # Remove any placeholder lines containing the original &STATES placeholder
    placeholder_pattern = "&STATES copyp=1"
    lines = [line for line in lines if placeholder_pattern not in line]

    # Generate the dynamic &STATES section

    dynamic_section = "".join(
        f"&STATES copyp=1 cpot=1 "
        f"jt={float(jt):.1f} "
        f"bandt={int((-1) ** int(parity + 1)):d} "
        f"et={et:.9f} /\n"
        for et, jt, parity in zip(
            values_et[1:], values_jt[1:], bandt_vals[1:]
        )  # Skip the first value (0.0)
    )

    # Convert the lines back into a string and replace the &partition / marker
    modified_template = "\n".join(lines)
    modified_template = modified_template.replace(
        "&partition /", dynamic_section + "&partition /"
    )

    return modified_template


def generate_inelastic_template(
    output_path: Union[str, PathLike],
    target_mass_amu: float,
    target_atomic_number: float,
    projectile_mass_amu: float,
    projectile_atomic_number: float,
    projectile_spin: Union[Fraction, str, int, float],
    E_lab_MeV: float,
    J_tot_min: Union[Fraction, str, int, float],
    J_tot_max: Union[Fraction, str, int, float],
    reaction_name: str,
    target_state_spins: List[Union[Fraction, str, int, float]],
    target_state_parities: List[bool],
    target_state_energies_MeV: List[float],
    multipoles: np.ndarray,
    R_match_fm: float,
    step_size_fm: float,
    overwrite: bool = False,
):
    """
    Generate an inelastic scattering input template for |frescox|.

    .. todo::
        * This has hardcoded formatting for writing values to file.  This
          package should not pretend to know what precision is needed by all
          applications.  Rather, it should write all values in full precision.
        * Seems like we should be doing explicit type checking of actual
          arguments.  Better yet if writing to full precision and type checking
          can be done by one single routine in the package's private interface
          that this just calls.
        * Ideally the text placeholders in the template would include units in
          the name so that when mapping arguments to placeholders below we have
          something like ``"RMATCH_FM": R_match_fm``.
        * Code checks if multipoles is None.  However, neither the documentation
          nor the type hints indicate that None is an acceptable argument.  The
          meaning of a None argument is not explained.

    Args:
        output_path:
            Path to save the generated template file
        target_mass_amu:
            Mass of the target nucleus
        target_atomic_number:
            Charge of the target nucleus
        projectile_mass_amu:
            Mass of the projectile nucleus
        projectile_atomic_number:
            Charge of the projectile nucleus
        projectile_spin:
            Spin of the projectile nucleus (integer or half-integer). Must be
            convertible to Fraction.
        E_lab_MeV:
            Laboratory energy of the projectile in MeV
        J_tot_min:
            Minimum total angular momentum (integer or half-integer).  Must be
            convertible to Fraction.
        J_tot_max:
            Maximum total angular momentum (integer or half-integer).  Must be
            convertible to Fraction.
        reaction_name:
            Name of the reaction for file naming
        target_state_spins:
            List of spin states of the target nucleus (integers or
            half-integers).  List elements must be convertible to Fraction.
        target_state_parities:
            List of parities for the target states (True for positive, False for
            negative)
        target_state_energies_MeV:
            List of excitation energies of the target states in MeV
        multipoles:
            numpy array of multipole transition orders (e.g., [2, 3] for
            quadrupole and octupole).
        R_match_fm:
            Matching radius in fm
        step_size_fm:
            Step size for the radial mesh in fm
        overwrite:
            Whether to overwrite the output file if it already exists
    """
    projectile_spin = _validate_spin(projectile_spin, "projectile_spin")
    J_tot_min = _validate_spin(J_tot_min, "J_tot_min")
    J_tot_max = _validate_spin(J_tot_max, "J_tot_max")

    if J_tot_min > J_tot_max:
        raise ValueError("J_tot_min cannot be greater than J_tot_max.")
    if J_tot_min < 0 or J_tot_max < 0:
        raise ValueError("J_tot_min and J_tot_max must be non-negative.")

    target_state_spins = [
        _validate_spin(s, "target_state_spins") for s in target_state_spins
    ]
    for spin in target_state_spins:
        if spin < 0:
            raise ValueError("All spin states must be non-negative.")

    if not isinstance(output_path, (str, PathLike)):
        raise TypeError("output_path must be a string or PathLike object.")
    output_path = Path(output_path).resolve()
    if output_path.is_dir():
        raise IsADirectoryError(
            f"Filename ({output_path}) corresponds to pre-existing directory"
        )
    elif output_path.exists() and not overwrite:
        raise FileExistsError(
            f"The file {output_path} already exists. "
            "Set overwrite=True to overwrite it."
        )

    num_states = len(target_state_energies_MeV)

    if len(target_state_spins) != num_states:
        raise ValueError(
            "Length of target_state_spins must match length"
            " of target_state_energies_MeV."
        )
    if len(target_state_parities) != num_states:
        raise ValueError(
            "Length of target_state_parities must match length "
            "of target_state_energies_MeV."
        )

    with open(TEMPLATE_FILE_PATH, "r") as file:
        template = file.read()

    modified_template = _setup_inelastic_system_template(
        template,
        np.asarray(target_state_energies_MeV),
        np.asarray(target_state_spins),
        np.asarray(target_state_parities),
    )

    # expand type=11 multipole stub(s)
    if multipoles is not None:
        modified_template = _expand_type11_pX(modified_template, multipoles)

    # Define placeholder replacements
    replacements = {
        "HEADER": reaction_name,
        "STEP_SIZE": f"{step_size_fm:.9f}",
        "RMATCH": f"{R_match_fm:.9f}",
        "J_TOT_MIN": f"{float(J_tot_min):.1f}",
        "J_TOT_MAX": f"{float(J_tot_max):.1f}",
        "E_LAB": f"{E_lab_MeV:.9f}",
        "CLOSED_COUPLINGS": f"{int(num_states):d}",
        "MASS_P": f"{projectile_mass_amu:.9f}",
        "CHARGE_P": f"{projectile_atomic_number:.9f}",
        "NUM_STATES": f"{int(num_states):d}",
        "MASS_T": f"{target_mass_amu:.9f}",
        "CHARGE_T": f"{target_atomic_number:.9f}",
        "S_PROJECTILE": f"{float(projectile_spin):.1f}",
        "I_GROUND": f"{float(target_state_spins[0]):.1f}",
        "GS_PAR": f"{int((-1) ** int(target_state_parities[0] + 1)):d}",
        "E_GROUND": f"{target_state_energies_MeV[0]:.9f}",
    }

    # Replace placeholders directly in the modified template
    for placeholder, value in replacements.items():
        modified_template = modified_template.replace(placeholder, value)

    # Write the final content to the output file
    with open(output_path, "w") as file:
        file.write(modified_template)
