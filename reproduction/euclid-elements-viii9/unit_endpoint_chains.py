"""Finite exact teaching model for Euclid VIII.9."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Optional


@dataclass(frozen=True)
class Trace:
    growth: Fraction
    scale: int
    unit_chains: Optional[tuple[tuple[int,...],tuple[int,...]]]


def inspect(xs, *, modern=False):
    xs = tuple(xs)
    if len(xs)<3 or any(type(x) is not int or x < (1 if modern else 2) for x in xs):
        raise ValueError("need positive integer terms and at least one mean")
    r = Fraction(xs[1],xs[0])
    if any(y*r.denominator != x*r.numerator for x,y in zip(xs,xs[1:])):
        raise ValueError("adjacent ratios differ")
    if not modern and r == 1:
        raise ValueError("constant chain needs modern=True")
    p,q,n = r.numerator,r.denominator,len(xs)-1
    h,rem = divmod(xs[0],q**n)
    if rem or any(x != h*q**(n-i)*p**i for i,x in enumerate(xs)):
        raise ArithmeticError("primitive-scale invariant failed")
    if gcd(xs[0],xs[-1]) != h:
        raise ArithmeticError("endpoint measure did not match scale")
    witness = None if h!=1 else (tuple(q**i for i in range(n+1)),tuple(p**i for i in range(n+1)))
    return Trace(r,h,witness)
