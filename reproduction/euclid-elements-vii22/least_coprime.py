"""Finite teaching checks for Euclid VII.22."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Witness:
    measure: int
    smaller: tuple[int, int]


def shrink(a, b, c):
    """Any common nonunit measure gives a strictly smaller proportional pair."""
    if any(type(t) is not int or t <= 1 for t in (a,b,c)):
        raise ValueError("expected nonunit positive integers")
    d, r = divmod(a,c)
    e, s = divmod(b,c)
    if r or s:
        raise ValueError("C must measure both given numbers")
    # VII.17: the same multiplier C makes A and B from D and E.
    if (sum(d for _ in range(c)),sum(e for _ in range(c))) != (a,b):
        raise ArithmeticError("common multiplier did not reconstruct the pair")
    if not (0 < d < a and 0 < e < b):
        raise ArithmeticError("quotient pair did not shrink")
    if min(d,e) == 1:
        raise ValueError("unit quotient falls outside the historical-number model")
    return Witness(c,(d,e))


def diagnostic(a, b):
    """Modern comparison; using gcd is not necessary for the contradiction."""
    if any(type(t) is not int or t <= 1 for t in (a,b)):
        raise ValueError("expected nonunit positive integers")
    c = gcd(a,b)
    return (a//c,b//c), c == 1


if __name__ == "__main__":
    print(shrink(18,30,2), shrink(18,30,6))
    print(diagnostic(8,15))
