"""Exact certificates for the two-stage multiplication in Euclid V.3."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __init__(self, value, kind="length"):
        if type(value) not in (int, Fraction):
            raise TypeError("expected an exact integer or Fraction")
        if value <= 0 or not isinstance(kind, str) or not kind.strip():
            raise ValueError("expected a positive tagged magnitude")
        object.__setattr__(self, "value", Fraction(value))
        object.__setattr__(self, "kind", kind)


def stage_count(terms, bases):
    if len(terms) != 2 or len(bases) != 2:
        raise ValueError("each stage and the bases must have two entries")
    counts = []
    for term, base in zip(terms, bases):
        if term.kind != base.kind:
            raise ValueError("each column must use its base's kind")
        q = term.value / base.value
        if q.denominator != 1 or q < 2:
            raise ValueError("expected a strict integer multiple")
        counts.append(q.numerator)
    if counts[0] != counts[1]:
        raise ValueError("unequal counts within the stage")
    return counts[0]


@dataclass(frozen=True)
class Certificate:
    inner_count: int
    outer_count: int
    total_count: int
    left_total: Magnitude
    right_total: Magnitude


def compose(bases, middle, large):
    """Check both pairwise stages before flattening either column."""
    n = stage_count(middle, bases)
    m = stage_count(large, middle)
    computed = []
    for base in bases:
        block = (base.value,) * n
        blocks = (block,) * m
        value = sum(part for copy in blocks for part in copy)
        computed.append(Magnitude(value, base.kind))
    if tuple(computed) != tuple(large):
        raise ArithmeticError("flattening did not reproduce the given quantities")
    return Certificate(n, m, m * n, *computed)


def regression_grid():
    scales = (Fraction(1, 2), Fraction(2, 3), Fraction(7, 4))
    valid = invalid = 0
    for a, b, n, m in product(scales, scales, range(2, 6), range(2, 6)):
        bases = Magnitude(a), Magnitude(b, "area")
        middle = Magnitude(n * a), Magnitude(n * b, "area")
        large = Magnitude(m * n * a), Magnitude(m * n * b, "area")
        cert = compose(bases, middle, large)
        if (cert.total_count, cert.left_total, cert.right_total) != (n * m, *large):
            raise ArithmeticError("direct product disagrees")
        valid += 1
        if n == m:
            continue
        # Swap phases on just one side. The output totals are unchanged.
        shifted = Magnitude(n * a), Magnitude(m * b, "area")
        try:
            compose(bases, shifted, large)
        except ValueError as error:
            if str(error) != "unequal counts within the stage":
                raise
        else:
            raise ArithmeticError("compensating phase counts accepted")
        invalid += 1
    return valid, invalid


if __name__ == "__main__":
    bases = Magnitude(Fraction(3, 2)), Magnitude(Fraction(5, 2), "area")
    middle = Magnitude(3), Magnitude(5, "area")
    large = Magnitude(9), Magnitude(15, "area")
    c = compose(bases, middle, large)
    print("inner / outer / flattened:", c.inner_count, c.outer_count, c.total_count)
    print("column totals:", c.left_total.value, c.right_total.value)
    print("grid (valid nestings, phase swaps rejected):", regression_grid())
