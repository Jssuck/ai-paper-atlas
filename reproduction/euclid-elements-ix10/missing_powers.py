"""Exact positional certificates in the positive-integer model of IX.10."""
from dataclasses import dataclass
from math import gcd, isqrt


@dataclass(frozen=True)
class Position:
    exponent: int
    value: int
    reduced_degree: int
    root: int


def floor_root(n, degree):
    if degree == 2:
        return isqrt(n)
    lo, hi = 0, 1 << ((n.bit_length() + degree - 1)//degree)
    while lo + 1 < hi:
        mid = (lo + hi)//2
        if mid**degree <= n:
            lo = mid
        else:
            hi = mid
    return lo


def positional_certificate(base, count, degree):
    """Return nonunit positions for a base that is not a square (or cube)."""
    if type(base) is not int or base < 2 or type(count) is not int or count < 1:
        raise ValueError("expected integer base >= 2 and count >= 1")
    if type(degree) is not int or degree not in (2, 3):
        raise ValueError("the historical branches have degree 2 or 3")
    if floor_root(base, degree)**degree == base:
        raise ValueError("base already has the selected power property")
    result = []
    term = 1
    for exponent in range(1, count + 1):
        term *= base
        reduced = degree//gcd(exponent, degree)
        root = floor_root(term, degree)
        if (root**degree == term) != (reduced == 1):
            raise ArithmeticError("exact root test disagrees with the positional certificate")
        result.append(Position(exponent, term, reduced, root if reduced == 1 else 0))
    return tuple(result)
