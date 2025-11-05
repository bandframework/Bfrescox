import re
from fractions import Fraction
from os import PathLike
from pathlib import Path
from typing import List

import numpy as np

from ._utils import _is_fraction_integer_or_half_integer

template_file_path = Path(__file__).parent / "templates/inelastic.template"
with open(template_file_path, "r") as file:
    inelastic_input_template = file.read()


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
    output_path: str | PathLike[str],
    mass_t: float,
    charge_t: float,
    mass_p: float,
    charge_p: float,
    spin_p: Fraction,
    E_lab: float,
    J_tot_min: Fraction,
    J_tot_max: Fraction,
    R_Coulomb: float,
    reaction_name: str,
    I_states: List[Fraction],
    Pi_states: List[bool],
    E_states: List[float],
    multipoles: np.ndarray,
    R_match: float = 60.0,
    step_size: float = 0.1,
):
    """
    Generate an inelastic scattering input template for Fresco.

    Args:
        output_path (str | PathLike[str]): Path to save the generated
            template file.
        mass_t (float): Mass of the target nucleus.
        charge_t (float): Charge of the target nucleus.
        mass_p (float): Mass of the projectile nucleus.
        charge_p (float): Charge of the projectile nucleus.
        spin_p (Fraction): Spin of the projectile nucleus (integer or
            half-integer).
        E_lab (float): Laboratory energy of the projectile in MeV.
        J_tot_min (Fraction): Minimum total angular momentum (integer or
            half-integer).
        J_tot_max (Fraction): Maximum total angular momentum (integer or
            half-integer).
        R_Coulomb (float): Coulomb radius in fm.
        reaction_name (str): Name of the reaction for file naming.
        I_states (List[Fraction]): List of spin states of the target
            nucleus (integers or half-integers).
        Pi_states (List[bool]): List of parities for the target states (True
            for positive, False for negative).
        E_states (List[float]): List of excitation energies of the target
            states in MeV.
        multipoles (np.ndarray): Array of multipole transition orders (e.g.,
            [2, 3] for quadrupole and octupole).
        R_match (float): Matching radius in fm. Default is 60.0.
        step_size (float): Step size for the radial mesh in fm. Default
            is 0.1.

    Raises:
        ValueError: If J_tot_min is greater than J_tot_max, or if either
            J_tot_min or J_tot_max is negative, or if they are not
            integer or half-integer values.
    """
    if J_tot_min > J_tot_max:
        raise ValueError("J_tot_min cannot be greater than J_tot_max.")
    if J_tot_min < 0 or J_tot_max < 0:
        raise ValueError("J_tot_min and J_tot_max must be non-negative.")
    if not _is_fraction_integer_or_half_integer(J_tot_min):
        raise ValueError("J_tot_min must be an integer or half-integer.")
    if not _is_fraction_integer_or_half_integer(J_tot_max):
        raise ValueError("J_tot_max must be an integer or half-integer.")
    for I_state in I_states:
        if I_state < 0:
            raise ValueError("All spin states must be non-negative.")
        if not _is_fraction_integer_or_half_integer(I_state):
            raise ValueError(
                "All spin states must be integers or half-integers."
            )

    if not isinstance(output_path, (str, PathLike)):
        raise TypeError("output_path must be a string or PathLike object.")
    output_path = Path(output_path).resolve()

    num_states = len(E_states)

    if len(I_states) != num_states:
        raise ValueError("Length of I_states must match length of E_states.")
    if len(Pi_states) != num_states:
        raise ValueError("Length of Pi_states must match length of E_states.")

    template = inelastic_input_template[:]
    modified_template = _setup_inelastic_system_template(
        template,
        np.asarray(E_states),
        np.asarray(I_states),
        np.asarray(Pi_states),
    )

    # expand type=11 multipole stub(s)
    if multipoles is not None:
        modified_template = _expand_type11_pX(modified_template, multipoles)

    # Define placeholder replacements
    replacements = {
        "HEADER": reaction_name,
        "STEP_SIZE": f"{step_size:.9f}",
        "RMATCH": f"{R_match:.9f}",
        "J_TOT_MIN": f"{float(J_tot_min):.1f}",
        "J_TOT_MAX": f"{float(J_tot_max):.1f}",
        "E_LAB": f"{E_lab:.9f}",
        "CLOSED_COUPLINGS": f"{int(num_states):d}",
        "MASS_P": f"{mass_p:.9f}",
        "CHARGE_P": f"{charge_p:.9f}",
        "NUM_STATES": f"{int(num_states):d}",
        "MASS_T": f"{mass_t:.9f}",
        "CHARGE_T": f"{charge_t:.9f}",
        "S_PROJECTILE": f"{float(spin_p):.1f}",
        "I_GROUND": f"{float(I_states[0]):.1f}",
        "GS_PAR": f"{int((-1) ** int(Pi_states[0] + 1))}",
        "E_GROUND": f"{E_states[0]:.9f}",
        "COULOMB_R": f"{R_Coulomb:.9f}",
    }

    # Replace placeholders directly in the modified template
    for placeholder, value in replacements.items():
        modified_template = modified_template.replace(placeholder, value)

    # Write the final content to the output file
    with open(output_path, "w") as file:
        file.write(modified_template)
