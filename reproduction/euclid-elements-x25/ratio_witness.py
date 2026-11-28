"""Euclid X.25: exact normalized squares of three widths."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def is_square(q):
    return isqrt(q.numerator)**2==q.numerator and isqrt(q.denominator)**2==q.denominator


@dataclass(frozen=True)
class Witness:
    width_squares: tuple[F,F,F]
    area_squared: F
    area_rational: bool


def construct(q,k,base_squared):
    """Use q=(x/u)^4, k=(y/x)^2 and base_squared=(base/u)^2."""
    if any(type(v) not in (int,F) or v<=0 for v in (q,k,base_squared)):
        raise ValueError("expected positive exact rational coordinates")
    q,k,b=map(F,(q,k,base_squared))
    if is_square(q) or is_square(k):
        raise ValueError("both q and k must be nonsquares")
    middle=k*q
    return Witness((q/b,middle/b,k*middle/b),middle,is_square(middle))
