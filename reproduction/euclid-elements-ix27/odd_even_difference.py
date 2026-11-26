"""Exact parity certificate for Euclid IX.27."""
from dataclasses import dataclass


@dataclass(frozen=True)
class OddDifference:
    stripped: int
    even_intermediate: int
    difference: int
    half_without_unit: int
    unit_boundary: bool


def odd_even_difference(a,b):
    """Model odd A > even B >= 2, including a modern unit output."""
    if any(type(x) is not int for x in (a,b)) or not a>b>=2 or a%2!=1 or b%2:
        raise ValueError("expected odd A > even B >= 2")
    stripped=a-1
    intermediate=stripped-b
    diff=intermediate+1
    half=intermediate//2
    if diff!=a-b or half+half+1!=diff:
        raise ArithmeticError("odd-difference witness failed")
    return OddDifference(stripped,intermediate,diff,half,diff==1)
