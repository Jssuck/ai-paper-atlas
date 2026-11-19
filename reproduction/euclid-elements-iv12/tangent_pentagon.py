"""Exact teaching model of Euclid IV.12; standard library only."""
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


def tangent_intersection(p, r):
    """Intersect the lines p·x=p·p and r·x=r·r."""
    det = cross(p, r)
    if not det.sign():
        raise ValueError("coincident or parallel tangent lines")
    pp, rr = dot(p, p), dot(r, r)
    return ((pp*r[1]-rr*p[1])/det, (p[0]*rr-r[0]*pp)/(V*det))


def envelope(contacts):
    """Return the corners following each contact in the supplied order."""
    if len(contacts) != 5 or len(set(contacts)) != 5:
        raise ValueError("expected five distinct contacts")
    r2 = dot(contacts[0], contacts[0])
    if r2.sign() <= 0 or any(dot(p, p) != r2 for p in contacts):
        raise ValueError("contacts must belong to one positive origin circle")
    return tuple(tangent_intersection(p, contacts[(i+1) % 5])
                 for i, p in enumerate(contacts))


def envelope_checks(contacts):
    vertices = envelope(contacts)
    r2 = dot(contacts[0], contacts[0])
    edges = [(vertices[i-1], v) for i,v in enumerate(vertices)]
    support, on_segment, inside = [], [], []
    for p, (a,b) in zip(contacts, edges):
        support.append(dot(p,a) == dot(p,b) == r2)
        # Under the support test p is collinear with the two end vertices.
        on_segment.append(dot(sub(p,a), sub(p,b)).sign() < 0)
        inside.append(all((r2-dot(p,v)).sign() >= 0 for v in vertices))
    squared = [dot(sub(a,b), sub(a,b)) for a,b in edges]
    angles = [angle_key(vertices[i-1], v, vertices[(i+1) % 5])
              for i,v in enumerate(vertices)]
    turns = [orient(vertices[i-1], v, vertices[(i+1) % 5])
             for i,v in enumerate(vertices)]
    crossings = sum(proper_crossing(a,b,c,d)
                    for i,(a,b) in enumerate(edges) for c,d in edges[i+1:]
                    if len({a,b,c,d}) == 4)
    convex = (len(set(vertices)) == 5 and len(set(turns)) == 1
              and turns[0] != 0 and crossings == 0 and all(inside))
    return {
        "tangent_lines": all(support),
        "contacts_on_side_segments": all(on_segment),
        "inside_all_tangent_halfplanes": all(inside),
        "strict_crossings": crossings,
        "convex_envelope": convex,
        "equal_sides": len(set(squared)) == 1,
        "equal_ordinary_angles": len(set(angles)) == 1,
        "angles_108": all(key == (-1,U*U) for key in angles),
        "side_square_formula": all(n == 4*r2*(1-U)/(1+U) for n in squared),
        "center_distances_formula": all(dot(v,v) == 2*r2/(1+U) for v in vertices),
    }


def wrong_order(contacts):
    return tuple(contacts[i] for i in (0,2,4,1,3))


def irregular_contacts(radius, branch):
    a, _, c, d, e = construct(radius, branch)
    # Rational parametrization of x²+V y²=R², with parameter 1/2.
    w = V * F(1,4)
    return a, (radius*(1-w)/(1+w), q(branch*radius)/(1+w)), c, d, e


def check_grid():
    good = stars = uneven = 0
    for n in range(1,13):
        for den in (13,17,19,23):
            for branch in (-1,1):
                radius = F(n,den)
                p = construct(radius, branch)
                a = envelope_checks(p)
                if a["strict_crossings"] != 0 or not all(v for k,v in a.items() if k != "strict_crossings"):
                    raise AssertionError(a)
                good += 1
                b = envelope_checks(wrong_order(p))
                if not (b["strict_crossings"] == 5 and not b["convex_envelope"]
                        and not b["inside_all_tangent_halfplanes"] and b["tangent_lines"]
                        and b["contacts_on_side_segments"] and b["equal_sides"]
                        and b["equal_ordinary_angles"] and not b["angles_108"]):
                    raise AssertionError(b)
                stars += 1
                c = envelope_checks(irregular_contacts(radius,branch))
                if not (c["strict_crossings"] == 0 and c["convex_envelope"]
                        and c["tangent_lines"] and c["contacts_on_side_segments"]
                        and not c["equal_sides"] and not c["equal_ordinary_angles"]):
                    raise AssertionError(c)
                uneven += 1
    return good, stars, uneven


if __name__ == "__main__":
    good, stars, uneven = check_grid()
    print(f"Exact regular envelopes: {good}; star-order controls: {stars}; irregular-contact controls: {uneven}")
