"""Exact directed nonmeasurement certificates for Euclid VIII.17."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    cube_chain: tuple[int,int,int,int]
    cube_remainder: int
    side_remainder: int
    cube_then_side_denominators: tuple[int,int]
    cube_then_side_antecedents: tuple[bool,bool]


def inspect(c,d,*,modern=False):
    if any(type(x) is not int or x < (1 if modern else 2) for x in (c,d)):
        raise ValueError("expected positive integral sides; nonunits by default")
    if c == d and not modern:
        raise ValueError("equal sides require modern=True")
    a,h,k,b = c**3,c*c*d,c*d*d,d**3
    q = c//gcd(c,d)
    cube,side = b%a,d%c
    if bool(cube)!=(q**3>1) or bool(side)!=(q>1):
        raise ArithmeticError("denominator certificate failed")
    # Branch 1 negates the conclusion of sides-measure => cubes-measure.
    # Branch 2 negates the conclusion of cubes-measure => sides-measure.
    return Trace((a,h,k,b),cube,side,(q**3,q),(bool(cube),bool(side)))


if __name__ == "__main__":
    for pair in ((6,9),(4,12),(12,4),(6,10)):
        print(pair,inspect(*pair))
