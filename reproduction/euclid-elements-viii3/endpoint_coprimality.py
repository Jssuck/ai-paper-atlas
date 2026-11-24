"""Exact positive-integer teaching model of Euclid VIII.3."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Trace:
    ratio: Fraction
    least_chain: tuple[int,...]
    is_least: bool
    endpoint_measure: int


def inspect(terms, *, modern=False):
    terms = tuple(terms)
    if len(terms) < 2 or any(type(x) is not int or x < (1 if modern else 2) for x in terms):
        raise ValueError("need at least two positive integer terms (nonunits by default)")
    ratio = Fraction(terms[0], terms[1])
    if any(Fraction(a,b) != ratio for a,b in zip(terms,terms[1:])):
        raise ValueError("adjacent ratios differ")
    a,b = ratio.numerator,ratio.denominator
    if min(a,b) == 1 and not modern:
        raise ValueError("reduced unit or equal ratio requires the explicit modern model")
    n = len(terms)-1
    least = tuple(a**(n-i)*b**i for i in range(n+1))
    is_least = terms == least
    measure = gcd(terms[0],terms[-1])
    if is_least and measure != 1:
        raise ArithmeticError("least-chain endpoints should be coprime")
    return Trace(ratio,least,is_least,measure)


if __name__ == "__main__":
    print(inspect((8,12,18,27)))
