"""Exact teaching model of Euclid VI.10, not a formalization of the text."""
from fractions import Fraction as Q


def point(p):
    x, y = p
    if any(type(v) not in (int, Q) for v in (x, y)):
        raise TypeError("coordinates must be exact rationals")
    return Q(x), Q(y)


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def advance(a, u, t):
    return a[0] + t * u[0], a[1] + t * u[1]


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def parameter(a, b, x):
    u, v = sub(b, a), sub(x, a)
    if u == (0, 0) or det(u, v):
        raise ValueError("point must be on a nonzero line")
    i = 0 if u[0] else 1
    return Q(v[i], u[i])


def intersect(a, u, b, v):
    denom = det(u, v)
    if not denom:
        raise ValueError("parallel or degenerate lines")
    return advance(a, u, Q(det(sub(b, a), v), denom))


def inputs(a, b, c, d, e):
    a, b, c, d, e = map(point, (a, b, c, d, e))
    if not det(sub(b, a), sub(c, a)):
        raise ValueError("ABC must be nondegenerate")
    t, s = parameter(a, c, d), parameter(a, c, e)
    if not 0 < t < s < 1:
        raise ValueError("expected strict order A-D-E-C")
    return a, b, c, d, e


def construct(a, b, c, d, e):
    """Return (F, G, H, K) via intersection, not assumed affine fractions."""
    a, b, c, d, e = inputs(a, b, c, d, e)
    u, v = sub(b, a), sub(b, c)
    f = intersect(a, u, d, v)
    g = intersect(a, u, e, v)
    h = intersect(d, u, e, v)
    k = intersect(d, u, c, v)
    return f, g, h, k


def affine(a, b, c, cuts):
    """Teaching extension: direct monotone normalized fractions for any cuts."""
    a, b, c = map(point, (a, b, c))
    u = sub(b, a)
    if not det(u, sub(c, a)):
        raise ValueError("ABC must be nondegenerate")
    ts = tuple(parameter(a, c, point(x)) for x in cuts)
    order = (0, *ts, 1)
    if not all(x < y for x, y in zip(order, order[1:])):
        raise ValueError("cuts must be strictly interior and ordered")
    return tuple(advance(a, u, t) for t in ts)


def certificate(a, b, c, d, e, f, g, h, k):
    """Check claimed points via order, parallelism, equal vectors and ratios."""
    a, b, c, d, e = inputs(a, b, c, d, e)
    f, g, h, k = map(point, (f, g, h, k))
    d0, e0 = parameter(a, c, d), parameter(a, c, e)
    f0, g0 = parameter(a, b, f), parameter(a, b, g)
    h0 = parameter(d, k, h)
    if not (0 < f0 < g0 < 1 and 0 < h0 < 1):
        raise ValueError("unexpected cut order")
    bc, ab = sub(b, c), sub(b, a)
    parallel = (
        det(sub(f, d), bc), det(sub(g, e), bc),
        det(sub(h, e), bc), det(sub(k, c), bc), det(sub(k, d), ab),
    )
    if any(parallel) or h == e or k == c:
        raise ValueError("lost required parallelism")
    if sub(h, d) != sub(g, f) or sub(k, h) != sub(b, g):
        raise ValueError("opposite parallelogram sides not equal")
    twice = ((1-e0)/(e0-d0), (1-h0)/h0, (1-g0)/(g0-f0))
    nested = ((e0-d0)/d0, (g0-f0)/f0)
    if len(set(twice)) > 1 or len(set(nested)) > 1:
        raise ValueError("ratio chain failed")
    return twice, nested


EXAMPLE = ((0, 0), (14, 0), (7, 7), (2, 2), (5, 5))


def sweep():
    """Test all cuts for denominator 3..8 for 18 oriented coordinate frames."""
    checked = reflected = 0
    for a in ((0, 0), (7, -3), (-2, 17)):
        for u in ((14, 0), (3, 8), (-5, 4)):
            for sign in (-1, 1):
                v = (-sign * u[1], sign * u[0])
                b, c = advance(a, u, 1), advance(a, v, 1)
                for n in range(3, 9):
                    for m in range(1, n-1):
                        for k in range(m+1, n):
                            d, e = (advance(a, v, Q(j, n)) for j in (m, k))
                            fg_hk = construct(a, b, c, d, e)
                            certificate(a, b, c, d, e, *fg_hk)
                            if affine(a, b, c, (d, e)) != fg_hk[:2]:
                                raise ValueError("affine oracle disagreement")
                            checked += 1
                            reflected += sign < 0
    return checked, reflected
