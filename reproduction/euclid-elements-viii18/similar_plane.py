"""Exact mixed-product construction for Euclid VIII.18."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Trace:
    chain: tuple[int,int,int]
    alternate_middle: int
    growth: Fraction


def construct(c,d,e,f,*,modern=False):
    if any(type(x) is not int or x < (1 if modern else 2) for x in (c,d,e,f)):
        raise ValueError("positive integral factors required, nonunits by default")
    if c*f != d*e:
        raise ValueError("paired factors are not similar")
    if c == e and not modern:
        raise ValueError("equal pairs require modern=True")
    a,g,b = c*d,d*e,e*f
    growth = Fraction(e,c)
    if g*g != a*b or Fraction(b,a) != growth**2:
        raise ArithmeticError("continued proportion certificate failed")
    return Trace((a,g,b),c*f,growth)


if __name__ == "__main__":
    print(construct(4,6,6,9))
