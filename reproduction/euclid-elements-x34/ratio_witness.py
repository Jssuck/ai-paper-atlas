"""Euclid X.34: two squared sides as an exact sum and difference of roots."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def square(q):
    return (isqrt(q.numerator)**2,isqrt(q.denominator)**2)==(q.numerator,q.denominator)


@dataclass(frozen=True)
class Witness:
    center_squared: F
    offset_squared: F
    sum_squared: F
    rectangle_area: F
    cross_term_squared: F
    cross_term_rational: bool
    offset_rational: bool


def construct(r,k):
    """Inputs r=HL/u², k=(L/H)²; squared sides are √center² ± √offset²."""
    if any(type(x) not in (int,F) for x in (r,k)):
        raise ValueError("expected exact rational inputs")
    r,k=F(r),F(k)
    if not (r>0 and 0<k<1):
        raise ValueError("expected r>0 and 0<k<1")
    if square(k) or square(1-k):
        raise ValueError("k and 1−k must both be nonsquares")
    center=r*r/(4*k)
    offset=center*(1-k)
    cross=4*center*offset
    return Witness(center,offset,4*center,r/2,cross,square(cross),square(offset))
