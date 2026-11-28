"""X.18: exact rationality propagation for a positive whole and its parts."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


@dataclass(frozen=True)
class Witness:
    gap_squared: Fraction
    ratios: tuple[Fraction, Fraction, Fraction, Fraction] | None


def analyze(whole, side):
    """Return d² and rational ratios (x/y, L/y, L/(2y), L/d), if present.

    L=whole=x+y, side²=4xy, x>y>0, and d=x−y>0.
    """
    if any(type(v) not in (int,Fraction) or v <= 0 for v in (whole,side)):
        raise ValueError("expected positive rational coordinates")
    length, side = Fraction(whole), Fraction(side)
    if length <= side:
        raise ValueError("whole must strictly exceed side")
    d2 = length**2 - side**2
    m,n = isqrt(d2.numerator),isqrt(d2.denominator)
    if (m*m,n*n) != (d2.numerator,d2.denominator):
        return Witness(d2,None)
    d = Fraction(m,n)
    x,y = (length+d)/2,(length-d)/2
    return Witness(d2,(x/y,length/y,length/(2*y),length/d))
