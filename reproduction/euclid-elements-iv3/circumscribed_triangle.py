"""Exact rational teaching reconstruction of Euclid, Elements IV.3."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def mul(k, v):
    return (k * v[0], k * v[1])


def dot(x, y):
    return x[0] * y[0] + x[1] * y[1]


def cross(x, y):
    return x[0] * y[1] - x[1] * y[0]


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def rational(x):
    if type(x) not in (int, Q):
        raise TypeError("use int or Fraction, not floating-point inputs")
    return Q(x)


def point(v):
    x, y = v
    return rational(x), rational(y)


def unit(t):
    """(cos θ, sin θ) for t = tan(θ/2); all arithmetic is exact."""
    t = rational(t)
    den = 1 + t*t
    return (1-t*t)/den, 2*t/den


def tangent_pair(n, m, center, r):
    """Local solution n·(X-K) = m·(X-K) = r for distinct unit normals."""
    d = 1 + dot(n, m)
    if d <= 0 or n == m:
        raise ValueError("coincident or opposite support normals")
    return add(center, mul(r/d, add(n, m)))


def construct(t_e, t_f, center=(0, 0), r=1, b=(0, -1), width=1):
    """Return DEF, ABC, LMN and rotated outward support normals A/B/C."""
    t_e, t_f, r, width = map(rational, (t_e, t_f, r, width))
    center, b = point(center), point(b)
    if min(t_e, t_f, r, width) <= 0 or t_e*t_f >= 1:
        raise ValueError("require positive parameters and t_e*t_f < 1")
    if dot(b, b) != 1:
        raise ValueError("KB direction must be a rational unit vector")

    ec, es = unit(t_e)
    fc, fs = unit(t_f)
    e, f = (Q(0), Q(0)), (width, Q(0))
    det = ec*fs + es*fc
    require(det > 0, "source rays must diverge into a valid triangle")
    d = mul(width*fs/det, (ec, es))
    source = (d, e, f)
    original = ((-es, ec), (Q(0), Q(-1)), (fs, fc))

    # Rotation carrying (0, -1) to b and preserving the two copies' sides.
    bx, by = b
    def rotate(v):
        return (-by*v[0] - bx*v[1], bx*v[0] - by*v[1])

    a, _, c = normals = tuple(map(rotate, original))
    contacts = tuple(add(center, mul(r, n)) for n in normals)
    l = tangent_pair(c, a, center, r)
    m = tangent_pair(a, b, center, r)
    n = tangent_pair(b, c, center, r)
    triangle = (l, m, n)

    # Every cyclic gap lies in (0, π). Each support binds on the given
    # edge; its opposite vertex satisfies the inequality strictly.
    edges = ((l, m, n), (m, n, l), (n, l, m))
    scales = []
    for i, ((p, q, opposite), k, contact) in enumerate(zip(edges, normals, contacts)):
        require(dot(k, k) == 1 and cross(k, normals[(i+1) % 3]) > 0,
                "unit normals in the required cyclic order")
        require(dot(k, sub(p, center)) == dot(k, sub(q, center)) == r,
                "both edge endpoints must be on the support")
        require(dot(k, sub(opposite, center)) < r,
                "the opposite vertex must be strictly inside the half-plane")
        edge = sub(q, p)
        require(cross(edge, sub(contact, p)) == 0
                and 0 < dot(edge, sub(contact, p)) < dot(edge, edge),
                "contact must lie strictly between its two endpoints")
        proto = rotate(sub(source[(i+1) % 3], source[i]))
        require(cross(edge, proto) == 0 and dot(edge, proto) > 0,
                "corresponding directed edges must parallel each other")
        scales.append(dot(edge, proto)/dot(proto, proto))
    require(len(set(scales)) == 1, "all corresponding edges must scale equally")
    return source, contacts, triangle, normals


def angle_type(triangle):
    products = [dot(sub(triangle[(i+1) % 3], v), sub(triangle[(i+2) % 3], v))
                for i, v in enumerate(triangle)]
    return "obtuse" if min(products) < 0 else "right" if min(products) == 0 else "acute"


def grid():
    ts = tuple(Q(i, j) for i, j in ((1, 5), (1, 4), (1, 3), (1, 2), (2, 3),
                                    (3, 4), (1, 1), (3, 2), (2, 1), (3, 1)))
    counts = Counter()
    for e, f, b, center, radius, width in product(
        ts, ts, ((0, -1), (1, 0), unit(Q(2, 3))),
        ((0, 0), (Q(2, 3), Q(-5, 7))), (1, Q(7, 5)), (1, 3),
    ):
        if e*f >= 1:
            try:
                construct(e, f, center, radius, b, width)
            except ValueError:
                counts["inadmissible"] += 1
            else:
                raise ArithmeticError("accepted invalid angle sum")
        else:
            source, _, triangle, _ = construct(e, f, center, radius, b, width)
            kind = angle_type(source)
            require(kind == angle_type(triangle), "angle class must be preserved")
            counts[kind] += 1
    return dict(sorted(counts.items()))


def as_text(points):
    return " ".join("(" + ",".join(map(str, p)) + ")" for p in points)


if __name__ == "__main__":
    source, contacts, triangle, _ = construct(Q(1, 2), Q(1, 3), width=5)
    print("D E F:", as_text(source))
    print("A B C:", as_text(contacts))
    print("L M N:", as_text(triangle))
    print("grid:", grid())
