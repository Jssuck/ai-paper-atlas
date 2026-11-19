"""Exact coordinate reconstruction of Euclid IV.8 (not a historical simulator)."""
from fractions import Fraction as F
from itertools import product


def point(p):
    x, y = p
    if any(type(k) not in (int, F) for k in (x, y)):
        raise TypeError("use exact int or Fraction coordinates")
    return F(x), F(y)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def scale(k, a):
    return k * a[0], k * a[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def sides(ps):
    return tuple(zip(ps, ps[1:] + ps[:1]))


def square(vertices):
    ps = tuple(map(point, vertices))
    if len(ps) != 4:
        raise ValueError("expected four vertices in boundary order")
    a, b, c, d = ps
    e, f = sub(b, a), sub(d, a)
    q = dot(e, e)
    if not q or dot(f, f) != q or dot(e, f) or c != add(b, f):
        raise ValueError("vertices do not form a nondegenerate square in boundary order")
    return ps


def inscribe(vertices):
    """Return (center, radius squared, contacts for AB, BC, CD, DA)."""
    a, b, c, d = ps = square(vertices)
    mid = lambda x, y: scale(F(1, 2), add(x, y))
    center = mid(a, c)
    return center, dot(sub(b, a), sub(b, a)) / 4, tuple(mid(x, y) for x, y in sides(ps))


def verify(vertices, candidate):
    """Check the square, line equations, supporting half-planes and finite contacts."""
    try:
        ps = square(vertices)
    except ValueError:
        return False
    center, radius_sq, contacts = candidate
    center = point(center)
    if type(radius_sq) not in (int, F) or radius_sq <= 0:
        return False
    contacts = tuple(map(point, contacts))
    if len(contacts) != 4 or len(set(contacts)) != 4:
        return False
    for (x, y), t in zip(sides(ps), contacts):
        edge, xt = sub(y, x), sub(t, x)
        length_sq = dot(edge, edge)
        if det(edge, xt) or not 0 < dot(edge, xt) < length_sq:
            return False
        if dot(edge, sub(center, t)) or dot(sub(center, t), sub(center, t)) != radius_sq:
            return False
        center_side = det(edge, sub(center, x))
        if not center_side or any(center_side * det(edge, sub(p, x)) < 0 for p in ps):
            return False
    return True


def line_distance_squares(vertices, center):
    """Supporting-line distances, also defined for a nonsquare rectangle."""
    ps, center = tuple(map(point, vertices)), point(center)
    edges = [(sub(y, x), sub(center, x)) for x, y in sides(ps)]
    if any(not dot(e, e) for e, _ in edges):
        raise ValueError("zero-length edge")
    return tuple(det(e, z)**2 / dot(e, e) for e, z in edges)


def build_square(a, e):
    a, e = point(a), point(e)
    f = -e[1], e[0]
    return a, add(a, e), add(add(a, e), f), add(a, f)


EXAMPLE = build_square((F(1, 2), F(-1, 3)), (4, 2))
RECTANGLE = ((0, 0), (4, 0), (4, 2), (0, 2))


def run_grid():
    anchors = ((0, 0), (F(1, 2), F(-1, 3)), (F(-3, 7), F(4, 9)))
    passed = rejected = 0
    for a, (x, y) in product(anchors, product(range(-5, 6), repeat=2)):
        ps = build_square(a, (F(x, 3), F(y, 5)))
        if not x and not y:
            try:
                inscribe(ps)
            except ValueError:
                rejected += 1
                continue
            raise RuntimeError("zero-side case accepted")
        if not verify(ps, inscribe(ps)):
            raise RuntimeError(f"invalid circle certificate: {ps}")
        passed += 1
    return passed, rejected


def formatted(ps):
    return tuple(tuple(map(str, p)) for p in ps)


if __name__ == "__main__":
    center, radius_sq, contacts = inscribe(EXAMPLE)
    print("vertices:", formatted(EXAMPLE))
    print("center, radius^2:", formatted((center,))[0], radius_sq)
    print("contacts:", formatted(contacts))
    print("center-to-side-line distance^2:", tuple(map(str, line_distance_squares(EXAMPLE, center))))
    print("certificate:", verify(EXAMPLE, (center, radius_sq, contacts)))
    print("rectangle center distances^2:", tuple(map(str, line_distance_squares(RECTANGLE, (2, 1)))))
    try:
        inscribe(RECTANGLE)
    except ValueError:
        print("nonsquare rectangle rejected")
    else:
        raise RuntimeError("rectangle wrongly accepted")
    print("grid (certified, zero-side rejected):", run_grid())
