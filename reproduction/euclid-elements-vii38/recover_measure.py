"""Exact teaching reconstruction of Euclid VII.38."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Trace:
    part_cuts: tuple[int, ...]
    transferred_cuts: tuple[int, ...]
    unit_count: int
    transferred_count: int


def recover(a, b, c, *, modern=False):
    """B is the named C-th part of A; recover C's measure count in A."""
    minimum = 1 if modern else 2
    if any(type(x) is not int or x < minimum for x in (a,b,c)):
        raise ValueError("positive integers are required, nonunits by default")
    parts = [0]
    for _ in range(c):
        parts.append(parts[-1]+b)
    if parts[-1] != a:
        raise ValueError("B must be precisely the C-th part of A")
    units = len(range(b))
    # VII.15: transfer from B-sized groups counted by units in C to
    # C-sized groups counted by units in B.
    alternate = [0]
    for _ in range(units):
        alternate.append(alternate[-1]+c)
    if alternate[-1] != a:
        raise ArithmeticError("measure transfer failed")
    return Trace(tuple(parts),tuple(alternate),units,len(alternate)-1)


if __name__ == "__main__":
    print(recover(12,4,3))
