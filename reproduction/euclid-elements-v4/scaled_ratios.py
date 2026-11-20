"""Exact bounded sign probes for the change of indices in Euclid V.4."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __init__(self, value, kind="length"):
        if type(value) not in (int, Fraction):
            raise TypeError("expected exact integer or Fraction")
        if value <= 0 or not isinstance(kind, str) or not kind.strip():
            raise ValueError("expected a positive tagged magnitude")
        object.__setattr__(self, "value", Fraction(value))
        object.__setattr__(self, "kind", kind)


def positive_integer(k):
    if type(k) is not int or k < 1:
        raise ValueError("expected a positive integer")
    return k


@dataclass(frozen=True)
class Ratio:
    first: Magnitude
    second: Magnitude

    def __post_init__(self):
        if self.first.kind != self.second.kind:
            raise ValueError("ratio requires one kind within each pair")

    def scale(self, u, v):
        return Ratio(Magnitude(self.first.value * positive_integer(u), self.first.kind),
                     Magnitude(self.second.value * positive_integer(v), self.second.kind))

    def sign(self, p, q):
        x = positive_integer(p) * self.first.value - positive_integer(q) * self.second.value
        return (x > 0) - (x < 0)


def equal_oracle(left, right):
    """Compare scalar coordinates after each pair uses one unit."""
    return left.first.value * right.second.value == left.second.value * right.first.value


def mismatch(left, right, limit):
    """None signifies only that the bounded probe grid has no disagreement."""
    for p, q in product(range(1, positive_integer(limit) + 1), repeat=2):
        s, t = left.sign(p, q), right.sign(p, q)
        if s != t:
            return p, q, s, t
    return None


def mapped_probe(ratio, u, v, p, q):
    scaled = ratio.scale(u, v).sign(p, q)
    source = ratio.sign(u * p, v * q)
    return scaled, source


def ratio(a, b, kind="length"):
    return Ratio(Magnitude(a, kind), Magnitude(b, kind))


def regression_grid():
    cases = checked = 0
    values = (Fraction(1, 2), Fraction(2, 3), Fraction(7, 4))
    for x, a, b, u, v in product(values, values, values, range(1, 5), range(1, 5)):
        left, right = ratio(x * a, a), ratio(x * b, b, "area")
        if not equal_oracle(left, right) or not equal_oracle(left.scale(u, v), right.scale(u, v)):
            raise ArithmeticError("oracle did not preserve exact equality")
        cases += 1
        for p, q in product(range(1, 5), repeat=2):
            s, t = mapped_probe(left, u, v, p, q)
            r, k = mapped_probe(right, u, v, p, q)
            if not (s == t == r == k):
                raise ArithmeticError("equimultiple signs disagree")
            checked += 1
    return cases, checked


if __name__ == "__main__":
    x, y = ratio(3, 2), ratio(6, 4, "area")
    print("sign before/after at (1,2):", x.sign(1, 2), x.scale(2, 1).sign(1, 2))
    print("matched-scale equality:", equal_oracle(x.scale(2, 1), y.scale(2, 1)))
    print("wrong-scale witness:", mismatch(x.scale(2, 1), y, 4))
    print("bounded agreement / exact oracle:", mismatch(ratio(101,100), ratio(102,101), 100),
          equal_oracle(ratio(101,100), ratio(102,101)))
    print("grid (ratio/scale choices, four-sign checks):", regression_grid())
