"""Exact finite teaching reconstruction of Euclid VIII.1."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Trace:
    adjacent: Fraction
    endpoint_measure: int
    least_by_vii33: tuple[int, ...]
    enters_viii1: bool


def inspect(terms):
    terms = tuple(terms)
    if len(terms) < 2 or any(type(x) is not int or x < 2 for x in terms):
        raise ValueError("at least two nonunit positive integers required")
    ratio = Fraction(terms[1],terms[0])
    if any(Fraction(b,a) != ratio for a,b in zip(terms,terms[1:])):
        raise ValueError("adjacent ratios must all be equal")
    g = 0
    for x in terms:
        g = gcd(g,x)
    endpoint = gcd(terms[0],terms[-1])
    least = tuple(x//g for x in terms)
    if endpoint == 1 and least != terms:
        raise ArithmeticError("a common scale would divide both endpoints")
    return Trace(ratio,endpoint,least,endpoint == 1)


if __name__ == "__main__":
    for xs in ((8,12,18,27),(16,24,36,54)):
        print(xs,inspect(xs))
