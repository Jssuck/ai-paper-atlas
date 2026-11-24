"""Exact finite teaching model of Euclid VIII.7."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Trace:
    growth: Fraction
    span: int
    endpoint_growth: Fraction
    measures_second: bool
    measures_last: bool


def inspect(xs, *, modern=False):
    xs = tuple(xs)
    if len(xs) < 3 or any(type(x) is not int or x < (1 if modern else 2) for x in xs):
        raise ValueError("need at least three positive integer terms (nonunits by default)")
    q = Fraction(xs[1],xs[0])
    if any(q.denominator*b != q.numerator*a for a,b in zip(xs,xs[1:])):
        raise ValueError("adjacent ratios differ")
    if q == 1 and not modern:
        raise ValueError("equality requires modern=True")
    span = len(xs)-1
    total = q**span
    if total.numerator*xs[0] != total.denominator*xs[-1]:
        raise ArithmeticError("endpoint ratio certificate failed")
    return Trace(q,span,total,q.denominator==1,total.denominator==1)


if __name__ == "__main__":
    for xs in ((5,15,45,135),(24,12,6,3),(8,12,18,27)):
        print(xs,inspect(xs))
