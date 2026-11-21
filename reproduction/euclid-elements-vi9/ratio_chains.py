"""Exact analytic model of the parallel construction in Euclid VI.9."""
from dataclasses import dataclass
from fractions import Fraction as Q

Point = tuple[Q, Q]


def point(raw: tuple) -> Point:
    if not isinstance(raw, (tuple, list)) or len(raw) != 2:
        raise ValueError("expected two rational coordinates")
    if any(type(q) not in (int, Q) for q in raw):
        raise TypeError("coordinates must be int or Fraction")
    return Q(raw[0]), Q(raw[1])


def add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def sub(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def mul(k: Q, a: Point) -> Point:
    return k * a[0], k * a[1]


def det(a: Point, b: Point) -> Q:
    return a[0] * b[1] - a[1] * b[0]


@dataclass(frozen=True)
class Cut:
    marks: tuple[Point, ...]
    cut_point: Point
    segment_parameter: Q


def construct(a: tuple, b: tuple, step: tuple, n: int = 3, m: int = 1) -> Cut:
    """Put n equal steps on an auxiliary ray, then project mark m parallel to CB."""
    if type(m) is not int or type(n) is not int or not 0 < m < n:
        raise ValueError("integers must satisfy 0 < m < n")
    a, b, step = point(a), point(b), point(step)
    direction = sub(b, a)
    if det(direction, step) == 0:
        raise ValueError("need a nonzero base and a nonparallel auxiliary step")
    marks = tuple(add(a, mul(k, step)) for k in range(n + 1))
    d, c = marks[m], marks[n]
    direction_parallel = sub(b, c)
    # Require det(a + t*(b-a) - d, b-c) == 0; do not set t=m/n.
    t = det(sub(d, a), direction_parallel) / det(direction, direction_parallel)
    return Cut(marks, add(a, mul(t, direction)), t)


def certificate(a: tuple, b: tuple, c: tuple, d: tuple, f: tuple) -> tuple[Q, Q, Q]:
    """For interior marks, return determinant and the two remainder/part ratios."""
    a, b, c, d, f = (point(p) for p in (a, b, c, d, f))

    def parameter(p, end):
        whole = sub(end, a)
        if whole == (0, 0) or det(sub(p, a), whole) != 0:
            raise ValueError("point must be on a nonzero segment")
        axis = 0 if whole[0] else 1
        k = (p[axis] - a[axis]) / whole[axis]
        if not 0 < k < 1:
            raise ValueError("point must be strictly interior")
        return k

    if det(sub(b, a), sub(c, a)) == 0:
        raise ValueError("auxiliary triangle must be nondegenerate")
    td, tf = parameter(d, c), parameter(f, b)
    return det(sub(f, d), sub(b, c)), (1-td)/td, (1-tf)/tf
