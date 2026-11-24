"""Exact integer teaching certificates for Euclid VIII.15."""
from dataclasses import dataclass
from math import gcd
from typing import Optional


@dataclass(frozen=True)
class Trace:
    squares: tuple[int,int,int]
    cubes: tuple[int,int,int,int]
    growth: tuple[int,int]
    side_count: Optional[int]
    adjacent_counts: tuple[Optional[int],...]
    endpoint_count: Optional[int]


def inspect(c,d,*,modern=False):
    if any(type(x) is not int or x < (1 if modern else 2) for x in (c,d)):
        raise ValueError("positive integral sides required, nonunits by default")
    if c == d and not modern:
        raise ValueError("equal sides require modern=True")
    e,f,g = c*c,c*d,d*d
    a,h,k,b = (c*e,c*f,d*f,d*g)
    common = gcd(c,d)
    p,q = d//common,c//common
    cubes = (a,h,k,b)
    if any(q*y != p*x for x,y in zip(cubes,cubes[1:])):
        raise ArithmeticError("cube bridge ratios failed")
    if q == 1:
        if b != p**3*a:
            raise ArithmeticError("endpoint multiplication failed")
        return Trace((e,f,g),cubes,(p,q),p,(p,p,p),p**3)
    return Trace((e,f,g),cubes,(p,q),None,(None,)*3,None)


def from_cubes(c,d,*,modern=False):
    """Transfer endpoint measurability to the first step, then to the sides."""
    a,h,k,b = inspect(c,d,modern=modern).cubes
    if b%a:
        return None
    count,remainder = divmod(h,a)
    if remainder or c*count != d:
        raise ArithmeticError("the first step did not yield the side count")
    return count


if __name__ == "__main__":
    for c,d in ((4,12),(4,6),(2,6)):
        print(c,d,inspect(c,d),from_cubes(c,d))
