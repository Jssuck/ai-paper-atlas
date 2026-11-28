"""Euclid X.22: apply the square on a medial length along a rational base."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Witness:
    width_squared: F
    width_to_base_squared: F


def apply_medial(q,b):
    """Accept q=(medial/u)^4 and b=(base/u)^2; return squared ratios."""
    if any(type(x) not in (int,F) or x <= 0 for x in (q,b)):
        raise ValueError("expected positive exact rational coordinates")
    q,b=F(q),F(b)
    p,r=q.numerator,q.denominator
    if isqrt(p)**2==p and isqrt(r)**2==r:
        raise ValueError("q must not be a rational square")
    return Witness(q/b,q/(b*b))
