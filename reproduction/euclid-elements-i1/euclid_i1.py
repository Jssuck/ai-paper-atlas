"""Exact teaching reconstruction of Elements I.1, not a formalization of Euclid."""
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


def construct(a, b):
    """Return both exact equilateral vertices above/below the directed base."""
    a, b = point(a), point(b)
    if a == b:
        raise ValueError('Distinct endpoints are required')
    dx, dy = b[0].a - a[0].a, b[1].a - a[1].a
    mx, my = (a[0].a + b[0].a) / 2, (a[1].a + b[1].a) / 2
    return ((Q3(mx, -dy / 2), Q3(my, dx / 2)),
            (Q3(mx, dy / 2), Q3(my, -dx / 2)))


def certificate(a, b, c):
    """Check a proposed vertex independently of the construction formula."""
    a, b, c = point(a), point(b), require_point(c)
    ab, ac, bc = distance2(a, b), distance2(a, c), distance2(b, c)
    turn = orientation(a, b, c)
    return {'distinct_base': a != b,
            'first_circle': ac == ab,
            'second_circle': bc == ab,
            'noncollinear': turn.sign() != 0,
            'accepted': a != b and ac == ab and bc == ab and turn.sign() != 0,
            'side_squared': ab.record(), 'orientation': turn.record()}


def enumerate_grid():
    points = list(product(range(-2, 3), repeat=2))
    pairs = triangles = violations = 0
    for a in points:
        for b in points:
            if a == b:
                continue
            pairs += 1
            for index, c in enumerate(construct(a, b)):
                triangles += 1
                proof = certificate(a, b, c)
                expected_sign = 1 if index == 0 else -1
                if not proof['accepted'] or orientation(point(a), point(b), c).sign() != expected_sign:
                    violations += 1
    return {'integer_grid_points': len(points), 'ordered_distinct_bases': pairs,
            'triangles_checked': triangles, 'violations': violations}


def examples():
    a, b = (0, 0), (1, 0)
    vertices = construct(a, b)
    return {'unit_base_vertices': [[v.record() for v in p] for p in vertices],
            'unit_base_certificates': [certificate(a, b, c) for c in vertices],
            'single_circle_counterexample': certificate(a, b, point((0, 1))),
            'off_circle_counterexample': certificate(a, b, point((0, 2))),
            'degenerate_certificate': certificate(a, a, point(a)),
            'rational_plane_obligation': {'x': '1/2', 'y_squared': '3/4',
                'reason': 'Subtracting the two circle equations fixes x; no rational y squares to 3/4. See article proof, not a finite search claim.'}}


if __name__ == '__main__':
    print(json.dumps({'enumeration': enumerate_grid(), 'examples': examples()}, ensure_ascii=False, indent=2))
