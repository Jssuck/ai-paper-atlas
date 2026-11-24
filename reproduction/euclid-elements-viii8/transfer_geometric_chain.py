"""Exact teaching reconstruction of Euclid VIII.8."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Trace:
    primitive: tuple[int,...]
    old_count: int
    new_count: int
    relative_scale: Fraction
    chain: tuple[int,...]


def transfer(source, first, last, *, modern=False):
    source = tuple(source)
    if len(source)<3 or any(type(x) is not int or x < (1 if modern else 2)
                           for x in (*source,first,last)):
        raise ValueError("need at least three positive integer source terms and two endpoints")
    a,b = source[:2]
    if any(a*y != b*x for x,y in zip(source,source[1:])):
        raise ValueError("source is not a constant-ratio chain")
    if a == b and not modern:
        raise ValueError("constant chain requires modern=True")
    if first*source[-1] != last*source[0]:
        raise ValueError("ordered endpoint ratios differ")
    common = gcd(*source)
    row = tuple(x//common for x in source)
    if gcd(row[0],row[-1]) != 1:
        raise ArithmeticError("primitive endpoint certificate failed")
    scale,r = divmod(first,row[0])
    if r or last != scale*row[-1]:
        raise ArithmeticError("coprime endpoints failed to yield an integral scale")
    return Trace(row,common,scale,Fraction(scale,common),tuple(x*scale for x in row))


if __name__ == "__main__":
    print(transfer((16,24,36,54),24,81))
