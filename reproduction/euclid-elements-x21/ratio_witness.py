"""Euclid X.21 teaching model: normalize area to a reference square."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def _square(q):
    return isqrt(q.numerator)**2 == q.numerator and isqrt(q.denominator)**2 == q.denominator


def _radical(q):
    # sqrt(p/r) = sqrt(p*r)/r. Remove squares by trial division.
    d, c, k = q.numerator*q.denominator, 1, 2
    while k*k <= d:
        while d % (k*k) == 0:
            d //= k*k
            c *= k
        k += 1
    return F(c,q.denominator), d


@dataclass(frozen=True)
class Witness:
    sides_commensurable: bool
    area_rational: bool
    area_radical: tuple[F,int]
    equal_square_side_fourth: F


def classify(a,b):
    """For sides u√a,u√b, return exact certificates relative to u."""
    if any(type(x) not in (int,F) or x <= 0 for x in (a,b)):
        raise ValueError("expected positive exact rational squared sides")
    a,b=F(a),F(b)
    q=a*b
    return Witness(_square(a/b),_square(q),_radical(q),q)
