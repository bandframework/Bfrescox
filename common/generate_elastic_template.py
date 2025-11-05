from fractions import Fraction
from os import PathLike
from pathlib import Path

from ._utils import _is_fraction_integer_or_half_integer

template_file_path = Path(__file__).parent / "templates/elastic.template"
with open(template_file_path, "r") as file:
    elastic_input_template = file.read()


def generate_elastic_template(
    output_path: str | PathLike[str],
    mass_t: float,
    charge_t: float,
    spin_t: Fraction,
    mass_p: float,
    charge_p: float,
    spin_p: Fraction,
    E_lab: float,
    J_tot_min: Fraction,
    J_tot_max: Fraction,
    R_Coulomb: float,
    reaction_name: str,
    E_0: float = 0.0,
    R_match: float = 60.0,
    step_size: float = 0.1,
):
    """
    Generate an elastic scattering input template for Fresco.

    Args:
        output_path (str | PathLike[str]): Path to save the generated
            template file.
        mass_t (float): Mass of the target nucleus.
        charge_t (float): Charge of the target nucleus.
        spin_t (Fraction): Spin of the target nucleus (integer or
            half-integer).
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
        E_0 (float): Ground state energy of the target nucleus in MeV
            (usually 0, larger for isomeric or excited final state).
            Default is 0.0.
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

    if not isinstance(output_path, (str, PathLike)):
        raise TypeError("output_path must be a string or PathLike object.")
    output_path = Path(output_path).resolve()

    # Define placeholder replacements
    replacements = {
        "HEADER": reaction_name,
        "STEP_SIZE": f"{step_size:.9f}",
        "RMATCH": f"{R_match:.9f}",
        "J_TOT_MIN": f"{float(J_tot_min):.1f}",
        "J_TOT_MAX": f"{float(J_tot_max):.1f}",
        "E_LAB": f"{E_lab:.9f}",
        "MASS_P": f"{mass_p:.9f}",
        "CHARGE_P": f"{charge_p:.9f}",
        "MASS_T": f"{mass_t:.9f}",
        "CHARGE_T": f"{charge_t:.9f}",
        "S_PROJECTILE": f"{float(spin_p):.1f}",
        "I_GROUND": f"{float(spin_t):.1f}",
        "E_GROUND": f"{E_0:.9f}",
        "COULOMB_R": f"{R_Coulomb:.9f}",
    }

    modified_template = elastic_input_template[:]

    # Replace placeholders directly in the modified template
    for placeholder, value in replacements.items():
        modified_template = modified_template.replace(placeholder, value)

    # Write the final content to the output file
    with open(output_path, "w") as file:
        file.write(modified_template)
