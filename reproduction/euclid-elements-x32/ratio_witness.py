"""Exact normalized squared lengths for Euclid X.32."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def square(q):
    return isqrt(q.numerator)**2==q.numerator and isqrt(q.denominator)**2==q.denominator


@dataclass(frozen=True)
class Witness:
    d_fourth: F
    e_fourth: F
    area_squared: F
    e_over_d_squared: F
    gap_ratio_squared: F
    gap_commensurable: bool


def construct(a,b,c):
    """Require a>c and all pairwise input length ratios irrational."""
    if any(type(x) not in (int,F) or x<=0 for x in (a,b,c)):
        raise ValueError("expected positive exact rational coordinates")
    a,b,c=map(F,(a,b,c))
    if a<=c:
        raise ValueError("A must strictly exceed C")
    for q,label in ((a/b,"A:B"),(a/c,"A:C"),(b/c,"B:C")):
        if square(q):
            raise ValueError(f"{label} must be length-incommensurable")
    k=c/a
    return Witness(a*b,b*c*c/a,b*c,k,1-k,square(1-k))
