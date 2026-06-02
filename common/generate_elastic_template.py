from fractions import Fraction
from os import PathLike
from pathlib import Path
from typing import Union

from ._utils import _validate_spin

TEMPLATE_FILE_PATH = Path(__file__).parent / "templates/elastic.template"


def generate_elastic_template(
    output_path: Union[str, PathLike],
    reaction_name: str,
    target_mass_amu: float,
    target_atomic_number: int,
    target_spin: Union[Fraction, str, int, float],
    projectile_mass_amu: float,
    projectile_atomic_number: int,
    projectile_spin: Union[Fraction, str, int, float],
    E_lab_MeV: float,
    J_tot_min: Union[Fraction, str, int, float],
    J_tot_max: Union[Fraction, str, int, float],
    E_0_MeV: float,
    R_match_fm: float,
    step_size_fm: float,
    overwrite: bool = False,
):
    """
    Generate an elastic scattering input template for |frescox|.

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

    Args:
        output_path:
            Path to save the generated template file
        reaction_name:
            Name of the reaction for file naming
        target_mass_amu:
            Mass of the target nucleus
        target_atomic_number:
            Charge of the target nucleus
        target_spin:
            Spin of the target nucleus (integer or half-integer)
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
        E_0_MeV:
            Ground state energy of the target nucleus in MeV (usually 0, larger
            for isomeric or excited final state)
        R_match_fm:
            Matching radius in fm
        step_size_fm:
            Step size for the radial mesh in fm
        overwrite:
            Whether to overwrite the output file if it already exists
    """
    projectile_spin = _validate_spin(projectile_spin, "projectile_spin")
    target_spin = _validate_spin(target_spin, "target_spin")
    J_tot_min = _validate_spin(J_tot_min, "J_tot_min")
    J_tot_max = _validate_spin(J_tot_max, "J_tot_max")

    if J_tot_min > J_tot_max:
        raise ValueError("J_tot_min cannot be greater than J_tot_max.")
    if J_tot_min < 0 or J_tot_max < 0:
        raise ValueError("J_tot_min and J_tot_max must be non-negative.")

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
