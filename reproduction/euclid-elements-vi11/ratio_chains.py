"""Exact coordinate teaching model of Euclid VI.11, not a general proof."""
from fractions import Fraction as Q
from itertools import product


def point(raw):
    if len(raw) != 2 or any(type(x) not in (int, Q) for x in raw):
        raise ValueError("point requires two exact rational coordinates")
    return tuple(map(Q, raw))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(t, u):
    return tuple(t * x for x in u)


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def norm2(u):
    return sum(x * x for x in u)


def construct(a, b, origin=(0, 0), u=(1, 0), v=(0, 1), *, copy_length=None):
    """Extend AB by AC, then intersect its new endpoint's parallel with AC."""
    if any(type(x) not in (int, Q) for x in (a, b)):
        raise ValueError("exact rational lengths required")
    a, b = Q(a), Q(b)
    d = b if copy_length is None else copy_length
    if type(d) not in (int, Q) or min(a, b, d) <= 0:
        raise ValueError("all lengths must be positive and exact")
    origin, u, v = map(point, (origin, u, v))
    if norm2(u) != 1 or norm2(v) != 1 or det(u, v) == 0:
        raise ValueError("independent unit directions required")
    A = origin
    B, C = add(A, scale(a, u)), add(A, scale(b, v))
    D = add(B, scale(d, u))
    w = sub(C, B)
    t = det(sub(D, A), w) / det(v, w)
    E = add(A, scale(t, v))
    return A, B, C, D, E


def ratio_squares(config):
    """Return squares of AB:BD and AC:CE without taking square roots."""
    A, B, C, D, E = config
    return (Q(norm2(sub(B, A)), norm2(sub(D, B))),
            Q(norm2(sub(C, A)), norm2(sub(E, C))))



def verify(config, a, b):
    """Check a complete VI.11 certificate including direction and point order."""
    A, B, C, D, E = config
    ab, ac, bd, ce, de, bc = sub(B, A), sub(C, A), sub(D, B), sub(E, C), sub(E, D), sub(C, B)
    def positive_multiple(u, v):
        return det(u, v) == 0 and sum(x * y for x, y in zip(u, v)) > 0
    if type(a) not in (int, Q) or type(b) not in (int, Q) or min(a, b) <= 0:
        return False
    expected = Q(b) ** 2 / a
    return (det(ab, ac) != 0 and positive_multiple(bd, ab)
            and positive_multiple(ce, ac) and positive_multiple(de, bc)
            and (norm2(ab), norm2(ac), norm2(bd), norm2(ce))
            == (a*a, b*b, b*b, expected*expected)
            and len(set(ratio_squares(config))) == 1)


def sweep():
    """576 deterministic configurations, each checked against b²/a."""
    lengths = (Q(1, 2), Q(2), Q(7, 3), Q(5))
    rotations = ((1, 0), (0, 1), (Q(3, 5), Q(4, 5)))
    rays = ((0, 1), (Q(3, 5), Q(4, 5)), (Q(-5, 13), Q(12, 13)))
    total = reflected = 0
    for a, b, (x, y), (r, s), mirror, origin in product(
        lengths, lengths, rotations, rays, (False, True), ((0, 0), (Q(-2, 3), 5))
    ):
        sign = -1 if mirror else 1
        u = (x, y)
        v = (x*r-sign*y*s, y*r+sign*x*s)
        if not verify(construct(a, b, origin, u, v), a, b):
            raise RuntimeError("inconsistent coordinate certificate")
        total += 1
        reflected += mirror
    return total, reflected
