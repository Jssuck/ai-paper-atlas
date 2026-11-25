"""Exact ordered-factor model of Euclid VIII.27."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class CubeRatio:
    chain: tuple
    primitive: tuple
    scale: int
    roots: tuple


def cube_ratio(left, right):
    a,b,c = left
    d,e,f = right
    if any(type(n) is not int or n < 1 for n in (a,b,c,d,e,f)):
        raise ValueError("each side factor must be a positive integer")
    if a*e != b*d or b*f != c*e:
        raise ValueError("corresponding sides are not proportional")
    chain = (a*b*c,d*b*c,d*b*f,d*e*f)
    scale = gcd(*chain)
    primitive = tuple(n//scale for n in chain)
    common = gcd(a,d)
    p,q = a//common,d//common
    if primitive != (p**3,p*p*q,p*q*q,q**3):
        raise ArithmeticError("primitive chain does not certify a cube ratio")
    return CubeRatio(chain,primitive,scale,(p,q))
