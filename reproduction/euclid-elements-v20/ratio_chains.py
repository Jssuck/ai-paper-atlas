"""Positive exact rational teaching model for Elements V.20."""
from dataclasses import dataclass
from fractions import Fraction


def cmp(x, y):
    """Trichotomy of two comparable values."""
    return (x > y) - (x < y)


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str

    def __post_init__(self):
        if type(self.value) not in (int, Fraction):
            raise TypeError("expected int or Fraction, not bool or float")
        if self.value <= 0:
            raise ValueError("magnitudes must be positive")
        if type(self.kind) is not str or not self.kind.strip():
            raise ValueError("expected a nonempty kind")
        object.__setattr__(self, "value", Fraction(self.value))


def ratio(x, y):
    if x.kind != y.kind:
        raise ValueError("a ratio requires magnitudes of the same kind")
    return x.value / y.value


@dataclass(frozen=True)
class Trace:
    left_ratio: Fraction
    left_reversed_ratio: Fraction
    right_ratio: Fraction
    right_reversed_ratio: Fraction
    sign: int


def verify_v20(left, right):
    """Trace V.8/V.7, inversion, transfer, and V.10/V.9 numerically.

    < is the dual of >; comparing in both directions at once avoids an
    extra call. This does not multiply adjacent ratios.
    """
    a, b, c = left
    d, e, f = right
    if any(not isinstance(m, Magnitude) for m in (a, b, c, d, e, f)):
        raise TypeError("each entry must be a Magnitude")
    ab, de = ratio(a, b), ratio(d, e)
    bc, ef = ratio(b, c), ratio(e, f)
    if ab != de:
        raise ValueError("first adjacent ratio does not match")
    if bc != ef:
        raise ValueError("second adjacent ratio does not match")
    # Simultaneous inversion of the second pair, V.7 corollary.
    cb, fe = 1 / bc, 1 / ef
    source_sign = cmp(a.value, c.value)
    # V.8/V.7 (or dual): compare ratios with the same second term.
    ratio_sign = cmp(ab, cb)
    if ratio_sign != source_sign:
        raise ArithmeticError("unexpected sign before transfer")
    # V.13 (or equality via V.11): transfer ratio order.
    transferred_sign = cmp(de, fe)
    if transferred_sign != ratio_sign:
        raise ArithmeticError("unexpected sign during transfer")
    # V.10/V.9 (or dual): same second term, so compare numerators.
    if cmp(d.value, f.value) != transferred_sign:
        raise ArithmeticError("unexpected sign after transfer")
    return Trace(ab, cb, de, fe, transferred_sign)


def chain(values, kind):
    return tuple(Magnitude(value, kind) for value in values)


def demo():
    for left, right in (
        ((6, 4, 3), (12, 8, 6)),
        ((6, 4, 6), (12, 8, 12)),
        ((3, 4, 6), (6, 8, 12)),
    ):
        t = verify_v20(chain(left, "line"), chain(right, "area"))
        print(f"{left} / {right}: middle-based ratios "
              f"({t.left_ratio}, {t.left_reversed_ratio}) and "
              f"({t.right_ratio}, {t.right_reversed_ratio}); sign {t.sign:+d}")
    for bad in ((12, 8, 15), (12, 20, 15)):
        try:
            verify_v20(chain((6, 4, 3), "line"), chain(bad, "area"))
        except ValueError as exc:
            print(f"{bad}: rejected ({exc}); endpoints 12 < 15")


if __name__ == "__main__":
    demo()
