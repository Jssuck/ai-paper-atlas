"""Exact teaching certificate for Euclid VIII.21."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class SolidTrace:
    efg: tuple
    no: tuple
    left: tuple
    right: tuple


def factor_solids(a: int, c: int, d: int, b: int) -> SolidTrace:
    """Use the first three terms to recover a primitive plane bridge."""
    if any(type(x) is not int or x < 1 for x in (a,c,d,b)):
        raise ValueError("expected four positive integers")
    if a*d != c*c or c*b != d*d:
        raise ValueError("successive ratios must agree")
    s = gcd(a,c,d)
    e,f,g = a//s,c//s,d//s
    # VIII.20 applied locally to E,F,G, expressed in its least-ratio form.
    t = gcd(e,f)
    p,q = e//t,f//t
    if (e,f,g) != (p*p,p*q,q*q):
        raise ArithmeticError("the primitive plane bridge must be a square chain")
    n, rn = divmod(a,e)
    o, ro = divmod(c,e)
    if rn or ro or d != n*g or b != o*g:
        raise ArithmeticError("least bridge does not measure the supplied chain")
    return SolidTrace((e,f,g),(n,o),(p,p,n),(q,q,o))
