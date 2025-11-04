from fractions import Fraction


def _is_fraction_integer_or_half_integer(f: Fraction | int | float) -> bool:
    """
    Args:
        f (Fraction | int | float): The fraction to check.

    Returns:
        bool: True if the fraction is an integer or half-integer, False
            otherwise.
    """
    if isinstance(f, Fraction):
        return f.denominator in [1, 2]
    if isinstance(f, int):
        return True
    return float(f * 2).is_integer()
