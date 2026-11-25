"""Exact model of Euclid VIII.26 with ordered corresponding sides."""
from dataclasses import dataclass
from math import gcd, isqrt


@dataclass(frozen=True)
class SquareRatio:
    chain: tuple
    primitive: tuple
    scale: int
    roots: tuple


def square_ratio(left, right):
    a,b = left
    c,d = right
    if any(type(n) is not int or n < 1 for n in (a,b,c,d)):
        raise ValueError("all side factors must be positive integers")
    middle = b*c
    if middle != a*d:
        raise ValueError("corresponding sides are not proportional")
    chain = (a*b,middle,c*d)
    scale = gcd(*chain)
    primitive = tuple(n//scale for n in chain)
    p,q = isqrt(primitive[0]),isqrt(primitive[2])
    if primitive != (p*p,p*q,q*q):
        raise ArithmeticError("primitive chain does not certify a square ratio")
    return SquareRatio(chain,primitive,scale,(p,q))
