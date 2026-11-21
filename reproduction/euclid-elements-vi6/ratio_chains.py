"""Exact rational witnesses for Euclid VI.6 (modern teaching model)."""
from fractions import Fraction as Q
from itertools import product


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def mul(s, a):
    return s * a[0], s * a[1]


def perp(a):
    return -a[1], a[0]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return dot(perp(a), b)


def sq(a):
    return dot(a, a)


def angle_key(a, b):
    """Sign of cosine and its square distinguish all unsigned angles."""
    if not sq(a) or not sq(b):
        raise ValueError("angle requires two nonzero rays")
    d = dot(a, b)
    return (d > 0) - (d < 0), Q(d * d, sq(a) * sq(b))


def require_triangle(a, b, c):
    if not cross(sub(b, a), sub(c, a)):
        raise ValueError("nondegenerate triangle required")


def transport(u, v, x, sign):
    """Map u to v, and its perpendicular to ±perp(v), exactly."""
    if not sq(u) or not sq(v) or sign not in (-1, 1):
        raise ValueError("nonzero bases and orientation ±1 required")
    return add(mul(Q(dot(u, x), sq(u)), v),
               mul(sign * Q(cross(u, x), sq(u)), perp(v)))


def angle_keys(a, b, c):
    return tuple(angle_key(sub(y, x), sub(z, x))
                 for x, y, z in ((a, b, c), (b, a, c), (c, a, b)))


def squared_sides(a, b, c):
    return sq(sub(b, a)), sq(sub(c, a)), sq(sub(c, b))


def witnesses(a, b, c, d, e, f):
    """Return both possible G witnesses on the line DF's opposite half-planes."""
    require_triangle(a, b, c)
    require_triangle(d, e, f)
    ab, ac, de, df = sub(b, a), sub(c, a), sub(e, d), sub(f, d)
    if angle_key(ab, ac) != angle_key(de, df):
        raise ValueError("unequal included angles")
    if sq(ab) * sq(df) != sq(ac) * sq(de):
        raise ValueError("adjacent side ratios unequal")
    return tuple(add(d, transport(ac, df, ab, s)) for s in (1, -1))


def verify(a, b, c, d, e, f):
    """Check copied angles, common-side cancellation, and final angle transfer."""
    gs = witnesses(a, b, c, d, e, f)
    p = angle_keys(a, b, c)
    ss = squared_sides(a, b, c)
    ds = squared_sides(d, e, f)
    scale_sq = Q(ds[1], ss[1])
    certificates = []
    for g in gs:
        side_signature = squared_sides(d, g, f)
        angles = angle_keys(d, g, f)
        if angles != p or side_signature != tuple(scale_sq * s for s in ss):
            raise AssertionError("failed equiangular copy or simultaneous scaling")
        if side_signature[0] != ds[0] or side_signature[1] != ds[1]:
            raise AssertionError("common-side cancellation failed")
        if side_signature != ds or angles != angle_keys(d, e, f):
            raise AssertionError("SAS check or angle transfer failed")
        certificates.append((g, side_signature, angles))
    if cross(sub(f, d), sub(gs[0], d)) * cross(sub(f, d), sub(gs[1], d)) >= 0:
        raise AssertionError("witnesses must be on opposite sides of DF")
    return tuple(certificates)


A, B, C = (0, 0), (3, 0), (0, 4)
D, E, F = (10, 0), (Q(29, 2), 0), (10, 6)
WRONG_ANGLE = (Q(127, 10), Q(18, 5))


def exhaustive():
    bases = ((3, 4), (-3, 4), (2, -1))
    ab_s = ((1, 0), (0, 1), (2, 3), (3, -2))
    df_s = ((1, 0), (0, 3), (4, 1), (-1, -2))
    scales = (Q(1, 2), Q(1), Q(3, 2))
    n = mirrored = 0
    for ab, ac, dv, k, s in product(ab_s, bases, df_s, scales, (-1, 1)):
        if not cross(ac, ab):
            continue
        df = mul(k, dv)
        # Independently build E by complex multiplication and optional conjugation.
        denom = sq(ac)
        x, y = ab
        u, v = ac
        alpha, beta = Q(x * u + y * v, denom), s * Q(y * u - x * v, denom)
        ex, ey = df
        e = add(D, (alpha * ex - beta * ey, alpha * ey + beta * ex))
        verify(A, ab, ac, D, e, add(D, df))
        n += 1
        mirrored += s == -1
    return n, mirrored, 2 * n
