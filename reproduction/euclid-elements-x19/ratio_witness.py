"""X.19: reference-relative classification of a rectangle."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Witness:
    length_ratio: F | None
    area_ratio: F | None
    area_counts: tuple[int,int] | None
    measure_in_reference_squares: F | None


def _root(v):
    m,n = isqrt(v.numerator),isqrt(v.denominator)
    return F(m,n) if m*m==v.numerator and n*n==v.denominator else None


def classify(a,b):
    """Sides are u√a,u√b. Return their ratio and area relative to u²."""
    if any(type(x) not in (int,F) or x<=0 for x in (a,b)):
        raise ValueError("expected positive exact rational squared coordinates")
    a,b = F(a),F(b)
    length, area = _root(a/b), _root(a*b)
    if area is None:
        return Witness(length,None,None,None)
    m,n = area.numerator,area.denominator
    return Witness(length,area,(m,n),F(1,n))
