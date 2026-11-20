"""Euclid V.19 and the transmitted porism in the typed rational model."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __post_init__(self):
        if type(self.value) not in (int, Fraction):
            raise TypeError("use integers or exact Fractions")
        if self.value <= 0:
            raise ValueError("expected a positive magnitude")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("expected a nonempty kind")
        object.__setattr__(self, "value", Fraction(self.value))

    def __add__(self, other):
        same_kind(self, other)
        return Magnitude(self.value + other.value, self.kind)

    def __sub__(self, other):
        same_kind(self, other)
        return Magnitude(self.value - other.value, self.kind)

    def scale(self, k):
        if type(k) is not int or k <= 0:
            raise ValueError("expected a positive integer probe")
        return Magnitude(self.value * k, self.kind)


def same_kind(a, b):
    if a.kind != b.kind:
        raise ValueError("magnitude kinds differ within a pair")


def sgn(a, b):
    return (a > b) - (a < b)


def compare(a, b):
    same_kind(a, b)
    return sgn(a.value, b.value)


def ratio(a, b):
    same_kind(a, b)
    return a.value / b.value


def proportion(a, b, c, d):
    """Exact rational oracle; not a finite approximation to V.Def.5."""
    return ratio(a, b) == ratio(c, d)


def cut(whole, removed):
    if compare(whole, removed) != 1:
        raise ValueError("removed magnitude must be strictly smaller than whole")
    return whole - removed


def main_trace(a, b, u, v):
    """AB, CD, AE, CF; replay V.16 -> V.17 -> V.16 -> V.11."""
    for x in (b, u, v):
        same_kind(a, x)
    r, s = cut(a, u), cut(b, v)
    if not proportion(a, b, u, v):
        raise ValueError("whole ratio does not match removed ratio")
    steps = (
        ("V.16", (a, u, b, v)),
        ("V.17", (r, u, s, v)),
        ("V.16", (r, s, u, v)),
        ("V.11", (r, s, a, b)),
    )
    if not all(proportion(*items) for _, items in steps):
        raise ArithmeticError("inconsistent replay")
    return tuple((name, ratio(*items[:2]), ratio(*items[2:]))
                 for name, items in steps)


def porism_trace(a, u, b, v):
    """AB, AE, CD, CF; typed alternative: V.17 -> inversion -> V.18."""
    r, s = cut(a, u), cut(b, v)
    if not proportion(a, u, b, v):
        raise ValueError("joint ratios do not match")
    steps = (
        ("V.17", (r, u, s, v)),
        ("inverse", (u, r, v, s)),
        ("V.18", (a, r, b, s)),
    )
    if not all(proportion(*items) for _, items in steps):
        raise ArithmeticError("inconsistent replay")
    return tuple((name, ratio(*items[:2]), ratio(*items[2:]))
                 for name, items in steps)


def demo():
    q = Magnitude
    a, b, u, v = map(q, (10, 15, 4, 6))
    print("main:", [(name, str(x), str(y)) for name, x, y in main_trace(a, b, u, v)])
    b, v = q(15, "area"), q(6, "area")
    print("porism mixed-kind:",
          [(name, str(x), str(y)) for name, x, y in porism_trace(a, u, b, v)])


if __name__ == "__main__":
    demo()
