"""Exact directed nonmeasurement certificates for Euclid VIII.16."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    bridge: tuple[int,int,int]
    side_remainder: int
    square_remainder: int
    denominators: tuple[int,int]
    branches_triggered: tuple[bool,bool]


def inspect(c,d,*,modern=False):
    if any(type(x) is not int or x < (1 if modern else 2) for x in (c,d)):
        raise ValueError("expected positive integral sides; nonunits by default")
    if c == d and not modern:
        raise ValueError("equal sides require modern=True")
    a,e,b = c*c,c*d,d*d
    q = c//gcd(c,d)
    side, square = d%c,b%a
    if bool(side)!=(q>1) or bool(square)!=(q*q>1):
        raise ArithmeticError("reduced denominators do not match the remainders")
    # VIII.16 text order: square antecedent first, side antecedent second.
    return Trace((a,e,b),side,square,(q,q*q),(bool(square),bool(side)))


if __name__ == "__main__":
    for pair in ((6,9),(4,12),(12,4)):
        print(pair,inspect(*pair))
