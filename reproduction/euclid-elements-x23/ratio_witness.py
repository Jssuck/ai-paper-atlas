"""Euclid X.23 and its porism in reference-relative exact coordinates."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def square(q):
    return isqrt(q.numerator)**2 == q.numerator and isqrt(q.denominator)**2 == q.denominator


@dataclass(frozen=True)
class Witness:
    length_premise: bool
    b_side_fourth: F
    ed_squared: F
    df_squared: F
    ed_over_df: F


def transfer(q,k,base_squared):
    """Use q=(A/u)^4, k=B²/A² and base_squared=(CD/u)^2."""
    if any(type(x) not in (int,F) or x<=0 for x in (q,k,base_squared)):
        raise ValueError("expected positive exact rational inputs")
    q,k,base = map(F,(q,k,base_squared))
    if square(q):
        raise ValueError("A must be medial: q cannot be a rational square")
    other = k*k*q
    return Witness(square(k),other,q/base, other/base,1/k)
