"""Euclid X.28, exact reference-relative reconstruction."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Witness:
    d_fourth: F
    e_fourth: F
    e_over_d_squared: F
    rectangle_area_squared: F


def _square(q):
    return (isqrt(q.numerator)**2, isqrt(q.denominator)**2)==(q.numerator,q.denominator)


def construct(a,b,c):
    """Accept normalized squares of three pairwise length-incommensurable sides."""
    if any(type(x) not in (int,F) or x<=0 for x in (a,b,c)):
        raise ValueError("expected positive exact rational coordinates")
    a,b,c=map(F,(a,b,c))
    for p,q,label in ((a,b,"A:B"),(a,c,"A:C"),(b,c,"B:C")):
        if _square(p/q):
            raise ValueError(f"{label} must be incommensurable in length")
    return Witness(a*b,a*c*c/b,c/b,a*c)
