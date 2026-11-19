"""Exact educational model of Euclid IV.4 for rational-coordinate triangles."""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import permutations, product
from math import isqrt


Point = tuple[Q, Q]


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def scale(k, u):
    return k * u[0], k * u[1]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def length(u):
    d = Q(dot(u, u))
    n, m = isqrt(d.numerator), isqrt(d.denominator)
    if n*n != d.numerator or m*m != d.denominator:
        raise ValueError("irrational side length is outside this exact model")
    return Q(n, m)


def triangle(A, B, C):
    def point(P):
        x, y = P
        if not all(isinstance(t, (int, Q)) for t in (x, y)):
            raise TypeError("coordinates must be integers or Fraction")
        return Q(x), Q(y)

    A, B, C = map(point, (A, B, C))
    det = cross(sub(B, A), sub(C, A))
    if not det:
        raise ValueError("triangle must be noncollinear")
    return A, B, C, det


def bisector_center(A, B, C):
    """Independent comparison: intersect the two interior bisector rays."""
    A, B, C, _ = triangle(A, B, C)
    ab, bc, ca = sub(A, B), sub(C, B), sub(A, C)
    u = add(scale(1/length(ab), ab), scale(1/length(bc), bc))
    v = add(scale(1/length(ca), ca), scale(-1/length(bc), bc))
    w = cross(u, v)
    if not w:
        raise ArithmeticError("internal angle bisectors unexpectedly parallel")
    t = cross(bc, v)/w
    s = cross(bc, u)/w
    if t <= 0 or s <= 0:
        raise ArithmeticError("intersection is not on both forward rays")
    return add(B, scale(t, u))


@dataclass(frozen=True)
class Incircle:
    center: Point
    radius: Q
    E: Point  # AB
    F: Point  # BC
    G: Point  # CA


def construct(A, B, C):
    """Construct and check a labeled incircle certificate using exact fractions."""
    A, B, C, det = triangle(A, B, C)
    sides = [(A, B), (B, C), (C, A)]
    c, a, b = [length(sub(V, U)) for U, V in sides]
    perimeter = a+b+c
    D = scale(1/perimeter, add(add(scale(a, A), scale(b, B)), scale(c, C)))
    r = abs(det)/perimeter
    sign = 1 if det > 0 else -1
    if bisector_center(A, B, C) != D:
        raise ArithmeticError("weighted center disagrees with the two bisectors")
    touches = []
    for (U, V), side_length in zip(sides, (c, a, b)):
        uv, di = sub(V, U), sub(D, U)
        t = dot(di, uv)/dot(uv, uv)
        H = add(U, scale(t, uv))
        if not (0 < t < 1 and
                sign * cross(uv, di) == side_length*r and
                dot(sub(D, H), uv) == 0 and
                dot(sub(D, H), sub(D, H)) == r*r):
            raise ArithmeticError("invalid oriented tangent contact")
        touches.append(H)
    E, F, G = touches
    for vertex, p, q in ((A, E, G), (B, E, F), (C, F, G)):
        vp, vq = sub(p, vertex), sub(q, vertex)
        if dot(vp, vp) != dot(vq, vq):
            raise ArithmeticError("unequal tangents from one vertex")
    return Incircle(D, r, E, F, G)


FIXTURES = {
    "acute": ((5, 12), (0, 0), (14, 0)),
    "right": ((0, 0), (4, 0), (0, 3)),
    "obtuse": ((9, 12), (0, 0), (4, 0)),
    "obtuse_isosceles": ((12, 5), (0, 0), (24, 0)),
}


def kind(*p):
    x, y, z = sorted(dot(sub(p[i], p[j]), sub(p[i], p[j]))
                     for i, j in ((0, 1), (1, 2), (2, 0)))
    return "right" if x+y == z else "acute" if x+y > z else "obtuse"


def grid():
    counts = {k: 0 for k in ("acute", "right", "obtuse", "invalid")}
    rotates = ((1, 0), (0, 1), (Q(3, 5), Q(4, 5)), (Q(-5, 13), Q(12, 13)))
    for points, perm, k, (u, v), offset in product(
        FIXTURES.values(), permutations(range(3)), (Q(1, 3), Q(1), Q(5, 2)),
        rotates, ((0, 0), (Q(2, 7), Q(-3, 5))),
    ):
        def transform(p):
            x, y = p
            return add(scale(k, (u*x-v*y, v*x+u*y)), offset)

        P = tuple(points[i] for i in perm)
        base, moved = construct(*P), construct(*map(transform, P))
        if moved != Incircle(transform(base.center), k*base.radius,
                             *(transform(H) for H in (base.E, base.F, base.G))):
            raise ArithmeticError("similarity or labeling invariance failed")
        counts[kind(*P)] += 1
    for inp in (((0, 0), (0, 0), (2, 3)),
                ((0, 0), (1, 1), (2, 2)),
                ((0, 0), (1, 0), (0, 1))):
        try:
            construct(*inp)
        except ValueError:
            counts["invalid"] += 1
        else:
            raise ArithmeticError("invalid input was accepted")
    return counts


if __name__ == "__main__":
    for name in FIXTURES:
        result = construct(*FIXTURES[name])
        print(name, "D =", result.center, "r =", result.radius)
        print("  E/F/G =", result.E, result.F, result.G)
    print("grid:", grid())
