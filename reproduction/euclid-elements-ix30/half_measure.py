"""Repeated-subtraction teaching certificate for Euclid IX.30."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    quotient: int
    half_dividend: int
    half_quotient: int


def half_measure(a,b):
    """Given an odd A measuring even B, show A also measures B/2."""
    if any(type(n) is not int for n in (a,b)) or a<3 or b<2 or a%2!=1 or b%2:
        raise ValueError("expected odd divisor >= 3 and even dividend >= 2")
    left,q=b,0
    while left>=a:
        left-=a
        q+=1
    if left:
        raise ValueError("the divisor must measure the dividend exactly")
    half,r=divmod(q,2)
    if r or a*half+a*half!=b:
        raise ArithmeticError("an odd quotient would give an odd product")
    return Witness(q,a*half,half)
