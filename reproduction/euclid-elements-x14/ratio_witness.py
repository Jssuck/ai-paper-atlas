"""Exact rational-side model for the two-way classification in X.14."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


@dataclass(frozen=True)
class Witness:
    remainder_square_ratio: Fraction
    remainder_to_larger_ratio: Fraction | None


def classify(a,b,c,d):
    """Given A>B and C>D in the same ordered ratio, classify both remainders."""
    for x in a,b,c,d:
        if type(x) not in (int,Fraction) or x <= 0:
            raise ValueError("positive rational sides required")
    a,b,c,d = map(Fraction,(a,b,c,d))
    if not (a>b and c>d):
        raise ValueError("each pair must be strictly decreasing")
    if a*d != b*c:
        raise ValueError("ordered ratios must agree")
    q = (a*a-b*b)/(a*a)
    m,n = isqrt(q.numerator),isqrt(q.denominator)
    return Witness(q, Fraction(m,n) if (m*m,n*n)==(q.numerator,q.denominator) else None)
