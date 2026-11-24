"""Exact integer teaching reconstruction of Euclid VIII.2."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    bases: tuple[int,int]
    terms: tuple[int,...]


def construct(a,b,n,*,modern=False):
    lower = 1 if modern else 2
    if (any(type(x) is not int or x < lower for x in (a,b))
            or type(n) is not int or n < 2):
        raise ValueError("need valid positive bases and length at least two")
    g = gcd(a,b)
    x,y = a//g,b//g
    if not modern and min(x,y) < 2:
        raise ValueError("reduced unit or equal ratio needs modern=True")
    out = (x,y)
    for _ in range(2,n):
        out = tuple(x*t for t in out) + (y*out[-1],)
    if any(b*u != a*v for u,v in zip(out,out[1:])):
        raise ArithmeticError("adjacent ratios differ")
    if gcd(out[0],out[-1]) != 1:
        raise ArithmeticError("endpoints are not coprime")
    return Trace((x,y),out)


if __name__ == "__main__":
    print(construct(2,3,3))
    print(construct(2,3,4))
