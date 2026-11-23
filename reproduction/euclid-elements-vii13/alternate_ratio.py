"""Exact integer-count model of Euclid VII.13."""
from dataclasses import dataclass
from math import gcd


def counts(x, y):
    g = gcd(x, y)
    return x // g, y // g


@dataclass(frozen=True)
class Alternation:
    incoming: tuple[int, int]
    crossed: tuple[int, int]
    route: str
    crossed_kind: str


def alternate(a, b, c, d):
    if any(type(x) is not int or x <= 1 for x in (a, b, c, d)):
        raise ValueError("given numbers must be integers greater than one")
    if not a < b or not a < c:
        raise ValueError("direct model requires proper input and crossed directions")
    incoming = counts(a, b)
    if incoming != counts(c, d):
        raise ValueError("input ratios disagree")
    crossed = counts(a, c)
    if crossed != counts(b, d):
        raise ArithmeticError("crossed part(s) disagree")
    return Alternation(incoming, crossed, "VII.9" if incoming[0] == 1 else "VII.10",
                       "part" if crossed[0] == 1 else "parts")


def demo():
    for args in ((4,8,12,24),(6,12,10,20),(4,6,12,18),(8,12,20,30)):
        print(args, alternate(*args))


if __name__ == "__main__":
    demo()
