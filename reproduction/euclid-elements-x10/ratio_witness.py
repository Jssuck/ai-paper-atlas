"""X.10 symbolic construction; every stored quantity is exact."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


@dataclass(frozen=True)
class Construction:
    squared_ratio: Fraction
    d_squared: Fraction
    e_fourth: Fraction


def construct(a, b, c):
    """Given A=a and B:C=b:c, return the radicands for positive D and E.

    The hypothesis excludes a rational-square ratio C/B.
    """
    if type(a) not in (int, Fraction) or a <= 0:
        raise ValueError("A must be a positive int or Fraction")
    if any(type(j) is not int or j <= 0 for j in (b, c)):
        raise ValueError("B and C must be positive integers")
    q = Fraction(c, b)
    p, d = q.numerator, q.denominator
    if isqrt(p)**2 == p and isqrt(d)**2 == d:
        raise ValueError("C/B is a rational square; X.10 hypothesis fails")
    a = Fraction(a)
    d_squared = a**2 * q
    e_fourth = a**2 * d_squared
    return Construction(q, d_squared, e_fourth)
