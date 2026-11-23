"""Finite exact teaching certificates for Euclid VII.21."""
from dataclasses import dataclass
from math import gcd


def divisor_count(a, b, c, d):
    """Given the VII.20 equal counts, make the VII.16 transfer explicit."""
    if any(type(x) is not int or x <= 1 for x in (a,b,c,d)):
        raise ValueError("expected nonunit positive integers")
    if not (c < a and d < b):
        raise ValueError("need a strictly smaller pair")
    k, r = divmod(a,c)
    h, s = divmod(b,d)
    if r or s or k != h or k <= 1:
        raise ValueError("no common nonunit measurement count")
    if (sum(k for _ in range(c)),sum(k for _ in range(d))) != (a,b):
        raise ArithmeticError("VII.16 transfer failed")
    return k


@dataclass(frozen=True)
class Diagnostic:
    least: tuple[int,int]
    count: int
    coprime: bool


def analyze(a,b):
    """Modern gcd diagnostic: not a reenactment of the original contradiction."""
    if any(type(x) is not int or x <= 1 for x in (a,b)):
        raise ValueError("expected nonunit positive integers")
    k = gcd(a,b)
    c,d = a//k,b//k
    if k > 1 and min(c,d) > 1 and divisor_count(a,b,c,d) != k:
        raise ArithmeticError("unexpected witness")
    return Diagnostic((c,d),k,k == 1)


if __name__ == "__main__":
    for pair in ((8,15),(16,30),(12,18)):
        print(pair,analyze(*pair))
