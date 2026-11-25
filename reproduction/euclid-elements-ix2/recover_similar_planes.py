"""Exact certificate for Euclid IX.2."""
from dataclasses import dataclass
from math import gcd, isqrt


@dataclass(frozen=True)
class PlaneTrace:
    product: int
    lifted_chain: tuple
    middle: int
    scale: int
    roots: tuple
    factors: tuple


def recover_similar_planes(a: int, b: int) -> PlaneTrace:
    """In the positive integer model, build similar factor pairs if AB is a square."""
    if any(type(x) is not int or x < 1 for x in (a,b)):
        raise ValueError("expected positive integer endpoints")
    c = a*b
    root = isqrt(c)
    if root**2 != c:
        raise ValueError("endpoint product must be a square")
    d,t = a*a,a*root
    m,rem = divmod(t,a)
    k = gcd(a,b)
    p,q = isqrt(a//k),isqrt(b//k)
    if rem or t*t != d*c or k*p*p != a or k*q*q != b or k*p*q != m:
        raise ArithmeticError("proportional witness invariant failed")
    return PlaneTrace(c,(d,t,c),m,k,(p,q),((p,k*p),(q,k*q)))
