"""Exact arithmetic reconstruction for Euclid VIII.20."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Factorization:
    d: int
    e: int
    f: int
    g: int


def factor_planes(a: int, c: int, b: int) -> Factorization:
    """Given a geometric triple (first, middle, last), recover D,E,F,G."""
    if any(type(x) is not int or x < 1 for x in (a, c, b)):
        raise ValueError("all three terms must be positive integers")
    if a*b != c*c:
        raise ValueError("the middle term must be a mean proportional")
    t = gcd(a, c)
    d, e = a//t, c//t
    f, rem_f = divmod(a,d)
    g, rem_g = divmod(c,d)
    if rem_f or rem_g or c != e*f or b != e*g:
        raise ArithmeticError("least-ratio measuring invariant failed")
    return Factorization(d,e,f,g)
