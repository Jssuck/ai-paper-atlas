"""Euclid III.30: choose a specified arc, then intersect the right bisector ray."""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import atan2, hypot, tau


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]


def cross(u, v):
    return u[0]*v[1]-u[1]*v[0]


def square(u):
    return dot(u, u)


def polar_sweep(a, b, o, direction):
    """Approximate directed sweep, measured from actual endpoints."""
    u, v = sub(a, o), sub(b, o)
    return (direction*(atan2(v[1], v[0])-atan2(u[1], u[0]))) % tau


@dataclass(frozen=True)
class SelectedArc:
    center: tuple
    a: tuple
    b: tuple
    direction: int  # +1 counterclockwise, -1 clockwise, from a to b

    def __post_init__(self):
        for p in (self.center, self.a, self.b):
            if not isinstance(p, tuple) or len(p) != 2:
                raise ValueError("points must be coordinate pairs")
            if not all(isinstance(x, (int, Q)) and not isinstance(x, bool) for x in p):
                raise TypeError("point coordinates must be integers or fractions")
        if type(self.direction) is not int or self.direction not in (-1, 1):
            raise ValueError("direction must be +1 or -1")
        if self.a == self.b:
            raise ValueError("distinct endpoints are required")
        if square(sub(self.a, self.center)) != square(sub(self.b, self.center)):
            raise ValueError("endpoints must be on the same centered circle")

    def chord_midpoint(self):
        return tuple((Q(x)+y)/2 for x, y in zip(self.a, self.b))

    def _ray_intersection(self, direction):
        # A directed CCW arc lies on the right of the chord A to B.
        x, y = sub(self.b, self.a)
        normal = (direction*y, -direction*x)
        radius = hypot(*sub(self.a, self.center))
        width = hypot(x, y)
        return tuple(float(o)+radius*(float(n)/width)
                     for o, n in zip(self.center, normal))

    def endpoints_on_bisector(self):
        """Approximate circle intersections: selected ray first; opposite second."""
        return self._ray_intersection(self.direction), self._ray_intersection(-self.direction)

    def full_sweep(self):
        return polar_sweep(self.a, self.b, self.center, self.direction)

    def parts(self, point):
        return (polar_sweep(self.a, point, self.center, self.direction),
                polar_sweep(point, self.b, self.center, self.direction))


def _unit(t):
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def _rotate(u, v):
    return (u[0]*v[0]-u[1]*v[1], u[0]*v[1]+u[1]*v[0])


def grid():
    """Return arcs and independent known midpoint directions from construction."""
    o = (Q(3, 7), Q(-2, 5))
    for r in (Q(1, 3), Q(5, 3), Q(7)):
        for t in (Q(i, 9) for i in range(1, 19)):
            for axis in (_unit(Q(i, 4)) for i in range(-6, 7)):
                def place(v):
                    return tuple(x+r*y for x, y in zip(o, v))
                a = place(_rotate(axis, _unit(-t)))
                b = place(_rotate(axis, _unit(t)))
                for swap in (-1, 1):
                    u, v = (a, b) if swap == 1 else (b, a)
                    for direction in (-1, 1):
                        sign = swap*direction
                        yield SelectedArc(o, u, v, direction), place(tuple(sign*z for z in axis))
