"""Book X.9: positive lengths specified by squared measures in one scale."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


@dataclass(frozen=True)
class Certificate:
    area_ratio: Fraction
    length_ratio: Fraction | None
    common_side_squared: Fraction | None


def classify(area_a, area_b):
    """Certify rational area ratio and recover a length measure when possible.

    Both squared lengths must be exact positive rationals in the same area unit.
    If length_ratio=m/n in lowest terms, the common side has square area_a/m².
    The side itself may be irrational in the externally chosen length unit.
    """
    for area in (area_a, area_b):
        if type(area) not in (int, Fraction) or area <= 0:
            raise ValueError("both squared lengths must be positive ints or Fractions")
    a, b = Fraction(area_a), Fraction(area_b)
    q = a / b
    p, d = q.numerator, q.denominator
    m, n = isqrt(p), isqrt(d)
    if m*m != p or n*n != d:
        return Certificate(q, None, None)
    return Certificate(q, Fraction(m, n), a/(m*m))
