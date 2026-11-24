"""Exact positive-integer divisibility checks for Euclid VIII.6."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Trace:
    growth: Fraction
    antecedent: bool
    forward: tuple[tuple[int,int,bool],...]


def inspect(xs, *, modern=False):
    xs = tuple(xs)
    if len(xs) < 3 or any(type(x) is not int or x < (1 if modern else 2) for x in xs):
        raise ValueError("need at least three positive integer terms (nonunits by default)")
    g = gcd(xs[0],xs[1])
    u,v = xs[0]//g,xs[1]//g
    if any(u*b != v*a for a,b in zip(xs,xs[1:])):
        raise ValueError("adjacent ratios differ")
    if u == v and not modern:
        raise ValueError("equality needs modern=True")
    # Each gap k has reduced later/earlier ratio v**k/u**k.
    # Its denominator is one exactly when u is one.
    forward = tuple((i,j, u == 1) for i in range(len(xs)) for j in range(i+1,len(xs)))
    return Trace(Fraction(v,u),u>1,forward)


if __name__ == "__main__":
    for xs in ((24,12,6,3),(8,12,18,27),(5,15,45,135)):
        print(xs,inspect(xs))
