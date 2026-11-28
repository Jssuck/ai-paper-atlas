"""Euclid X.31: preserve the gap's commensurability in exact coordinates."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def square(q):
    return isqrt(q.numerator)**2==q.numerator and isqrt(q.denominator)**2==q.denominator


@dataclass(frozen=True)
class Witness:
    c_fourth: F
    d_fourth: F
    rectangle_area: F
    d_over_c_squared: F
    gap_ratio_squared: F
    gap_commensurable: bool


def construct(a,b):
    """Inputs a=(A/u)^2 > b=(B/u)^2 > 0, with b/a nonsquare."""
    if any(type(x) not in (int,F) or x<=0 for x in (a,b)):
        raise ValueError("expected positive exact rational squared lengths")
    a,b=F(a),F(b)
    if a<=b:
        raise ValueError("A must strictly exceed B")
    k=b/a
    if square(k):
        raise ValueError("B/A must be irrational")
    return Witness(a*b,b**3/a,b,k,1-k,square(1-k))
