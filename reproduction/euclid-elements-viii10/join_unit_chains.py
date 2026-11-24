"""Exact arithmetic teaching model of Euclid VIII.10."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Trace:
    mixed: tuple[int, ...]
    growth: Fraction
    endpoint_measure: int


def join(left, right, *, modern=False):
    left,right = tuple(left),tuple(right)
    if len(left) != len(right) or len(left)<3:
        raise ValueError("need equal lengths and at least one mean")
    if any(type(x) is not int or x < 1 for x in left+right):
        raise ValueError("expected positive integer terms")
    if left[0] != 1 or right[0] != 1:
        raise ValueError("both chains must start at the unit")
    a,b = left[1],right[1]
    if not modern and (min(a,b) < 2 or a == b):
        raise ValueError("unit bases or equal endpoints need modern=True")
    if any(y != x*s for row,s in ((left,a),(right,b)) for x,y in zip(row,row[1:])):
        raise ValueError("each unit chain must have a constant ratio")
    # Take one factor from each opposite position so exponents add to n.
    row = tuple(x*y for x,y in zip(reversed(left),right))
    return Trace(row,Fraction(b,a),gcd(left[-1],right[-1]))


if __name__ == "__main__":
    print(join((1,4,16,64),(1,6,36,216)))
