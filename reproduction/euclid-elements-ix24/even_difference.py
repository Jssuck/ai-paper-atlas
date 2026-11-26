"""Construct the two equal halves in Euclid IX.24."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Difference:
    larger_half: int
    smaller_half: int
    remainder_half: int
    remainder: int


def even_difference(a,b):
    """Find the equal halves of A-B in the strict positive even domain."""
    if any(type(x) is not int for x in (a,b)) or not a>b>=2 or a%2 or b%2:
        raise ValueError("expected positive even integers A > B >= 2")
    left,right=a//2,b//2
    half=left-right
    remainder=a-b
    if half<=0 or half+half!=remainder:
        raise ArithmeticError("half-difference invariant failed")
    return Difference(left,right,half,remainder)
