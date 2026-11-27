"""X.13: positive lengths modeled by rational squared coordinates."""
from fractions import Fraction
from math import isqrt


def _positive(x):
    if type(x) not in (int, Fraction) or x <= 0:
        raise ValueError("expected a positive int or Fraction")
    return Fraction(x)


def ratio(a_squared, b_squared):
    """Return the positive rational A/B, or None if lengths are incommensurable."""
    q = _positive(a_squared) / _positive(b_squared)
    m, n = isqrt(q.numerator), isqrt(q.denominator)
    return Fraction(m,n) if m*m == q.numerator and n*n == q.denominator else None


def transfer(a_squared, b_squared, c_squared):
    """Verify A commensurable with B and A incommensurable with C; return B/C."""
    if ratio(a_squared,b_squared) is None:
        raise ValueError("A and B must be commensurable")
    if ratio(a_squared,c_squared) is not None:
        raise ValueError("A and C must be incommensurable")
    return ratio(b_squared,c_squared)
