"""Exact teaching model of Euclid IV.11; standard library only."""
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Q5:
    """a+b√5, with rational coefficients."""
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        if not all(isinstance(x, (int, F)) for x in (self.a, self.b)):
            raise TypeError("expected exact rational coefficients")
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    def __add__(self, other):
        other = q(other)
        return Q5(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-q(other))

    def __rsub__(self, other):
        return q(other) + (-self)

    def __mul__(self, other):
        other = q(other)
        return Q5(self.a * other.a + 5 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = q(other)
        norm = other.a * other.a - 5 * other.b * other.b
        return self * Q5(other.a / norm, -other.b / norm)

    def sign(self):
        # If signs differ compare |a|² with |b√5|², then use sign(a).
        sa = (self.a > 0) - (self.a < 0)
        sb = (self.b > 0) - (self.b < 0)
        if not sa or not sb or sa == sb:
            return sa or sb
        d = self.a * self.a - 5 * self.b * self.b
        return sa * ((d > 0) - (d < 0))


def q(x):
    return x if isinstance(x, Q5) else Q5(x)


# x-coordinate is literal; y-coordinate is the coefficient of sqrt(V).
U = Q5(F(-1, 4), F(1, 4))  # cos(72 degrees)
V = 1 - U * U
COS36 = Q5(F(1, 4), F(1, 4))


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0] * b[0] + V * a[1] * b[1]


def cross(a, b):
    # Positive sqrt(V) does not affect sign.
    return a[0] * b[1] - a[1] * b[0]


def angle_key(a, b, c):
    """Ordinary angle ABC, identified by sign(cos) and cos squared."""
    p, r = sub(a, b), sub(c, b)
    norm = dot(p, p) * dot(r, r)
    if not norm.sign():
        raise ValueError("zero ray")
    prod = dot(p, r)
    return prod.sign(), prod * prod / norm


def rotate(p, branch):
    x, y = p
    return U * x - branch * V * y, branch * x + U * y


def construct(radius=1, branch=1):
    """A,B,C,D,E in boundary order, starting at (radius, 0)."""
    if isinstance(radius, bool) or not isinstance(radius, (int, F)) or radius <= 0:
        raise ValueError("radius must be a positive rational")
    if type(branch) is not int or branch not in (-1, 1):
        raise ValueError("orientation must be +1 or -1")
    points = [(q(radius), q(0))]
    for _ in range(4):
        points.append(rotate(points[-1], branch))
    if rotate(points[-1], branch) != points[0]:
        raise ArithmeticError("rotation orbit does not close")
    return tuple(points)


def orient(a, b, p):
    return cross(sub(b, a), sub(p, a)).sign()


def proper_crossing(a, b, c, d):
    return (orient(a, b, c) * orient(a, b, d) < 0
            and orient(c, d, a) * orient(c, d, b) < 0)


def polygon_checks(points):
    """Five distinct points on a positive circle centered at the origin.

    Use actual winding and strict intersections independent of input order.
    Distinct points on this circle prevent collinear overlaps of chords
    that do not share an endpoint.
    """
    if len(points) != 5 or len(set(points)) != 5:
        raise ValueError("expected five distinct points")
    r2 = dot(points[0], points[0])
    if r2.sign() <= 0 or any(dot(p, p) != r2 for p in points):
        raise ValueError("points must be on one positive-radius origin circle")
    edges = [(p, points[(i + 1) % 5]) for i, p in enumerate(points)]
    sides = [dot(sub(a, b), sub(a, b)) for a, b in edges]
    angles = [angle_key(points[i - 1], p, points[(i + 1) % 5])
              for i, p in enumerate(points)]
    winding, crossings = 0, 0
    for i, (a, b) in enumerate(edges):
        turn = cross(a, b).sign()
        # Half-open positive-x ray crossing test, counting signed crossings.
        if not turn and dot(a, b).sign() < 0:
            raise ValueError("center on a chord; winding undefined")
        if a[1].sign() <= 0 < b[1].sign() and turn > 0:
            winding += 1
        if b[1].sign() <= 0 < a[1].sign() and turn < 0:
            winding -= 1
        for c, d in edges[i + 1:]:
            if len({a, b, c, d}) == 4 and proper_crossing(a, b, c, d):
                crossings += 1
    return {
        "same_circle": True,
        "equal_chords": len(set(sides)) == 1,
        "equal_ordinary_angles": len(set(angles)) == 1,
        "ordinary_angles_108": all(k == (-1, U * U) for k in angles),
        "strict_crossings": crossings,
        "winding": winding,
        "regular_convex_boundary": (len(set(sides)) == 1 and len(set(angles)) == 1
                                    and crossings == 0 and abs(winding) == 1),
    }


def source_checks(points):
    """Check IV.11's triangle ACD and the intended internal CE/DB rays."""
    A, B, C, D, E = points
    apex = angle_key(D, A, C)
    bases = (angle_key(A, C, D), angle_key(C, D, A))
    halves = (angle_key(A, C, E), angle_key(E, C, D),
              angle_key(C, D, B), angle_key(B, D, A))
    # Each bisecting ray endpoint must be strictly inside its base-angle
    # wedge: E lies on D's side of AC and A's side
    # of CD. Likewise B lies on A's side of CD and C's side of DA.
    ce_inside = (orient(C, A, E) == orient(C, A, D) != 0
                 and orient(C, D, E) == orient(C, D, A) != 0)
    db_inside = (orient(D, C, B) == orient(D, C, A) != 0
                 and orient(D, A, B) == orient(D, A, C) != 0)
    return {
        "apex_36": apex == (1, COS36 * COS36),
        "both_bases_72": all(k == (1, U * U) for k in bases),
        "interior_bisectors_CE_DB": ce_inside and db_inside,
        "five_equal_inscribed_angles": all(k == apex for k in halves),
    }


def star(points):
    return tuple(points[i] for i in (0, 2, 4, 1, 3))


def check_grid():
    positive = controls = 0
    for n in range(1, 13):
        for d in (13, 17, 19, 23):
            for branch in (-1, 1):
                points = construct(F(n, d), branch)
                boundary = polygon_checks(points)
                if (not all(source_checks(points).values())
                    or not boundary["regular_convex_boundary"]
                    or not boundary["ordinary_angles_108"]
                    or boundary["winding"] != branch):
                    raise AssertionError(boundary)
                positive += 1
                failure = polygon_checks(star(points))
                if (not failure["equal_chords"] or not failure["equal_ordinary_angles"]
                    or failure["ordinary_angles_108"] or failure["regular_convex_boundary"]
                    or failure["strict_crossings"] != 5 or failure["winding"] != 2 * branch):
                    raise AssertionError(failure)
                controls += 1
    return positive, controls


if __name__ == "__main__":
    positive, controls = check_grid()
    print(f"Exact convex boundary certificates: {positive}; star controls: {controls}")
