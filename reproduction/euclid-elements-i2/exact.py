"""Exact arithmetic helpers adapted from this repository’s original I.1 teaching code."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json


def rational(value):
    """Accept exact rational scalars only; reject silently rounded inputs."""
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError('Use int or Fraction, not float, bool, or text')
    return F(value)


@dataclass(frozen=True)
class Q3:
    """The exact real number a + b sqrt(3), represented by rational coefficients."""
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', rational(self.a))
        object.__setattr__(self, 'b', rational(self.b))

    def __add__(self, other):
        if not isinstance(other, Q3):
            return NotImplemented
        return Q3(self.a + other.a, self.b + other.b)

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, other):
        if not isinstance(other, Q3):
            return NotImplemented
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, Q3):
            return NotImplemented
        return Q3(self.a * other.a + 3 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    def scale(self, scalar):
        scalar = rational(scalar)
        return Q3(self.a * scalar, self.b * scalar)

    def sign(self):
        """Exact sign, using rational squares only when summands oppose."""
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        delta = self.a * self.a - 3 * self.b * self.b
        # sqrt(3) irrational: delta is never zero for nonzero rational a,b.
        return ((delta > 0) - (delta < 0)) * ((self.a > 0) - (self.a < 0))

    def record(self):
        return {'rational': str(self.a), 'sqrt3_coefficient': str(self.b)}


def point(value):
    """Convert a two-coordinate exact rational endpoint."""
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise TypeError('Endpoint must contain two rational coordinates')
    return tuple(Q3(rational(x)) for x in value)


def require_point(value):
    if not isinstance(value, (list, tuple)) or len(value) != 2 or not all(isinstance(x, Q3) for x in value):
        raise TypeError('Certificate point must contain two Q3 coordinates')
    return tuple(value)


def distance2(p, q):
    p, q = require_point(p), require_point(q)
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def orientation(a, b, c):
    a, b, c = map(require_point, (a, b, c))
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

