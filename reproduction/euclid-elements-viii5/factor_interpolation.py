"""Exact arithmetic teaching trace for Euclid VIII.5."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    raw: tuple[int,int,int]
    primitive: tuple[int,int,int]
    common_measure: int
    endpoint_order: int


def interpolate(a,b,c,d,*,modern=False):
    if any(type(x) is not int or x < (1 if modern else 2) for x in (a,b,c,d)):
        raise ValueError("need positive integral factors, nonunits by default")
    x,y,z = a*b,c*b,c*d
    g = gcd(gcd(x,y),z)
    if c*x != a*y or d*y != b*z:
        raise ArithmeticError("factor replacement ratios failed")
    return Trace((x,y,z),(x//g,y//g,z//g),g,(x>z)-(x<z))


if __name__ == "__main__":
    print(interpolate(6,10,9,14))
