"""
Generate an inelastic scattering input template for Fresco.
"""

import re
from fractions import Fraction
from pathlib import Path
from typing import List

import numpy as np

from ._utils import _is_fraction_integer_or_half_integer

inelastic_input_template = r"""
HEADER
NAMELIST
&FRESCO hcm=STEP_SIZE rmatch=RMATCH
    jtmin=J_TOT_MIN jtmax=J_TOT_MAX absend= 0.01
	thmin=0.00 thmax=180.00 thinc=1.00
    iter=0 ips=0.0 iblock=CLOSED_COUPLINGS chans=1 smats=2  xstabl=1
	!wdisk=2 waves=3
    elab(1)=E_LAB treneg=1 /

 &PARTITION namep='projectile' massp=MASS_P zp=CHARGE_P
            namet='target'   masst=MASS_T zt=CHARGE_T qval=0.0 nex=NUM_STATES  /
 &STATES jp=S_PROJECTILE bandp=1 ep=0.0000 cpot=1 jt=I_GROUND bandt=GS_PAR et=E_GROUND /
 &STATES copyp=1 		 cpot=1 jt=I_EXCITED bandt=1 et=E_EXCITED /
 &partition /

 &POT kp=1 ap=MASS_P at=MASS_T rc=COULOMB_R  /
 &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
 &POT kp=1 type=11          pX=DELTA_LAMBDA_X /
 &POT kp=1 type=2  p1=@Vs@ p2=@rs@ p3=@as@ p4=@Ws@ p5=@rws@ p6=@aws@ /
 &POT kp=1 type=11          pX=DELTA_LAMBDA_X /
 &POT kp=1 type=3  p1=@Vso@ p2=@rso@ p3=@aso@ p4=@Wso@ p5=@rwso@ p6=@awso@ /

 &pot /
 &overlap /
 &coupling /
"""


def _expand_type11_pX(text: str, L_list) -> str:
    """
    For each line like:
      &POT kp=1 type=11          pX=DELTA_LAMBDA_X /
    replace with:
      &POT kp=1 type=11 p0=DELTA_LAMBDA_0 p2=DELTA_LAMBDA_2 ... /
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
    This ensures that the placeholder line for &STATES is removed and replaced.
    """
    # Split the template into lines for easier manipulation
    lines = template.splitlines()

    # Remove any placeholder lines containing the original &STATES placeholder
    placeholder_pattern = "&STATES copyp=1"
    lines = [line for line in lines if placeholder_pattern not in line]

    # Generate the dynamic &STATES section

    dynamic_section = "".join(
        f"&STATES copyp=1         cpot=1 jt={float(jt)} bandt={(-1) ** float(parity + 1)} et={et} /\n"
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
    output_path: Path,
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
    multipoles_t: np.ndarray,
    R_match: float = 60.0,
    step_size: float = 0.1,
):
    """
    Generate an inelastic scattering input template for Fresco.

    Parameters:
    output_path (Path): Path to save the generated template file.
    mass_t (float): Mass of the target nucleus.
    charge_t (float): Charge of the target nucleus.
    mass_p (float): Mass of the projectile nucleus.
    charge_p (float): Charge of the projectile nucleus.
    spin_p (Fraction): Spin of the projectile nucleus (integer or half-integer).
    E_lab (float): Laboratory energy of the projectile in MeV.
    J_tot_min (Fraction): Minimum total angular momentum (integer or half-integer).
    J_tot_max (Fraction): Maximum total angular momentum (integer or half-integer).
    R_Coulomb (float): Coulomb radius in fm.
    reaction_name (str): Name of the reaction for file naming.
    I_states (List[Fraction]): List of spin states of the target nucleus (integers
        or half-integers).
    Pi_states (List[bool]): List of parities for the target states (True for
        positive, False for negative).
    E_states (List[float]): List of excitation energies of the target states in MeV.
    multipoles_t (np.ndarray): Array of multipole transition orders (e.g., [2, 3]
        for quadrupole and octupole).
    R_match (float): Matching radius in fm. Default is 60.0.
    step_size (float): Step size for the radial mesh in fm. Default is 0

    Returns:

    """
    if J_tot_min > J_tot_max:
        raise ValueError("J_tot_min cannot be greater than J_tot_max.")
    if J_tot_min < 0 or J_tot_max < 0:
        raise ValueError("J_tot_min and J_tot_max must be non-negative.")
    if not _is_fraction_integer_or_half_integer(J_tot_min):
        raise ValueError("J_tot_min must be an integer or half-integer.")
    if not _is_fraction_integer_or_half_integer(J_tot_max):
        raise ValueError("J_tot_max must be an integer or half-integer.")
    for I in I_states:
        if I < 0:
            raise ValueError("All spin states must be non-negative.")
        if not _is_fraction_integer_or_half_integer(I):
            raise ValueError("All spin states must be integers or half-integers.")

    num_states = len(E_states)

    if len(I_states) != num_states:
        raise ValueError("Length of I_states must match length of E_states.")
    if len(Pi_states) != num_states:
        raise ValueError("Length of Pi_states must match length of E_states.")

    template = inelastic_input_template[:]
    modified_template = _setup_inelastic_system_template(
        template, E_states, I_states, Pi_states
    )

    # expand type=11 multipole stub(s)
    if multipoles_t is not None:
        modified_template = _expand_type11_pX(modified_template, multipoles_t)

    # Define placeholder replacements
    replacements = {
        "HEADER": reaction_name,
        "STEP_SIZE": str(step_size),
        "RMATCH": str(R_match),
        "J_TOT_MIN": str(float(J_tot_min)),
        "J_TOT_MAX": str(float(J_tot_max)),
        "E_LAB": str(E_lab),
        "CLOSED_COUPLINGS": str(int(num_states)),
        "MASS_P": str(mass_p),
        "CHARGE_P": str(charge_p),
        "NUM_STATES": str(num_states),
        "MASS_T": str(mass_t),
        "CHARGE_T": str(charge_t),
        "S_PROJECTILE": str(float(spin_p)),
        "I_GROUND": str(float(I_states[0])),
        "GS_PAR": str(Pi_states[0]),
        "E_GROUND": str(E_states[0]),
        "COULOMB_R": str(R_Coulomb),
    }

    # Replace placeholders directly in the modified template
    for placeholder, value in replacements.items():
        modified_template = modified_template.replace(placeholder, value)

    # Write the final content to the output file
    with open(output_path, "w") as file:
        file.write(modified_template)
