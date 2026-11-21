"""Positive exact rational teaching model for Elements V.21."""
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


def verify_v21(left, right):
    """Trace the opposite edge alignment using exact rational quotients.

    The three-way numerical comparison is a teaching model. V.21's
    written proof expands the greater case but abbreviates the others.
    """
    a, b, c = left
    d, e, f = right
    if any(not isinstance(m, Magnitude) for m in (a, b, c, d, e, f)):
        raise TypeError("each entry must be a Magnitude")
    ab, ef = ratio(a, b), ratio(e, f)
    bc, de = ratio(b, c), ratio(d, e)
    if ab != ef:
        raise ValueError("first perturbed pair A:B / E:F does not match")
    if bc != de:
        raise ValueError("second perturbed pair B:C / D:E does not match")
    # V.8 / V.7: same subsequent term B; keep the left order.
    source_sign = cmp(a.value, c.value)
    cb, ed = 1 / bc, 1 / de  # invert both terms of the second pair
    ratio_sign = cmp(ab, cb)
    if ratio_sign != source_sign:
        raise ArithmeticError("unexpected sign before transfer")
    # V.13 / V.11: transfer the ratio order to same antecedent E.
    transferred_sign = cmp(ef, ed)
    if transferred_sign != ratio_sign:
        raise ArithmeticError("unexpected sign during transfer")
    # V.10 / V.9: the second terms compare in reverse order (D vs F).
    if -cmp(f.value, d.value) != transferred_sign:
        raise ArithmeticError("unexpected sign after transfer")
    return Trace(ab, cb, ef, ed, transferred_sign)


def chain(values, kind):
    return tuple(Magnitude(value, kind) for value in values)


def demo():
    for left, right in (
        ((6, 4, 3), (8, 6, 4)),
        ((6, 4, 6), (8, 12, 8)),
        ((3, 4, 6), (4, 6, 8)),
    ):
        t = verify_v21(chain(left, "line"), chain(right, "area"))
        print(f"{left} / {right}: A:B,C:B = ({t.left_ratio}, {t.left_reversed_ratio}); "
              f"E:F,E:D = ({t.right_ratio}, {t.right_reversed_ratio}); sign {t.sign:+d}")
    for right in ((3, 6, 4), (8, 6, 10), (12, 8, 6)):
        try:
            verify_v21(chain((6, 4, 3), "line"), chain(right, "area"))
        except ValueError as exc:
            print(f"{right}: rejected ({exc}); D–F order {cmp(right[0], right[2]):+d}")
        else:
            raise RuntimeError("expected perturbed group mismatch")


if __name__ == "__main__":
    demo()
