"""Exact normalized coordinates for Euclid X.29."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Witness:
    l_squared: F
    g_squared: F
    g_over_h: F


def construct(h,n,m):
    """Use h=(H/u)^2 and strictly positive integers n>m."""
    if type(h) not in (int,F) or h<=0:
        raise ValueError("h must be positive and exact rational")
    if type(n) is not int or type(m) is not int or not n>m>0:
        raise ValueError("expected strictly ordered positive integers n>m")
    gap=n*n-m*m
    if isqrt(gap)**2==gap:
        raise ValueError("n²−m² must not be an integer square")
    h=F(h)
    return Witness(h*F(gap,n*n), h*F(m*m,n*n), F(m,n))
