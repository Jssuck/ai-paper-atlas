"""Euclid X.24: a rectangle on lengths commensurable with a medial length."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Witness:
    rectangle_area_squared: F
    square_over_rectangle: F
    equivalent_side_fourth: F


def form_rectangle(q,h):
    """Take q=(x/u)^4 nonsquare and rational length ratio h=y/x > 0."""
    if any(type(x) not in (int,F) or x<=0 for x in (q,h)):
        raise ValueError("expected positive exact rational coordinates")
    q,h=F(q),F(h)
    p,d=q.numerator,q.denominator
    if isqrt(p)**2==p and isqrt(d)**2==d:
        raise ValueError("x must be medial: q cannot be a rational square")
    s=q*h*h
    return Witness(s,1/h,s)
