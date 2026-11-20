"""Exact certificates for the two-row composition in Euclid V.2."""
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


@dataclass(frozen=True)
class Certificate:
    first_count: int
    second_count: int
    total_count: int
    left_total: Magnitude
    right_total: Magnitude


def row_count(row, bases):
    if len(row) != 2 or len(bases) != 2:
        raise ValueError("each row and the bases must have two entries")
    counts = []
    for term, base in zip(row, bases):
        if term.kind != base.kind:
            raise ValueError("each column must use its base's kind")
        q = term.value / base.value
        if q.denominator != 1 or q < 2:
            raise ValueError("expected a strict integer multiple")
        counts.append(q.numerator)
    if counts[0] != counts[1]:
        raise ValueError("unequal counts within the row")
    return counts[0]


def compose(first, second, bases):
    """Check both hypotheses before deriving either total."""
    m = row_count(first, bases)
    n = row_count(second, bases)
    left = Magnitude(first[0].value + second[0].value, bases[0].kind)
    right = Magnitude(first[1].value + second[1].value, bases[1].kind)
    return Certificate(m, n, m + n, left, right)


def regression_grid():
    """Compare the certificate to explicit concatenations in each column."""
    valid = invalid = 0
    scales = (Fraction(1, 2), Fraction(2, 3), Fraction(7, 4))
    for a, b, m, n in product(scales, scales, range(2, 6), range(2, 6)):
        bases = (Magnitude(a), Magnitude(b, "area"))
        first = (Magnitude(a * m), Magnitude(b * m, "area"))
        second = (Magnitude(a * n), Magnitude(b * n, "area"))
        c = compose(first, second, bases)
        expected = sum([a] * m + [a] * n), sum([b] * m + [b] * n)
        if (c.total_count, c.left_total.value, c.right_total.value) != (m + n, *expected):
            raise ArithmeticError("copy check failed")
        valid += 1
        # Reallocate counts on the right between rows, preserving both totals.
        # Positive controls include n=2; choose allocation direction accordingly.
        if n > 2:
            mr, nr = m + 1, n - 1
        elif m > 2:
            mr, nr = m - 1, n + 1
        else:
            continue
        wrong_first = (first[0], Magnitude(b * mr, "area"))
        wrong_second = (second[0], Magnitude(b * nr, "area"))
        if wrong_first[1].value + wrong_second[1].value != c.right_total.value:
            raise ArithmeticError("control should preserve the right total")
        try:
            compose(wrong_first, wrong_second, bases)
        except ValueError as error:
            if str(error) != "unequal counts within the row":
                raise
        else:
            raise ArithmeticError("compensating error accepted")
        invalid += 1
    return valid, invalid


if __name__ == "__main__":
    bases = (Magnitude(Fraction(3, 2)), Magnitude(Fraction(5, 2), "area"))
    c = compose((Magnitude(3), Magnitude(5, "area")),
                (Magnitude(Fraction(9, 2)), Magnitude(Fraction(15, 2), "area")), bases)
    print("first / second / total count:", c.first_count, c.second_count, c.total_count)
    print("column totals:", c.left_total.value, c.right_total.value)
    print("grid (valid compositions, compensating errors rejected):", regression_grid())
