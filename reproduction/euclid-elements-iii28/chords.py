"""Euclid III.28 classroom model: exact endpoint geometry, approximate arcs."""
from dataclasses import dataclass
from fractions import Fraction
from math import atan2, fsum, hypot, pi, tau


def point(x, y):
    return (Fraction(x), Fraction(y))


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def square(a):
    return dot(a, a)


def unit(t):
    """Rational point on the unit circle; t is a rational parameter."""
    t = Fraction(t)
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def place(origin, r, u):
    return (origin[0] + r*u[0], origin[1] + r*u[1])


def rotate(u, v):
    return (u[0]*v[0]-u[1]*v[1], u[0]*v[1]+u[1]*v[0])


@dataclass(frozen=True)
class Chord:
    origin: tuple
    a: tuple
    b: tuple

    def __post_init__(self):
        for p in (self.origin, self.a, self.b):
            if not (isinstance(p, tuple) and len(p) == 2 and
                    all(isinstance(x, (int, Fraction)) and not isinstance(x, bool) for x in p)):
                raise TypeError("coordinates must be exact integers or fractions")
        if self.a == self.b:
            raise ValueError("the two endpoints must be distinct")
        if square(sub(self.a, self.origin)) != square(sub(self.b, self.origin)):
            raise ValueError("endpoint distances from the center differ")

    @property
    def r2(self):
        return square(sub(self.a, self.origin))

    @property
    def c2(self):
        return square(sub(self.a, self.b))

    @property
    def diameter(self):
        return self.c2 == 4*self.r2

    def endpoint_sweeps(self):
        """Signed endpoint-to-endpoint short and long paths; tie is arbitrary."""
        u, v = sub(self.a, self.origin), sub(self.b, self.origin)
        if self.diameter:
            return pi, -pi
        forward = (atan2(float(v[1]), float(v[0])) -
                   atan2(float(u[1]), float(u[0]))) % tau
        backward = forward-tau
        return (forward, backward) if forward < -backward else (backward, forward)

    def endpoint_arcs(self):
        """Short/long sweeps from endpoint polar angles, radians; ties explicit."""
        short, long = self.endpoint_sweeps()
        return abs(short), abs(long)

    def cos_signature(self):
        """Exact cosine of the principal central angle; does not calculate arcs."""
        return Fraction(dot(sub(self.a, self.origin), sub(self.b, self.origin)),
                        self.r2)

    def midpoint_d2(self):
        mid = ((Fraction(self.a[0])+self.b[0])/2,
               (Fraction(self.a[1])+self.b[1])/2)
        return square(sub(mid, self.origin))


def pair_family():
    """Different translations/orientations, with independent raw endpoint paths."""
    a0, b0 = point(3, -6), point(-8, 11)
    rotations = [unit(Fraction(i, 4)) for i in range(-6, 7)]
    for r in (1, 2, 5):
        for i in range(1, 21):
            endpoint = unit(Fraction(i, 7))
            for direction in rotations:
                for orientation in (-1, 1):
                    v = (endpoint[0], orientation*endpoint[1])
                    a = Chord(a0, place(a0, r, (1, 0)), place(a0, r, endpoint))
                    b = Chord(b0, place(b0, r, rotate(direction, v)), place(b0, r, direction))
                    yield a, b


def unequal_radius_pair():
    # Both have half-chord 12. The perpendicular offsets are 5 and 9.
    o = point(0, 0)
    return Chord(o, point(5, 12), point(5, -12)), Chord(o, point(9, 12), point(9, -12))


def polyline_arc_estimate(chord, sweep, pieces):
    """Approximate corresponding arc length as a regular inscribed polygonal chain."""
    from math import cos, sin
    u = sub(chord.a, chord.origin)
    start = atan2(float(u[1]), float(u[0]))
    radius = hypot(*map(float, u))
    vertices = [(radius*cos(start+sweep*i/pieces), radius*sin(start+sweep*i/pieces))
                for i in range(pieces+1)]
    return fsum(hypot(b[0]-a[0], b[1]-a[1]) for a, b in zip(vertices, vertices[1:]))
