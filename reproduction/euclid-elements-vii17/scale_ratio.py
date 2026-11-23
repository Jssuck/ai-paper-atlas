"""Exact integer model of Euclid VII.17."""
from dataclasses import dataclass
from math import gcd


def reduced(x, y):
    g = gcd(x, y)
    return x // g, y // g


def nonunits(*values):
    if any(type(x) is not int or x <= 1 for x in values):
        raise ValueError("given numbers must be integers greater than one")


@dataclass(frozen=True)
class Trace:
    products: tuple[int, int]
    measure_counts: tuple[int, int]
    internal_ratio: tuple[int, int]
    crossed_ratio: tuple[int, int]


def compare_products(a, b, c, d, e):
    """Check claimed products before comparing their ratio."""
    nonunits(a,b,c,d,e)
    bd, leftover_d = divmod(d,b)
    ce, leftover_e = divmod(e,c)
    if (bd,ce) != (a,a) or leftover_d or leftover_e:
        raise ValueError("products must have the same specified measure count A")
    internal = reduced(b,d)
    if internal != reduced(c,e):
        raise ArithmeticError("common unit part failed")
    crossed = reduced(b,c)
    if crossed != reduced(d,e):
        raise ArithmeticError("alternation failed")
    return Trace((d,e),(bd,ce),internal,crossed)


def scale(a, b, c):
    nonunits(a,b,c)
    # Separate sums of A copies, rather than use ratio equality to infer E.
    d = sum(b for _ in range(a))
    e = sum(c for _ in range(a))
    return compare_products(a,b,c,d,e)


if __name__ == "__main__":
    print(scale(3,4,6))
