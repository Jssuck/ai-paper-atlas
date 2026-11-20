"""Exact modern teaching model of Elements V.Def.1–7 on Q(sqrt(2))."""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product


def _fraction(x):
    if type(x) not in (int, Fraction):
        raise TypeError("use int or Fraction; no floating-point input")
    return Fraction(x)


def _sign(x):
    return (x > 0) - (x < 0)


@dataclass(frozen=True)
class Q2:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, "a", _fraction(self.a))
        object.__setattr__(self, "b", _fraction(self.b))

    def __sub__(self, other):
        return Q2(self.a - other.a, self.b - other.b)

    def scale(self, multiplier):
        k = _fraction(multiplier)
        return Q2(k * self.a, k * self.b)

    def sign(self):
        sa, sb = _sign(self.a), _sign(self.b)
        if not sa or not sb or sa == sb:
            return sa or sb
        # Opposite signs: compare the squares of the positive absolute terms.
        return sa * _sign(self.a**2 - 2 * self.b**2)


@dataclass(frozen=True)
class Magnitude:
    value: Q2
    kind: str

    def __post_init__(self):
        if not isinstance(self.value, Q2):
            raise TypeError("expected Q2 magnitude")
        if self.value.sign() <= 0:
            raise ValueError("the model uses strictly positive magnitudes")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("kind must be a nonempty label")


def _same_kind(a, b):
    if a.kind != b.kind:
        raise ValueError("the two magnitudes of each pair must have the same kind")


def measure(part, whole):
    """Positive integer k with k * part = whole, or None (including equal parts)."""
    _same_kind(part, whole)
    p, w = part.value, whole.value
    if (w - p).sign() <= 0:
        return None
    k = w.a / p.a if p.a else w.b / p.b
    return int(k) if k.denominator == 1 and p.scale(k) == w else None


def exceeding_multipliers(a, b):
    """Two strict witnesses m*a>b and n*b>a for V.Def.4, not least witnesses."""
    _same_kind(a, b)

    def one(left, right):
        k = 1
        while (left.value.scale(k) - right.value).sign() <= 0:
            k *= 2
        return k

    return one(a, b), one(b, a)


@dataclass(frozen=True)
class Ratio:
    first: Magnitude
    second: Magnitude

    def __post_init__(self):
        _same_kind(self.first, self.second)

    def compare_multiples(self, m, n):
        if type(m) is not int or type(n) is not int or m < 1 or n < 1:
            raise ValueError("multipliers are positive integers")
        return (self.first.value.scale(m) - self.second.value.scale(n)).sign()


def witness(left, right, bound, *, greater=False):
    """Find bounded D5 disagreement or a directional D7 (> vs <=) witness."""
    if type(bound) is not int or bound < 1:
        raise ValueError("bound is a positive integer")
    for m, n in product(range(1, bound + 1), repeat=2):
        p, q = left.compare_multiples(m, n), right.compare_multiples(m, n)
        matches = p > 0 and q <= 0 if greater else p != q
        if matches:
            return m, n, p, q
    return None  # unknown at this bound; not a certificate of equality


def example_ratio(a, b, kind="length"):
    return Ratio(Magnitude(a, kind), Magnitude(b, kind))


def examples():
    surd = example_ratio(Q2(0, 1), Q2(1))
    rational = example_ratio(Q2(7), Q2(5), "area")
    near_high = example_ratio(Q2(101), Q2(100))
    near_low = example_ratio(Q2(102), Q2(101))
    return surd, rational, near_high, near_low


if __name__ == "__main__":
    s, r, h, l = examples()
    for label, left, right, bound in [("surd/rational", s, r, 6), ("two rationals", h, l, 100)]:
        print(label, "bound", bound, "D5 disagreement", witness(left, right, bound))
        for limit in (bound + 1, bound + 2):
            print("bound", limit, "D5 disagreement", witness(left, right, limit),
                  "| D7 witness", witness(left, right, limit, greater=True))
