"""Exact circle-angle classifications and a separate modern secant-limit demo."""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import atan2, pi


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def square(a):
    return dot(a, a)


def classify(value):
    return "acute" if value > 0 else "obtuse" if value < 0 else "right"


def angle(u, v):
    return atan2(abs(cross(u, v)), dot(u, v))


def unit(t):
    return (Q(1-t*t, 1+t*t), Q(2*t, 1+t*t))


@dataclass(frozen=True)
class Segment:
    center: tuple
    a: tuple
    b: tuple
    p: tuple  # boundary vertex identifying the selected arc, not a disk interior point

    def __post_init__(self):
        for point in (self.center, self.a, self.b, self.p):
            if not isinstance(point, tuple) or len(point) != 2:
                raise ValueError("each point must be a coordinate pair")
            if not all(type(x) in (int, Q) for x in point):
                raise TypeError("integer or Fraction coordinates required")
        if len({self.a, self.b, self.p}) != 3:
            raise ValueError("three distinct boundary points required")
        radii = {square(sub(x, self.center)) for x in (self.a, self.b, self.p)}
        if len(radii) != 1:
            raise ValueError("the boundary points must lie on the same circle")

    def chord_side(self, point):
        return cross(sub(self.b, self.a), sub(point, self.a))

    def kind(self):
        side = self.chord_side(self.center)*self.chord_side(self.p)
        return "major" if side > 0 else "minor" if side < 0 else "half"

    def inscribed_sign_value(self):
        return dot(sub(self.a, self.p), sub(self.b, self.p))

    def inscribed_angle(self):
        return angle(sub(self.a, self.p), sub(self.b, self.p))

    def toward_arc_tangent(self):
        x, y = sub(self.a, self.center)
        direction = 1 if self.chord_side(self.p) < 0 else -1
        return (-direction*y, direction*x)

    def sample_toward_endpoint(self, divisions):
        """Rational circle point at angular displacement 2 atan(1/divisions) from A."""
        if type(divisions) is not int or divisions <= 0:
            raise ValueError("positive integer divisions required")
        t = Q(1, divisions)
        c, s = unit(t)
        x, y = sub(self.a, self.center)
        tx, ty = self.toward_arc_tangent()
        return (self.center[0]+c*x+s*tx, self.center[1]+c*y+s*ty)

    def modern_limit_angle(self):
        return angle(sub(self.b, self.a), self.toward_arc_tangent())

    def secant_angle_at_a(self, sample):
        return angle(sub(self.b, self.a), sub(sample, self.a))


def examples():
    o = (0, 0)
    yield Segment(o, (3, -4), (3, 4), (-5, 0))
    yield Segment(o, (3, -4), (3, 4), (5, 0))
    yield Segment(o, (5, 0), (-5, 0), (3, 4))


def rational_grid():
    """Distinct ordered endpoint triples on three rationally parametrized circles."""
    center = (Q(7, 3), Q(-9, 4))
    samples = tuple(unit(Q(i, 4)) for i in range(-8, 9)) + ((-1, 0),)
    for r in (Q(1, 3), Q(5, 2), Q(7)):
        pts = tuple(tuple(x+r*y for x, y in zip(center, u)) for u in samples)
        for a in pts:
            for b in pts:
                if a == b:
                    continue
                for p in pts:
                    if p != a and p != b:
                        yield Segment(center, a, b, p)
