"""Exact teaching reconstruction for Elements IV.9; no historical code."""
from fractions import Fraction as F
from itertools import product


def point(raw):
    x, y = raw
    if type(x) not in (int, F) or type(y) not in (int, F):
        raise TypeError("coordinates must be exact integers or Fraction")
    return F(x), F(y)


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def scale(k, a):
    return k*a[0], k*a[1]


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def diagonal_intersection(vertices):
    a, b, c, d = map(point, vertices)
    p, q = sub(c, a), sub(d, b)
    denom = det(p, q)
    if not denom:
        raise ValueError("the diagonals have no unique intersection")
    return add(a, scale(det(sub(b, a), q)/denom, p))


def vertex_distances2(center, vertices):
    o = point(center)
    vectors = [sub(point(p), o) for p in vertices]
    return tuple(dot(v, v) for v in vectors)


def boundary(a, e, f):
    return a, add(a, e), add(a, add(e, f)), add(a, f)


def _rectangle(vertices, square):
    a, b, c, d = ps = tuple(map(point, vertices))
    e, f = sub(b, a), sub(d, a)
    e2, f2 = dot(e, e), dot(f, f)
    if not e2 or not f2 or dot(e, f) or c != add(b, f):
        raise ValueError("expected a nondegenerate rectangle in boundary order")
    if square and e2 != f2:
        raise ValueError("expected a square, not just a rectangle")
    return ps


def rectangle_circumcircle(vertices):
    """Modern extension: allow unequal adjacent sides, but still orthogonal."""
    ps = _rectangle(vertices, square=False)
    o = diagonal_intersection(ps)
    return o, vertex_distances2(o, ps)[0]


def circumscribe(vertices):
    """IV.9 scope: accept only nondegenerate squares."""
    ps = _rectangle(vertices, square=True)
    o = diagonal_intersection(ps)
    return o, vertex_distances2(o, ps)[0]


def verify_square_circle(vertices, center, radius2):
    """Check input geometry from cyclic edges and check incidence independently."""
    ps = tuple(map(point, vertices))
    if len(ps) != 4 or len(set(ps)) != 4 or type(radius2) not in (F, int) or radius2 <= 0:
        return False
    edges = tuple(sub(ps[(i+1) % 4], ps[i]) for i in range(4))
    lengths = tuple(dot(v, v) for v in edges)
    if not lengths[0] or len(set(lengths)) != 1:
        return False
    if any(dot(edges[i], edges[(i+1) % 4]) for i in range(4)):
        return False
    # Reject a crossed ordering even if some local checks happen to coincide.
    turns = tuple(det(edges[i], edges[(i+1) % 4]) for i in range(4))
    if not turns[0] or len(set(turns)) != 1:
        return False
    return vertex_distances2(center, ps) == (radius2,)*4


def examples():
    square = boundary((F(1, 2), F(-1, 3)), (4, 2), (-2, 4))
    rect = boundary((0, 0), (4, 0), (0, 2))
    rhombus = boundary((0, 0), (5, 0), (3, 4))
    return square, rect, rhombus


def run_grid():
    starts = ((0, 0), (F(1, 2), F(-1, 3)), (F(-3, 7), F(4, 9)))
    passed = rejected = 0
    for a, (x, y) in product(starts, product(range(-5, 6), repeat=2)):
        e = F(x, 3), F(y, 5)
        ps = boundary(a, e, (-e[1], e[0]))
        if e == (0, 0):
            try:
                circumscribe(ps)
            except ValueError:
                rejected += 1
                continue
            raise RuntimeError("zero edge unexpectedly accepted")
        if not verify_square_circle(ps, *circumscribe(ps)):
            raise RuntimeError("certificate rejected")
        passed += 1
    return passed, rejected


def show_point(p):
    return tuple(map(str, p))


if __name__ == "__main__":
    sq, rect, rhombus = examples()
    o, radius2 = circumscribe(sq)
    print("square:", tuple(map(show_point, sq)))
    print("center, radius^2:", show_point(o), str(radius2))
    print("certificate:", verify_square_circle(sq, o, radius2))
    o, radius2 = rectangle_circumcircle(rect)
    print("nonsquare rectangle center, radius^2:", show_point(o), str(radius2))
    o = diagonal_intersection(rhombus)
    print("rhombus center, vertex distances^2:", show_point(o),
          tuple(map(str, vertex_distances2(o, rhombus))))
    print("grid (certified, zero-side rejected):", run_grid())
