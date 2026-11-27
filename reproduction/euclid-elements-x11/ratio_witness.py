"""X.11 teaching model with positive lengths represented by squared ratios."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


@dataclass(frozen=True)
class Witness:
    squared_ratio: Fraction
    counts: tuple[int, int] | None
    left_measure: Fraction | None
    right_measure: Fraction | None


def transfer(q1, q2, b=1, d=1):
    """Given q1=(A/B)^2 and q2=(C/D)^2, and exact B=b, D=d.

    Ratios must be equal. When the shared ratio is m:n in lowest terms,
    return shared counts and separately scaled pair-local measures.
    """
    for x in (q1, q2, b, d):
        if type(x) not in (int, Fraction) or x <= 0:
            raise ValueError("all inputs must be positive ints or Fractions")
    q1, q2, b, d = map(Fraction, (q1, q2, b, d))
    if q1 != q2:
        raise ValueError("the ordered ratios are not equal")
    p, q = q1.numerator, q1.denominator
    m, n = isqrt(p), isqrt(q)
    if m*m != p or n*n != q:
        return Witness(q1, None, None, None)
    return Witness(q1, (m,n), b/n, d/n)
