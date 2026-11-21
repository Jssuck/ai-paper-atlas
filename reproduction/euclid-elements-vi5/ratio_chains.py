"""Exact coordinate probes of Euclid VI.5, not a general proof."""
from fractions import Fraction as Q


def point(x, y):
    return Q(x), Q(y)


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]


def det(a, b):
    return a[0]*b[1] - a[1]*b[0]


def angle_signature(a, b, c):
    u, v = sub(b, a), sub(c, a)
    n = dot(u, u)*dot(v, v)
    if not n:
        raise ValueError("zero-length angle arm")
    d = dot(u, v)
    return (d > 0) - (d < 0), Q(d*d, n)


def sides(tri):
    return tuple(dot(w, w) for w in
                 (sub(tri[i], tri[(i+1) % 3]) for i in range(3)))


def angles(tri):
    return tuple(angle_signature(tri[i], tri[(i+1) % 3], tri[(i+2) % 3])
                 for i in range(3))


def orientation(tri):
    return det(sub(tri[1], tri[0]), sub(tri[2], tri[0]))


def construct_g(a, b, c, e, f):
    """Place the angle-copy candidate on the left of directed line EF."""
    u, v, w = sub(c, b), sub(a, b), sub(f, e)
    n = dot(u, u)
    cross = det(u, v)
    if not n or not cross or not dot(w, w):
        raise ValueError("nondegenerate source triangle and target base required")
    # Coordinates along directed BC and its left normal, in units of BC.
    x, y = Q(dot(u, v), n), Q(abs(cross), n)
    wx, wy = w
    return e[0] + x*wx - y*wy, e[1] + x*wy + y*wx


def probe(abc, target):
    """Check angle and length predicates independently; save the proof witness."""
    if not orientation(abc) or not orientation(target):
        raise ValueError("two nondegenerate triangles required")
    a, b, c = abc
    d, e, f = target
    g = construct_g(a, b, c, e, f)
    copied = (g, e, f)
    s, r, h = sides(abc), sides(target), sides(copied)
    scale_sq = Q(r[1], s[1])
    return {"g": g, "side_ratios_sq": tuple(Q(x, y) for x, y in zip(r, s)),
            "copy_ratios_sq": tuple(Q(x, y) for x, y in zip(h, s)),
            "proportional": all(ri == scale_sq*si for ri, si in zip(r, s)),
            "copied_angles": angles(abc) == angles(copied),
            "equal_angles": angles(abc) == angles(target),
            "ss_equal": r == h,
            "same_half_plane": (det(sub(f, e), sub(d, e)) > 0)}


A, B, C = point(0, 3), point(0, 0), point(4, 0)
E, F = point(10, 0), point(16, 0)
D, M = point(10, Q(9, 2)), point(10, -Q(9, 2))
N = point(Q(127, 10), Q(18, 5))
ABC = (A, B, C)


def exercise_grid():
    """Positive tests by exact transformations, not by filtering for the claim."""
    count = 0
    for a in (point(0, 3), point(1, 2), point(-2, 1), point(5, 1)):
        for shift in (point(0, 0), point(3, -2), point(Q(1, 3), Q(2, 5))):
            for k in (Q(1, 3), Q(1), Q(3, 2)):
                for u, v in ((1, 0), (0, 1), (Q(3, 5), Q(4, 5))):
                    for sign in (-1, 1):
                        def transform(p):
                            x, y = p[0], sign*p[1]
                            return (shift[0] + k*(u*x-v*y),
                                    shift[1] + k*(v*x+u*y))
                        abc = a, B, C
                        p = probe(abc, tuple(map(transform, abc)))
                        if (not all(p[key] for key in
                                    ("proportional", "copied_angles", "equal_angles", "ss_equal"))
                                or p["side_ratios_sq"] != (k*k,)*3
                                or p["copy_ratios_sq"] != (k*k,)*3
                                or p["same_half_plane"] != (sign == 1)):
                            raise AssertionError(p)
                        count += 1
    return count


if __name__ == "__main__":
    print(f"grid: {exercise_grid()} exact configurations (both placements)")
