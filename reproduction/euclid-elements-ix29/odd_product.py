"""Odd-product teaching certificate for Euclid IX.29."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    copies: int
    residual_half: int
    unit_pairs: int
    total_half: int
    total: int


def odd_times_odd(a,b):
    """Take odd B exactly odd A times; both inputs are nonunit."""
    if any(type(n) is not int or n<3 or n%2!=1 for n in (a,b)):
        raise ValueError("expected two odd integers >= 3")
    residual_per_copy=(b-1)//2
    residual_half=units=total=0
    for _ in range(a):
        residual_half+=residual_per_copy
        units+=1
        total+=b
    pairs,remaining=divmod(units,2)
    half=residual_half+pairs
    if remaining!=1 or half+half+remaining!=total:
        raise ArithmeticError("odd product certificate failed")
    return Witness(a,residual_half,pairs,half,total)
