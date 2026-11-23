"""Exact finite reconstruction of the witness chain in Euclid VII.24."""
from dataclasses import dataclass
from math import gcd


def nonunits(*values):
    if any(type(x) is not int or x <= 1 for x in values):
        raise ValueError("require positive nonunit integers")


@dataclass(frozen=True)
class Trace:
    d: int
    e: int
    f: int
    least_pair: tuple[int, int]
    scale: int


def force_divisor(a, b, c, e):
    """Given E dividing C and AB, force E to divide B if A and C are coprime."""
    nonunits(a,b,c,e)
    if gcd(a,c) != 1:
        raise ValueError("A and C must be coprime")
    d = sum(a for _ in range(b))
    f, r = divmod(d,e)
    if c%e or r:
        raise ValueError("E must divide both C and D")
    if gcd(e,a) != 1:  # VII.23: E divides C, which is coprime to A.
        raise ArithmeticError("coprimality did not transfer")
    if e*f != a*b:  # VII.19: E:A = B:F.
        raise ArithmeticError("cross products differ")
    # VII.21 makes (E,A) least; VII.20 forces the same integer scale.
    scale, remainder = divmod(b,e)
    if remainder or (scale*a != f):
        raise ArithmeticError("least ratio did not give an integer scale")
    return Trace(d,e,f,(e,a),scale)


def certificate(a,b,c):
    nonunits(a,b,c)
    if gcd(a,c) != 1 or gcd(b,c) != 1:
        raise ValueError("A and B must each be coprime to C")
    d = sum(a for _ in range(b))
    for e in range(2,c+1):
        if c%e == d%e == 0:
            raise ArithmeticError(f"impossible common measure: {force_divisor(a,b,c,e)}")
    return d


if __name__ == "__main__":
    print("product:",certificate(8,9,35))
    print("hypothetical chain with B:C hypothesis dropped:",force_divisor(8,10,35,5))
