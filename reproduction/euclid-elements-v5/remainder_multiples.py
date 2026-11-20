"""Exact positive rational model of Euclid V.5."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str

    def __post_init__(self):
        if type(self.value) not in (int, Fraction) or self.value <= 0:
            raise ValueError("expected a positive exact magnitude")
        if not isinstance(self.kind, str) or not self.kind:
            raise ValueError("expected a nonempty quantity kind")
        object.__setattr__(self, "value", Fraction(self.value))


@dataclass(frozen=True)
class Result:
    factor: int
    large_remainder: Fraction
    small_remainder: Fraction
    auxiliary_small_remainder: Fraction
    rebuilt_small_whole: Fraction
    added_large_remainder: Fraction
    rebuilt_large_whole: Fraction


def copies(value, factor):
    return sum((value for _ in range(factor)), Fraction(0))


def solve(large, small, large_part, small_part):
    if len({x.kind for x in (large, small, large_part, small_part)}) != 1:
        raise ValueError("all four magnitudes must be of the same kind")
    a, b, x, y = (q.value for q in (large, small, large_part, small_part))
    if not (x < a and y < b):
        raise ValueError("removed quantities must be proper parts")
    common = a / b
    if common.denominator != 1 or common < 2 or x / y != common:
        raise ValueError("wholes and parts must share a strict integer factor")
    m = common.numerator
    large_rest, small_rest = a - x, b - y

    # Original architecture: build CG by division, then V.1 and cancellation.
    cg = large_rest / m
    gf = cg + y
    if copies(gf, m) != x + large_rest or gf != b or gf - y != small_rest or cg != small_rest:
        raise ArithmeticError("auxiliary construction failed")

    # Independent proof geometry: build a comparison large remainder by addition.
    # Once m is known, the rest of this branch never needs division.
    comparison = copies(small_rest, m)
    comparison_whole = x + comparison
    if comparison_whole != copies(y + small_rest, m) or comparison_whole != a or comparison != large_rest:
        raise ArithmeticError("addition-only construction failed")
    return Result(m, large_rest, small_rest, cg, gf, comparison, comparison_whole)


def make_case(a, b, x, y, kind="length"):
    return tuple(Magnitude(v, kind) for v in (a, b, x, y))


def grid():
    """Return verified rows and rejected proper-part mismatches."""
    good = rejected = 0
    values = (Fraction(1, 7), Fraction(2, 5), Fraction(3, 2))
    for kind, part, remainder, m in product(("length", "area"), values, values, range(2, 6)):
        total = part + remainder
        actual = solve(*make_case(m * total, total, m * part, part, kind))
        expected = Result(m, m * remainder, remainder, remainder, total, m * remainder, m * total)
        if actual != expected:
            raise ArithmeticError("exact grid check failed")
        good += 1
        try:
            solve(*make_case(m * total, total, m * part + remainder / 2, part, kind))
        except ValueError as e:
            if "strict integer factor" not in str(e):
                raise
            rejected += 1
        else:
            raise ArithmeticError("mismatched proper parts were accepted")
    return good, rejected


if __name__ == "__main__":
    result = solve(*make_case(15, 5, 6, 2))
    print("factor:", result.factor)
    print("original auxiliary / rebuilt small whole:", result.auxiliary_small_remainder, result.rebuilt_small_whole)
    print("addition-only auxiliary / rebuilt large whole:", result.added_large_remainder, result.rebuilt_large_whole)
    print("large / small remainders:", result.large_remainder, result.small_remainder)
    print("grid (valid, mismatched parts rejected):", grid())
