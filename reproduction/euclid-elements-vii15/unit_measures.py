"""Euclid VII.15 as an exact reblocking of adjacent unit intervals."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Trace:
    x: int
    y: int
    z: int
    unit_to_x_count: int
    y_to_z_cuts: tuple[int, ...]
    unit_to_y_count: int
    x_to_z_cuts: tuple[int, ...]


def measure(x, y, z, *, modern=False):
    floor = 1 if modern else 2
    if any(type(t) is not int or t < floor for t in (x,y,z)):
        raise ValueError("expected positive integers (nonunits unless modern=True)")
    count, residue = divmod(z, y)
    if residue or count != x:
        raise ValueError("Y must measure Z as many times as the unit measures X")
    y_cuts = tuple(range(0, z+1, y))
    # Reblock the same line into X-sized intervals, one per unit in Y.
    x_cuts = [0]
    for _ in range(y):
        x_cuts.append(x_cuts[-1]+x)
    if x_cuts[-1] != z:
        raise ArithmeticError("grouping did not end at Z")
    return Trace(x,y,z,x,y_cuts,y,tuple(x_cuts))


if __name__ == "__main__":
    print(measure(3,4,12))
