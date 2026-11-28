"""Exact squared length coordinates for Euclid X.30."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Witness:
    l_squared: F
    g_squared: F
    l_over_h_squared: F
    g_over_h_squared: F


def construct(h,m,n):
    """Use h=(H/u)^2>0 and positive integer m,n with nonsquare sum of squares."""
    if type(h) not in (int,F) or h<=0:
        raise ValueError("expected positive exact rational h")
    if any(type(i) is not int or i<=0 for i in (m,n)):
        raise ValueError("expected two positive integer legs")
    total=m*m+n*n
    if isqrt(total)**2==total:
        raise ValueError("sum of squared legs must not be an integer square")
    h=F(h)
    l,g=F(m*m,total),F(n*n,total)
    return Witness(h*l,h*g,l,g)
