"""Positive rational model of the equimultiple construction in Euclid V.8."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __post_init__(self):
        if type(self.value) not in (int, Fraction) or self.value <= 0:
            raise ValueError("expected positive int or Fraction")
        if not isinstance(self.kind, str) or not self.kind:
            raise ValueError("expected nonempty kind")
        object.__setattr__(self, "value", Fraction(self.value))


def comparable(*values):
    if len({item.kind for item in values}) != 1:
        raise ValueError("all directly compared magnitudes must have the same kind")


def witness_signs(a, b, c, d, m, n):
    """Compare m*a with n*b and m*c with n*d; each side must be homogeneous."""
    comparable(a, b)
    comparable(c, d)
    if type(m) is not int or type(n) is not int or min(m, n) < 1:
        raise ValueError("multipliers must be positive integers")
    x, y = m*a.value-n*b.value, m*c.value-n*d.value
    return (x > 0) - (x < 0), (y > 0) - (y < 0)


def certifies(a, b, c, d, m, n):
    first, second = witness_signs(a, b, c, d, m, n)
    return first > 0 and second <= 0


def bounded_witness(a, b, c, d, bound):
    """Return a witness if found, never a verdict of equality or non-greater."""
    comparable(a, b)
    comparable(c, d)
    if type(bound) is not int or bound < 1:
        raise ValueError("bound must be a positive integer")
    return next(((m, n) for m in range(1, bound + 1)
                 for n in range(1, bound + 1)
                 if certifies(a, b, c, d, m, n)), None)


@dataclass(frozen=True)
class Construction:
    branch: str
    n: int
    m: int
    small_multiple: Fraction
    large_multiple: Fraction
    shared_multiple: Fraction


def construct(a, b, c):
    """For a>b, construct multipliers such that m*b<n*c<m*a."""
    comparable(a, b, c)
    a, b, c = a.value, b.value, c.value
    if a <= b:
        raise ValueError("expected first magnitude strictly greater than second")
    gap = a - b
    branch = "gap<smaller" if gap < b else "gap>smaller" if gap > b else "gap=smaller"
    m = c // min(gap, b) + 1
    n = (m * max(gap, b)) // c + 1
    return Construction(branch, n, m, m*b, m*a, n*c)


def sample_cases():
    yield "gap<smaller", tuple(map(Magnitude, (8, 5, 7)))
    yield "gap=smaller", tuple(map(Magnitude, (10, 5, 7)))
    yield "gap>smaller", tuple(map(Magnitude, (10, 3, 7)))


if __name__ == "__main__":
    for label, (a, b, c) in sample_cases():
        p = construct(a, b, c)
        print(label, f"(m,n)=({p.m},{p.n});",
              f"{p.small_multiple} < {p.shared_multiple} < {p.large_multiple};",
              witness_signs(a, c, b, c, p.m, p.n),
              witness_signs(c, b, c, a, p.n, p.m))
