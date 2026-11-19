"""Exact coordinate reconstruction of Euclid IV.7 (teaching code)."""
from fractions import Fraction as F
from itertools import product


def point(value):
    x, y = value
    if type(x) not in (int, F) or type(y) not in (int, F):
        raise TypeError("coordinates must be int or Fraction")
    return F(x), F(y)


def add(a, b): return a[0] + b[0], a[1] + b[1]
def sub(a, b): return a[0] - b[0], a[1] - b[1]
def mul(k, a): return k * a[0], k * a[1]
def turn(a): return -a[1], a[0]
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def det(a, b): return a[0] * b[1] - a[1] * b[0]


def intersection(a, b, q):
    """Solve a·z=b·z=q by Cramer's rule; z is relative to center."""
    d = det(a, b)
    if not d:
        raise ValueError("distinct, nonparallel supporting normals required")
    return q * (b[1] - a[1]) / d, q * (a[0] - b[0]) / d


def tangent_quad(center, u, v):
    """Intersect tangents in normal sequence u,v,-u,-v."""
    o, u, v = map(point, (center, u, v))
    q = dot(u, u)
    if not q:
        raise ValueError("zero radius")
    if dot(v, v) != q:
        raise ValueError("normals must be equal-length radius vectors")
    normals = (u, v, mul(-1, u), mul(-1, v))
    return tuple(add(o, intersection(a, b, q))
                 for a, b in zip(normals, normals[1:] + normals[:1]))


def circumscribe(center, u):
    """Return CCW vertices, starting at the intersection of u and Ju tangents."""
    u = point(u)
    return tangent_quad(center, u, turn(u))


def measurements(vertices):
    ps = tuple(map(point, vertices))
    a, b, c, d = ps
    es = tuple(sub(y, x) for x, y in zip(ps, ps[1:] + ps[:1]))
    return (tuple(dot(e, e) for e in es),
            tuple(dot(x, y) for x, y in zip(es, es[1:] + es[:1])),
            (dot(sub(c, a), sub(c, a)), dot(sub(d, b), sub(d, b))),
            sum(det(x, y) for x, y in zip(ps, ps[1:] + ps[:1])) / 2)


def verify(center, u, vertices):
    """Certify this construction's specified start, order and finite-side contacts."""
    o, u = map(point, (center, u))
    ps = tuple(map(point, vertices))
    q = dot(u, u)
    if not q or len(ps) != 4 or len(set(ps)) != 4:
        return False
    a, b, c, d = ps
    sides, dots, diags, area = measurements(ps)
    if sides != (4*q,) * 4 or dots != (0,) * 4 or diags != (8*q,) * 2 or area != 4*q:
        return False
    normals = (u, turn(u), mul(-1, u), mul(-1, turn(u)))
    for x, y, n in zip((d, a, b, c), (a, b, c, d), normals):
        contact = add(o, n)
        edge = sub(y, x)
        if add(x, y) != mul(2, contact) or dot(edge, n) != 0:
            return False
        # Check the actual edge supporting line, independent of intersection code.
        if det(edge, sub(o, x)) ** 2 != q * dot(edge, edge):
            return False
    return True


def run_grid():
    centers = ((0, 0), (F(1, 2), F(-1, 3)), (F(-3, 7), F(4, 9)))
    passed = rejected = 0
    for o, (x, y) in product(centers, product(range(-5, 6), repeat=2)):
        u = F(x, 3), F(y, 5)
        if u == (0, 0):
            try:
                circumscribe(o, u)
            except ValueError:
                rejected += 1
                continue
            raise RuntimeError("zero-radius case accepted")
        if not verify(o, u, circumscribe(o, u)):
            raise RuntimeError(f"certificate failure: {o}, {u}")
        passed += 1
    return passed, rejected


def formatted(vertices):
    return [tuple(map(str, p)) for p in vertices]


if __name__ == "__main__":
    o, u = (F(1, 2), F(-1, 3)), (2, 1)
    p = circumscribe(o, u)
    sides, dots, diags, area = measurements(p)
    print("vertices:", formatted(p))
    print("radius^2, side^2, diagonal^2, area:", dot(u, u), sides[0], diags[0], area)
    sides, dots, _, _ = measurements(tangent_quad((0, 0), (5, 0), (3, 4)))
    print("nonperpendicular tangencies: sides^2=", tuple(map(str, sides)),
          "adjacent dots=", tuple(map(str, dots)))
    print("grid (certified, zero-radius rejected):", run_grid())
