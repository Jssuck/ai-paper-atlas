"""A typed positive-rational teaching model of Euclid V.16."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __post_init__(self):
        if type(self.value) not in (int, Fraction):
            raise TypeError("use exact integers or Fractions")
        if self.value <= 0:
            raise ValueError("magnitude must be positive")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("kind must be a nonempty string")
        object.__setattr__(self, "value", Fraction(self.value))

    def scale(self, k):
        if type(k) is not int or k <= 0:
            raise ValueError("probe must be a positive integer")
        return Magnitude(k * self.value, self.kind)


def cmp(left, right):
    if left.kind != right.kind:
        raise ValueError("comparisons require matching kinds")
    return (left.value > right.value) - (left.value < right.value)


def ratio(left, right):
    if left.kind != right.kind:
        raise ValueError("ratios require matching kinds")
    return left.value / right.value


def replay(a, b, c, d, m, n):
    """Return original, scaled, and alternated ratios and comparison signs.

    The Fraction quotients act as a modern oracle for checking substeps;
    V.14 is checked computationally here, not proved by the code.
    """
    start, end = ratio(a, b), ratio(c, d)
    if a.kind != c.kind:
        raise ValueError("alternation requires the same kind across both pairs")
    if start != end:
        raise ValueError("hypothesis A:B ~ C:D is false")
    e, f, g, h = a.scale(m), b.scale(m), c.scale(n), d.scale(n)
    left, right = ratio(e, f), ratio(g, h)
    if start != left or end != right:  # two V.15 steps
        raise ArithmeticError("same-scale ratio was not preserved")
    if left != end or left != right:  # two V.11 steps
        raise ArithmeticError("ratio chain did not close")
    first, second = cmp(e, g), cmp(f, h)  # V.14
    if first != second:
        raise ArithmeticError("V.14 comparison mismatch")
    x, y = ratio(a, c), ratio(b, d)
    threshold = Fraction(n, m)
    signs = tuple((q > threshold) - (q < threshold) for q in (x, y))
    if (first, second) != signs:
        raise ArithmeticError("probe orientation mismatch")
    return (start, end), (left, right), (x, y), (first, second)


def demo():
    a, b, c, d = map(Magnitude, (2, 3, 4, 6))
    print("A,B,C,D = 2,3,4,6 (same kind)")
    for m, n in ((1, 1), (2, 1), (3, 1)):
        orig, scaled, alt, signs = replay(a, b, c, d, m, n)
        fmt = lambda pair: " ~ ".join(map(str, pair))
        print(f"m={m} n={n}; original={fmt(orig)}; scaled={fmt(scaled)}; alternating={fmt(alt)}; signs={signs}")


if __name__ == "__main__":
    demo()
