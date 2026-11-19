"""Exact teaching model of Euclid IV.13; standard library only."""
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


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def scale(a, k):
    return (a[0] * k, a[1] * k)


def norm(a):
    return dot(a, a)


def edges(points):
    return tuple(zip(points, points[1:] + points[:1]))


def boundary_sign(points):
    if len(points) != 5 or len(set(points)) != 5:
        raise ValueError("expected five distinct vertices")
    signs = {cross(sub(b, a), sub(c, a)).sign()
             for a, b in edges(points) for c in points if c not in (a, b)}
    if signs not in ({1}, {-1}):
        raise ValueError("expected a strictly convex boundary order")
    return signs.pop()


def source_bisector(left, apex, right):
    """Sum equal-length incident side vectors (the internal branch)."""
    x, y = sub(left, apex), sub(right, apex)
    if norm(x) != norm(y) or not cross(x,y).sign():
        raise ValueError("fixture does not admit the equal-length bisector")
    return add(x, y)


def center_from_bisectors(points):
    """Intersect the actual internal rays at C and D."""
    side = boundary_sign(points)
    _, b, c, d, e = points
    u = source_bisector(b, c, d)
    v = source_bisector(c, d, e)
    det = cross(u, v)
    if not det.sign():
        raise ValueError("parallel candidate bisectors")
    dc = sub(d, c)
    t = cross(dc, v) / det
    w = cross(dc, u) / det
    if t.sign() <= 0 or w.sign() <= 0:
        raise ValueError("intersection is not on both internal rays")
    center = add(c, scale(u, t))
    if any(side * cross(sub(y, x), sub(center, x)).sign() <= 0
           for x, y in edges(points)):
        raise ValueError("center candidate is not strictly inside")
    return center


def inspect_center(points, center):
    """Audit the global signed half-planes and all five perpendicular feet."""
    side = boundary_sign(points)
    interior, positions, orthogonal, distances = [], [], [], []
    for a, b in edges(points):
        e, w = sub(b, a), sub(center, a)
        t = dot(e, w) / norm(e)
        foot = add(a, scale(e, t))
        delta = sub(center, foot)
        interior.append(side * cross(e, w).sign() > 0)
        positions.append(t)
        orthogonal.append(not dot(e, delta).sign())
        distances.append(norm(delta))
    return {
        "inside_every_halfplane": all(interior),
        "feet_strictly_inside_sides": all(t.sign() > 0 and (1-t).sign() > 0 for t in positions),
        "perpendicular_feet": all(orthogonal),
        "all_feet_midpoints": all(t == q(F(1,2)) for t in positions),
        "equal_positive_distance_squares": len(set(distances)) == 1 and distances[0].sign() > 0,
        "distance_squares": tuple(distances),
    }


def fixtures(radius, branch):
    # Vary translations as well as scale and mirror. The center is not passed
    # to the construction, only retained as an independent fixture oracle.
    pts = construct(radius, branch)
    origin = (q(radius*F(7,3)), q(-radius*F(5,7)))
    regular = tuple(add(p, origin) for p in pts)
    irregular = (add(origin, scale(pts[0], F(11,10))), *regular[1:])
    shifted = add(origin, (q(radius*F(1,20)), q(0)))
    return origin, regular, irregular, shifted


def check_grid():
    good = uneven = misplaced = 0
    for n in range(1,13):
        for den in (13,17,19,23):
            for branch in (-1,1):
                radius = F(n, den)
                oracle, p, irregular, shifted = fixtures(radius, branch)
                actual = center_from_bisectors(p)
                a = inspect_center(p, actual)
                target = radius * radius * COS36 * COS36
                if actual != oracle or not all(a[k] for k in a if k != "distance_squares") or set(a["distance_squares"]) != {target}:
                    raise AssertionError(a)
                good += 1
                if center_from_bisectors(irregular) != oracle:
                    raise AssertionError("perturbation unexpectedly moved the bisectors")
                for polygon, candidate in ((irregular, oracle), (p, shifted)):
                    b = inspect_center(polygon, candidate)
                    if not (b["inside_every_halfplane"] and b["feet_strictly_inside_sides"]
                            and b["perpendicular_feet"] and not b["equal_positive_distance_squares"]):
                        raise AssertionError(b)
                uneven += 1
                misplaced += 1
    return good, uneven, misplaced


if __name__ == "__main__":
    good, uneven, misplaced = check_grid()
    print(f"Exact regular incircles: {good}; perturbed polygons: {uneven}; shifted-center controls: {misplaced}")
