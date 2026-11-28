"""X.27: construct two medial sides from rational normalized squares."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Witness:
    c_fourth: F
    d_fourth: F
    d_over_c_squared: F
    rectangle_area: F


def construct(a,b):
    """a=(A/u)^2 and b=(B/u)^2; B²/A² must be a nonsquare."""
    if any(type(v) not in (int,F) or v<=0 for v in (a,b)):
        raise ValueError("expected positive exact rational squares of lengths")
    a,b=F(a),F(b)
    k=b/a
    if isqrt(k.numerator)**2==k.numerator and isqrt(k.denominator)**2==k.denominator:
        raise ValueError("input ratio of squared lengths must not be a rational square")
    return Witness(a*b,b**3/a,k,b)
