"""Exact arithmetic model for Euclid X.8, using positive rational square ratios."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


@dataclass(frozen=True)
class Certificate:
    squared_ratio: Fraction
    floors: tuple[int, int]
    ratio: Fraction | None
    a: Fraction | None


def _positive(value):
    if type(value) not in (int, Fraction) or value <= 0:
        raise ValueError("expected a positive int or Fraction")
    return Fraction(value)


def classify(q, b=1):
    """For q=(A/B)^2 and positive rational B, certify A/B and A if rational.

    Otherwise floors bound the roots of the reduced numerator and denominator;
    each nonsquare t has floor r with r² < t < (r+1)².
    """
    q, b = _positive(q), _positive(b)
    p, d = q.numerator, q.denominator
    u, v = isqrt(p), isqrt(d)
    ratio = Fraction(u, v) if u*u == p and v*v == d else None
    return Certificate(q, (u, v), ratio, None if ratio is None else b*ratio)
