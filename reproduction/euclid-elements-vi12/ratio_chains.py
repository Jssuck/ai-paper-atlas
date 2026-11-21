"""Exact coordinate teaching model for Euclid Elements VI.12."""
from fractions import Fraction as Q
from itertools import product


def vector(p):
    if len(p) != 2 or any(type(x) not in (int, Q) for x in p):
        raise ValueError("expected two rational coordinates")
    return tuple(map(Q, p))


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


def dot(p, q):
    return p[0]*q[0] + p[1]*q[1]


def add(p, q):
    return p[0]+q[0], p[1]+q[1]


def sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def mul(k, p):
    return k*p[0], k*p[1]


def positions(a, b, c, D, u, v):
    if any(type(z) not in (int, Q) or z <= 0 for z in (a, b, c)):
        raise ValueError("three positive rational lengths required")
    D, u, v = map(vector, (D, u, v))
    if dot(u, u) != 1 or dot(v, v) != 1 or not det(u, v):
        raise ValueError("two noncollinear unit directions required")
    G = add(D, mul(a, u))
    E = add(G, mul(b, u))
    H = add(D, mul(c, v))
    return D, G, E, H, v


def intersection(D, G, E, H, v):
    """Intersect E + t(H−G) with D + s*v, solving for s by determinants."""
    w = sub(H, G)
    denominator = det(v, w)
    if not denominator:
        raise ValueError("no unique line intersection")
    s = det(sub(E, D), w) / denominator
    return add(D, mul(s, v))


def construct(a, b, c, D=(0, 0), u=(1, 0), v=(0, 1)):
    D, G, E, H, v = positions(a, b, c, D, u, v)
    return D, G, E, H, intersection(D, G, E, H, v)


def certificate(a, b, c, points):
    """Validate positions, positive order, parallelism and ratio by exact arithmetic."""
    if len(points) != 5 or any(type(z) not in (int, Q) or z <= 0 for z in (a, b, c)):
        raise ValueError("invalid lengths or point count")
    D, G, E, H, F = map(vector, points)
    dg, ge, dh, hf = sub(G, D), sub(E, G), sub(H, D), sub(F, H)
    if not det(dg, dh) or det(dg, ge) or det(dh, hf):
        raise ValueError("rays are degenerate or points lie off their rays")
    if dot(dg, ge) <= 0 or dot(dh, hf) <= 0:
        raise ValueError("segment order is invalid")
    if tuple(dot(z, z) for z in (dg, ge, dh)) != (a*a, b*b, c*c):
        raise ValueError("given or copied lengths do not match")
    if det(sub(F, E), sub(H, G)):
        raise ValueError("parallel condition fails")
    # Along unit v=DH/c; positive dot gives unsigned tail length.
    x = dot(hf, dh) / c
    if a*x != b*c:
        raise ValueError("ratio check fails")
    return x


def sweep():
    """Compare the intersection algorithm with the direct positive-length oracle."""
    lengths = (Q(1, 3), Q(3, 2), Q(4), Q(7))
    directions = ((1, 0), (0, 1), (Q(3,5), Q(4,5)))
    count = reflected = 0
    for (a, b, c), D, u, v, mirror in product(
        product(lengths, repeat=3), ((0, 0), (2, -3)), directions,
        ((Q(-4,5), Q(3,5)), (Q(5,13), Q(12,13))), (False, True)
    ):
        if mirror:
            u, v = (u[0], -u[1]), (v[0], -v[1])
        pts = construct(a, b, c, D, u, v)
        x = b*c/a
        if pts[-1] != add(D, mul(c+x, v)) or certificate(a, b, c, pts) != x:
            raise RuntimeError("intersection disagrees with direct formula")
        count += 1
        reflected += mirror
    return count, reflected
