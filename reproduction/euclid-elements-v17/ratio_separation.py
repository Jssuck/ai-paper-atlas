"""Euclid V.17, replayed in a typed positive-rational model."""
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

    def __add__(self, other):
        same_kind(self, other)
        return Magnitude(self.value + other.value, self.kind)


def same_kind(a, b):
    if a.kind != b.kind:
        raise ValueError("operations within a pair require matching kinds")


def sgn(a, b):
    return (a > b) - (a < b)


def cmp(a, b):
    same_kind(a, b)
    return sgn(a.value, b.value)


def ratio(a, b):
    same_kind(a, b)
    return a.value / b.value


@dataclass(frozen=True)
class Replay:
    whole_ratios: tuple
    remainder_ratios: tuple
    whole_pairs: tuple
    remainder_pairs: tuple
    canceled: tuple
    whole_signs: tuple
    remainder_signs: tuple


def replay(x, y, z, w, p, q):
    """Check whole ratios, build probes, cancel, and expose both sign pairs.

    x,y and z,w are each homogeneous, but the groups may differ in kind.
    Quotient equality and quotient-vs-threshold are modern rational oracles.
    """
    groups = ((x, y), (z, w))
    wholes = tuple((a + b, b) for a, b in groups)
    whole_ratios = tuple(ratio(ab, b) for ab, b in wholes)
    if whole_ratios[0] != whole_ratios[1]:
        raise ValueError("hypothesis (x+y):y ~ (z+w):w is false")

    whole_pairs, remainder_pairs, canceled = [], [], []
    for (a, b), (ab, _) in zip(groups, wholes):
        left = ab.scale(p)
        pb, pa, qb = b.scale(p), a.scale(p), b.scale(q)
        right = pb + qb
        if left != pa + pb or right != b.scale(p + q):
            raise ArithmeticError("V.1 / V.2 expansion mismatch")
        whole_pairs.append((left, right))
        remainder_pairs.append((pa, qb))
        canceled.append(pb)

    whole_signs = tuple(cmp(a, b) for a, b in whole_pairs)
    rem_signs = tuple(cmp(a, b) for a, b in remainder_pairs)
    if whole_signs[0] != whole_signs[1]:  # V.Def.5 at (p, p+q)
        raise ArithmeticError("whole-ratio probe mismatch")
    if rem_signs != whole_signs:
        raise ArithmeticError("cancellation changed a comparison sign")

    remainders = tuple(ratio(a, b) for a, b in groups)
    threshold = Fraction(q, p)
    if rem_signs != tuple(sgn(r, threshold) for r in remainders):
        raise ArithmeticError("independent threshold check failed")
    return Replay(whole_ratios, remainders, tuple(whole_pairs),
                  tuple(remainder_pairs), tuple(canceled), whole_signs,
                  rem_signs)


def demo():
    x, y = map(Magnitude, (2, 3))
    z, w = (Magnitude(v, "area") for v in (4, 6))
    print("x,y=2,3 (length); z,w=4,6 (area)")
    for p, q in ((1, 1), (3, 2), (2, 1)):
        r = replay(x, y, z, w, p, q)
        fmt = lambda pairs: " | ".join(f"{a.value}:{b.value}" for a, b in pairs)
        print(f"p={p} q={q}: compared wholes {fmt(r.whole_pairs)} "
              f"-> remainders {fmt(r.remainder_pairs)}; signs={r.remainder_signs}")
    print("whole quotients: 5/3, 5/3; remainder quotients: 2/3, 2/3")


if __name__ == "__main__":
    demo()
