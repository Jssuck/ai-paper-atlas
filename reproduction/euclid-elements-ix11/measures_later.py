"""Exact quotient certificate for Euclid IX.11."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Measurement:
    earlier: int
    later: int
    count: int
    neighbor_count: int


def measure_later(q, i, j):
    """Measure term j by term i; indices are exponents and 0 is unity."""
    if any(type(n) is not int for n in (q,i,j)) or not (q>=2 and 1<=i<j):
        raise ValueError("expected integers q>=2 and 1<=i<j")
    earlier = value = 1
    for step in range(1,j+1):
        value *= q
        if step == i:
            earlier = value
    later = value
    count, rem = divmod(later,earlier)
    neighbor_count, adjacent_rem = divmod(earlier*q,earlier)
    if rem or adjacent_rem or count != neighbor_count**(j-i):
        raise ArithmeticError("iterated measurement invariant failed")
    return Measurement(earlier,later,count,neighbor_count)
