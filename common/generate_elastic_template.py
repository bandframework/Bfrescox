from fractions import Fraction
from os import PathLike
from pathlib import Path

from ._utils import _is_fraction_integer_or_half_integer, _validate_spin

TEMPLATE_FILE_PATH = Path(__file__).parent / "templates/elastic.template"


def generate_elastic_template(
    output_path: str | PathLike[str],
    reaction_name: str,
    target_mass_amu: float,
    target_atomic_number: int,
    target_spin: Fraction | str | int | float,
    projectile_mass_amu: float,
    projectile_atomic_number: int,
    projectile_spin: Fraction | str | int | float,
    E_lab_MeV: float,
    J_tot_min: Fraction | str | int | float,
    J_tot_max: Fraction | str | int | float,
    E_0_MeV: float,
    R_match_fm: float,
    step_size_fm: float,
):
    """
    Generate an elastic scattering input template for Fresco

    Args:
        output_path (str | PathLike[str]): Path to save the generated
            template file
        reaction_name (str): Name of the reaction for file naming
        target_mass_amu (float): Mass of the target nucleus
        target_atomic_number (int): Charge of the target nucleus
        target_spin (Fraction | str | int | float): Spin of the target
            nucleus (integer or half-integer)
        projectile_mass_amu (float): Mass of the projectile nucleus
        projectile_atomic_number (int): Charge of the projectile nucleus
        projectile_spin (Fraction | str | int | float): Spin of the
            projectile nucleus (integer or half-integer). Must be
            convertable to Fraction.
        E_lab_MeV (float): Laboratory energy of the projectile in MeV
        J_tot_min (Fraction | str | int | float): Minimum total angular
            momentum (integer or half-integer). Must be convertable to
            Fraction.
        J_tot_max (Fraction | str | int | float): Maximum total angular
            momentum (integer or half-integer). Must be convertable to
            Fraction.
        E_0_MeV (float): Ground state energy of the target nucleus in MeV
            (usually 0, larger for isomeric or excited final state)
        R_match_fm (float): Matching radius in fm.
        step_size_fm (float): Step size for the radial mesh in fm.

    Raises:
        ValueError: If J_tot_min is greater than J_tot_max, or if either
            J_tot_min or J_tot_max is negative, or if they are not
            integer or half-integer values
    """
    projectile_spin = _validate_spin(projectile_spin, "projectile_spin")
    target_spin = _validate_spin(target_spin, "target_spin")
    J_tot_min = _validate_spin(J_tot_min, "J_tot_min")
    J_tot_max = _validate_spin(J_tot_max, "J_tot_max")

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
        "STEP_SIZE": f"{step_size_fm:.9f}",
        "RMATCH": f"{R_match_fm:.9f}",
        "J_TOT_MIN": f"{float(J_tot_min):.1f}",
        "J_TOT_MAX": f"{float(J_tot_max):.1f}",
        "E_LAB": f"{E_lab_MeV:.9f}",
        "MASS_P": f"{projectile_mass_amu:.9f}",
        "CHARGE_P": f"{projectile_atomic_number:.9f}",
        "MASS_T": f"{target_mass_amu:.9f}",
        "CHARGE_T": f"{target_atomic_number:.9f}",
        "S_PROJECTILE": f"{float(projectile_spin):.1f}",
        "I_GROUND": f"{float(target_spin):.1f}",
        "E_GROUND": f"{E_0_MeV:.9f}",
    }

    with open(TEMPLATE_FILE_PATH, "r") as file:
        modified_template = file.read()

    # Replace placeholders directly in the modified template
    for placeholder, value in replacements.items():
        modified_template = modified_template.replace(placeholder, value)

    # Write the final content to the output file
    with open(output_path, "w") as file:
        file.write(modified_template)
