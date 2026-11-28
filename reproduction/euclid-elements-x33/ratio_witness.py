"""X.33: exact conjugate squared coordinates for the constructed parts."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def square(k):
    return (isqrt(k.numerator)**2, isqrt(k.denominator)**2)==(k.numerator,k.denominator)


@dataclass(frozen=True)
class Witness:
    radicand: F
    center: F
    coefficient: F
    sum_squares: F
    rectangle_squared: F


def construct(h,l):
    """Return x²/u²,y²/u² as center ± coefficient*sqrt(radicand)."""
    if any(type(x) not in (int,F) or x<=0 for x in (h,l)):
        raise ValueError("expected positive exact rational square coordinates")
    h,l=F(h),F(l)
    if h<=l:
        raise ValueError("h must strictly exceed l")
    k=l/h
    if square(k) or square(1-k):
        raise ValueError("both k and 1−k must be nonsquares")
    return Witness(1-k,h/2,h/2,h,h*l/4)
