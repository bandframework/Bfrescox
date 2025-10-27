"""
Generate an elastic scattering input template for Fresco.
"""

from fractions import Fraction
from pathlib import Path

from ._utils import _is_fraction_integer_or_half_integer

elastic_input_template = r"""HEADER
NAMELIST
&FRESCO hcm=STEP_SIZE rmatch=RMATCH
    jtmin=J_TOT_MIN jtmax=J_TOT_MAX absend= 0.01
  thmin=0.00 thmax=180.00 thinc=1.00
    iter=0 ips=0.0 iblock=0 chans=1 smats=2  xstabl=1
  wdisk=2
    elab(1)=E_LAB treneg=1 /

 &PARTITION namep='projectile' massp=MASS_P zp=CHARGE_P
            namet='target'   masst=MASS_T zt=CHARGE_T qval=-0.000 nex=1  /
 &STATES jp=S_PROJECTILE bandp=1 ep=0.0000 cpot=1 jt=I_GROUND bandt=1 et=E_GROUND /
 &partition /

 &POT kp=1 ap=MASS_P at=MASS_T rc=COULOMB_R  /
 &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
 &POT kp=1 type=2  p1=@Vs@ p2=@rs@ p3=@as@ p4=@Ws@ p5=@rws@ p6=@aws@ /
 &POT kp=1 type=3  p1=@Vso@ p2=@rso@ p3=@aso@ p4=@Wso@ p5=@rwso@ p6=@awso@ /

 &pot /
 &overlap /
 &coupling /
"""


def generate_elastic_template(
    output_path: Path,
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
    BE_t: float = 0.0,
    R_match: float = 60.0,
    step_size: float = 0.1,
):
    """
    Generate an elastic scattering input template for Fresco.

    Parameters:
    output_path (Path): Path to save the generated template file.
    mass_t (float): Mass of the target nucleus.
    charge_t (float): Charge of the target nucleus.
    spin_t (Fraction): Spin of the target nucleus (integer or half-integer).
    mass_p (float): Mass of the projectile nucleus.
    charge_p (float): Charge of the projectile nucleus.
    spin_p (Fraction): Spin of the projectile nucleus (integer or half-integer).
    E_lab (float): Laboratory energy of the projectile in MeV.
    J_tot_min (Fraction): Minimum total angular momentum (integer or half-integer).
    J_tot_max (Fraction): Maximum total angular momentum (integer or half-integer).
    R_Coulomb (float): Coulomb radius in fm.
    reaction_name (str): Name of the reaction for file naming.
    BE_t (float): Binding energy of the target in MeV. Default is 0.0.
    R_match (float): Matching radius in fm. Default is 60.0.
    step_size (float): Step size for the radial mesh in fm. Default is 0
    """

    if J_tot_min > J_tot_max:
        raise ValueError("J_tot_min cannot be greater than J_tot_max.")
    if J_tot_min < 0 or J_tot_max < 0:
        raise ValueError("J_tot_min and J_tot_max must be non-negative.")
    if not _is_fraction_integer_or_half_integer(J_tot_min):
        raise ValueError("J_tot_min must be an integer or half-integer.")
    if not _is_fraction_integer_or_half_integer(J_tot_max):
        raise ValueError("J_tot_max must be an integer or half-integer.")

    # Define placeholder replacements
    replacements = {
        "HEADER": reaction_name,
        "STEP_SIZE": str(step_size),
        "RMATCH": str(R_match),
        "J_TOT_MIN": str(float(J_tot_min)),
        "J_TOT_MAX": str(float(J_tot_max)),
        "E_LAB": str(E_lab),
        "MASS_P": str(mass_p),
        "CHARGE_P": str(charge_p),
        "MASS_T": str(mass_t),
        "CHARGE_T": str(charge_t),
        "S_PROJECTILE": str(float(spin_p)),
        "I_GROUND": str(float(spin_t)),
        "E_GROUND": str(BE_t),
        "COULOMB_R": str(R_Coulomb),
    }

    modified_template = elastic_input_template[:]

    # Replace placeholders directly in the modified template
    for placeholder, value in replacements.items():
        modified_template = modified_template.replace(placeholder, value)

    # Write the final content to the output file
    with open(output_path, "w") as file:
        file.write(modified_template)
