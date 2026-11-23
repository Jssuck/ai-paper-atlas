"""Euclid VII.10 with exact integer counts."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Proof:
    m: int
    n: int
    g: int
    h: int
    comparison: tuple[int, int]
    aggregation: str


def compare(ab: int, c: int, de: int, f: int) -> Proof:
    if any(type(x) is not int or x <= 1 for x in (ab, c, de, f)):
        raise ValueError("given numbers must be integers greater than one")
    g, h = gcd(ab, c), gcd(de, f)
    m, n = ab // g, c // g
    if not 1 < m < n or (de // h, f // h) != (m, n):
        raise ValueError("the two given ratios must be the same proper non-unit fraction")
    if g >= h:
        raise ValueError("the historical comparison requires AB<DE")
    # VII.9: because g is one n-th of C, and h one n-th of F,
    # lifting the local comparison from (g,h) to (C,F) preserves counts.
    common = gcd(g, h)
    local = g // common, h // common
    if (local[0] * n * common, local[1] * n * common) != (c, f):
        raise ArithmeticError("unit-pair comparison failed")
    # VII.5 (one part) or VII.6 (multiple parts): pool m matched pairs.
    combined = tuple(sum(block for _ in range(m)) for block in (g, h))
    if combined != (ab, de) or combined != tuple(x * m * common for x in local):
        raise ArithmeticError("matched-pair aggregation failed")
    return Proof(m, n, g, h, local, "VII.5" if local[0] == 1 else "VII.6")


def demo():
    for values in ((8,12,16,24), (8,12,20,30)):
        print(values, compare(*values))


if __name__ == "__main__":
    demo()
