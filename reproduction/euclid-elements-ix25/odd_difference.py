"""Exact parity certificate for Euclid IX.25."""
from dataclasses import dataclass


@dataclass(frozen=True)
class OddDifference:
    stripped: int
    even_intermediate: int
    difference: int
    half_without_unit: int
    unit_boundary: bool


def odd_difference(a,b):
    """Model even A > odd B >= 3, including a modern unit output."""
    if any(type(x) is not int for x in (a,b)) or not a>b>=3 or a%2 or b%2!=1:
        raise ValueError("expected even A > odd B >= 3")
    stripped=b-1
    intermediate=a-stripped
    diff=intermediate-1
    half=intermediate//2-1
    if diff!=a-b or half+half+1!=diff:
        raise ArithmeticError("odd-difference witness failed")
    return OddDifference(stripped,intermediate,diff,half,diff==1)
