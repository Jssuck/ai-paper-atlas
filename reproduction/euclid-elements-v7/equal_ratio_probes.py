"""Exact positive rational model of the two conclusions in Euclid V.7."""
from fractions import Fraction
from dataclasses import dataclass


@dataclass(frozen=True)
class Quantity:
    value: Fraction
    kind: str = "length"

    def __post_init__(self):
        if type(self.value) is not int and not isinstance(self.value, Fraction):
            raise TypeError("expected exact integer or Fraction")
        object.__setattr__(self, "value", Fraction(self.value))
        if self.value <= 0 or not isinstance(self.kind, str) or not self.kind:
            raise ValueError("expected positive quantity and kind")


def _same_kind(a, b, c):
    if not a.kind == b.kind == c.kind:
        raise ValueError("all three quantities must share a kind")


def compare(a, b):
    return (a > b) - (a < b)


def probes(a, b, c, p, q):
    """Return forward and reverse sign pairs, without assuming A=B."""
    _same_kind(a, b, c)
    if any(type(k) is not int or k < 1 for k in (p, q)):
        raise ValueError("positive integer probe coefficients required")
    a, b, c = a.value, b.value, c.value
    return ((compare(p*a, q*c), compare(p*b, q*c)),
            (compare(p*c, q*a), compare(p*c, q*b)))


def verify(a, b, c, p, q):
    _same_kind(a, b, c)
    if a.value != b.value:
        raise ValueError("A and B are not equal")
    return probes(a, b, c, p, q)


def equality_witness(a, b, c):
    """Find a forward distinguishing probe via equality on A:C."""
    _same_kind(a, b, c)
    if a.value == b.value:
        return None
    ratio = a.value / c.value
    p, q = ratio.denominator, ratio.numerator
    return p, q, probes(a, b, c, p, q)[0]


def finite_grid():
    total, signs = 0, set()
    choices = (Fraction(1, 3), Fraction(3, 2), Fraction(5, 3), Fraction(8, 5))
    for kind in ("length", "area"):
        for x in choices:
            for y in choices:
                a, b, c = Quantity(x, kind), Quantity(x, kind), Quantity(y, kind)
                for p in range(1, 7):
                    for q in range(1, 7):
                        forward, reverse = verify(a, b, c, p, q)
                        swapped, _ = verify(a, b, c, q, p)
                        if forward[0] != forward[1] or reverse[0] != reverse[1]:
                            raise ArithmeticError("equal inputs disagreed")
                        if reverse != tuple(-s for s in swapped):
                            raise ArithmeticError("swapped-index sign reversal disagreed")
                        signs.update(forward + reverse)
                        total += 1
    return total, tuple(sorted(signs))


if __name__ == "__main__":
    print("grid (paired probes, observed signs):", finite_grid())
    t = Quantity(Fraction(17, 16)), Quantity(Fraction(18, 17)), Quantity(1)
    print("distinguishing forward probe:", equality_witness(*t))
