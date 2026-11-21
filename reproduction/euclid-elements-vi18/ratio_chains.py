"""Exact modern teaching model for ordered direct similarities in VI.18."""
from fractions import Fraction as Q

Point = tuple[Q, Q]


def point(p) -> Point:
    x, y = p
    if any(type(q) not in (int, Q) for q in (x, y)):
        raise TypeError("coordinates must be int or Fraction")
    return Q(x), Q(y)


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def scale(t, u):
    return t * u[0], t * u[1]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def direct_similarity(c, d, a, b):
    """Return the orientation-preserving map c→a, d→b."""
    c, d, a, b = map(point, (c, d, a, b))
    u, v = sub(d, c), sub(b, a)
    n = dot(u, u)
    if not n or not dot(v, v):
        raise ValueError("source and target bases must be nonzero")
    alpha, beta = dot(u, v) / n, det(u, v) / n

    def transform(p):
        x, y = sub(point(p), c)
        return add(a, (alpha * x - beta * y, beta * x + alpha * y))

    return transform


def _angle_direction(old_base, new_base, old_ray):
    """Transfer an oriented angle using an unnormalized local direction."""
    along = dot(old_base, old_ray)
    across = det(old_base, old_ray)
    x, y = new_base
    return along * x - across * y, along * y + across * x


def copy_triangle(p, q, r, a, b):
    """Copy vertex r by intersecting two angle rays, with p→a and q→b."""
    p, q, r, a, b = map(point, (p, q, r, a, b))
    pq, ab = sub(q, p), sub(b, a)
    if not dot(ab, ab) or not det(pq, sub(r, p)):
        raise ValueError("triangle and target baseline must be nondegenerate")
    ra = _angle_direction(pq, ab, sub(r, p))
    rb = _angle_direction(sub(p, q), sub(a, b), sub(r, q))
    den = det(ra, rb)
    if not den:
        raise ValueError("parallel angle rays")
    t, s = det(ab, rb) / den, det(ab, ra) / den
    if t <= 0 or s <= 0:
        raise ValueError("intersection must lie on both forward rays")
    return add(a, scale(t, ra))


def reconstruct(c, d, f, e, a, b):
    """Copy CDF then DFE across the shared DF→BG diagonal."""
    g = copy_triangle(c, d, f, a, b)
    h = copy_triangle(d, f, e, b, g)
    return g, h
