from fractions import Fraction


def _is_fraction_integer_or_half_integer(f):
    """
    Args:
      f: A fractions.Fraction object.

    Returns:
      True if the fraction represents an even integer or
        half-integer, False otherwise.
    """
    if isinstance(f, Fraction):
        return f.denominator in [1, 2]
    return (f * 2).is_integer()
