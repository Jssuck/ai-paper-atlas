"""Exact row and column certificates for the finite-copy argument in V.1."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __init__(self, value, kind="length"):
        if type(value) not in (int, Fraction):
            raise TypeError("expected an exact integer or Fraction")
        if value <= 0 or not isinstance(kind, str) or not kind.strip():
            raise ValueError("magnitude must be positive and tagged")
        object.__setattr__(self, "value", Fraction(value))
        object.__setattr__(self, "kind", kind)


def common_multiple(large, bases):
    if not large or len(large) != len(bases):
        raise ValueError("expected nonempty lists of the same length")
    counts = []
    for g, b in zip(large, bases):
        if g.kind != b.kind:
            raise ValueError("each pair must use the same kind")
        quotient = g.value / b.value
        if quotient.denominator != 1 or quotient < 2:
            raise ValueError("expected a strict integer multiple")
        counts.append(quotient.numerator)
    if any(n != counts[0] for n in counts):
        raise ValueError("multiplicities differ")
    return counts[0]


def proof_columns(large, bases):
    """Repeat the entire base tuple; no addition across different kinds."""
    k = common_multiple(large, bases)
    bases = tuple(bases)
    rows = tuple((b,) * k for b in bases)
    return k, rows, tuple(zip(*rows))


def totals(magnitudes):
    if not magnitudes or len({m.kind for m in magnitudes}) != 1:
        raise ValueError("addition needs a nonempty homogeneous list")
    return Magnitude(sum(m.value for m in magnitudes), magnitudes[0].kind)


def aggregate_certificate(large, bases):
    k, _, columns = proof_columns(large, bases)
    total_base = totals(bases)
    total_large = totals(large)
    if totals(tuple(totals(col) for col in columns)) != total_large:
        raise ArithmeticError("aggregate does not match column sums")
    return k, total_large, total_base


def regression_grid():
    """Deterministically test grouping against a direct linear expression."""
    good = wrong = 0
    from itertools import product
    for a, b, c in product((Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)), repeat=3):
        bases = tuple(Magnitude(v) for v in (a, b, c))
        for k in range(2, 8):
            large = tuple(Magnitude(k * v) for v in (a, b, c))
            n, whole, base = aggregate_certificate(large, bases)
            if (n, whole.value, base.value) != (k, k * (a + b + c), a + b + c):
                raise ArithmeticError("positive model mismatch")
            good += 1
            changed = large[:-1] + (Magnitude((k + 1) * c),)
            try:
                aggregate_certificate(changed, bases)
            except ValueError as error:
                if str(error) != "multiplicities differ":
                    raise
            else:
                raise ArithmeticError("different factors accepted")
            wrong += 1
    return good, wrong


if __name__ == "__main__":
    bases = (Magnitude(Fraction(3, 2)), Magnitude(Fraction(5, 2)))
    large = (Magnitude(Fraction(9, 2)), Magnitude(Fraction(15, 2)))
    k, rows, columns = proof_columns(large, bases)
    print("factor / rows / columns:", k, len(rows), len(columns))
    print("sum of one column / total:", totals(columns[0]).value, totals(large).value)
    print("grid (valid groupings, differing factors rejected):", regression_grid())
