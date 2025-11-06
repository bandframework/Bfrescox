from fractions import Fraction
from typing import Union


def _is_fraction_integer_or_half_integer(f: Fraction) -> bool:
    """
    Args:
        f (Fraction): The fraction to check

    Returns:
        bool: True if the fraction is an integer or half-integer, False
            otherwise.
    """
    return f.denominator in [1, 2]


def _validate_spin(
    spin: Union[Fraction, str, int, float], var_name: str
) -> Fraction:
    """
    Args:
        spin (Union[Fraction, str, int, float]): The spin value to validate,
            must be convertible to a Fraction.

    Raises:
        ValueError: If the spin is not an integer or half-integer.

    Returns:
        Fraction: The validated spin value as a Fraction.
    """
    if not isinstance(spin, (Fraction, str, int, float)):
        raise TypeError(f"{var_name} must be a Fraction, str, int, or float.")
    spin_fraction = Fraction(spin)
    if not _is_fraction_integer_or_half_integer(spin_fraction):
        raise ValueError(f"{var_name} must be an integer or half-integer.")
    return spin_fraction
