"""Exact measurement certificates for Euclid VIII.14."""
from dataclasses import dataclass
from math import gcd
from typing import Optional


@dataclass(frozen=True)
class Trace:
    bridge: tuple[int,int,int]
    reduced_growth: tuple[int,int]
    side_count: Optional[int]
    bridge_count: Optional[int]
    square_count: Optional[int]


def inspect(c,d,*,modern=False):
    if any(type(x) is not int or x < (1 if modern else 2) for x in (c,d)):
        raise ValueError("positive integer sides required (nonunits by default)")
    if c == d and not modern:
        raise ValueError("equal sides require modern=True")
    a,e,b = c*c,c*d,d*d
    if e*e != a*b:
        raise ArithmeticError("square bridge is not geometric")
    g = gcd(c,d)
    p,q = d//g,c//g
    if q == 1:
        if p*a != e or p*e != b or p*p*a != b:
            raise ArithmeticError("forward multiplication certificate failed")
        return Trace((a,e,b),(p,q),p,p,p*p)
    return Trace((a,e,b),(p,q),None,None,None)


def from_squares(c,d,*,modern=False):
    """If A divides B, recover C's measurement count in D via A:E."""
    trace = inspect(c,d,modern=modern)
    a,e,b = trace.bridge
    _,r = divmod(b,a)
    if r:
        return None
    count,s = divmod(e,a)
    if s or count*c != d:
        raise ArithmeticError("VIII.7 transfer to the middle term failed")
    return count


if __name__ == "__main__":
    for sides in ((4,12),(12,4),(6,9),(4,10),(2,3)):
        print(sides,inspect(*sides))
