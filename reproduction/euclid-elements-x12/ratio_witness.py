"""X.12: construct common measures from two successive rational ratios."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Witness:
    product_counts: tuple[int, int, int]
    product_measure: Fraction
    primitive_counts: tuple[int, int, int]
    primitive_measure: Fraction


def combine(a_over_c, c_over_b, c):
    """Find common scales for A,C,B from A/C, C/B and C in an exact unit."""
    for x in (a_over_c, c_over_b, c):
        if type(x) not in (int, Fraction) or x <= 0:
            raise ValueError("expected positive ints or Fractions")
    first, second, c = map(Fraction, (a_over_c, c_over_b, c))
    d, e = first.numerator, first.denominator
    f, g = second.numerator, second.denominator
    h, k, ell = d*f, e*f, e*g
    divisor = gcd(h, k, ell)
    unit = c/k
    return Witness((h, k, ell), unit,
                   (h//divisor, k//divisor, ell//divisor), unit*divisor)
