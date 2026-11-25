"""Exact integer teaching model of Euclid IX.8."""
from dataclasses import dataclass
from math import isqrt
from typing import Optional


@dataclass(frozen=True)
class Term:
    position: int
    exponent: int
    value: int
    guaranteed_square_root: Optional[int]
    guaranteed_cube_root: Optional[int]
    actual_square: bool
    actual_cube: bool


def _is_cube(n):
    lo,hi=0,1 << ((n.bit_length()+2)//3)
    while lo+1<hi:
        mid=(lo+hi)//2
        if mid**3<=n:
            lo=mid
        else:
            hi=mid
    return lo**3==n


def power_positions(q, length):
    """Return length terms including the separately identified unit position."""
    if type(q) is not int or q<2 or type(length) is not int or length<1:
        raise ValueError("expected integer base >= 2 and length >= 1")
    value=1
    terms=[]
    for exponent in range(length):
        square=q**(exponent//2) if exponent>0 and exponent%2==0 else None
        cube=q**(exponent//3) if exponent>0 and exponent%3==0 else None
        if (square is not None and square**2!=value) or (cube is not None and cube**3!=value):
            raise ArithmeticError("positional root certificate failed")
        terms.append(Term(exponent+1,exponent,value,square,cube,
                          isqrt(value)**2==value,_is_cube(value)))
        value*=q
    return tuple(terms)
