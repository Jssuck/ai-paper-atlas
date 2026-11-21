"""Exact coordinate probes for Euclid VI.3; no floating-point arithmetic."""
from fractions import Fraction as F
from math import isqrt


def point(x, y):
    return (F(x), F(y))


def plus(u, v):
    return (u[0] + v[0], u[1] + v[1])


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def scale(k, u):
    return (k * u[0], k * u[1])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def rational_norm(u):
    """Return length if rational; raise rather than approximate otherwise."""
    square = F(dot(u, u))
    p, q = isqrt(square.numerator), isqrt(square.denominator)
    if p * p != square.numerator or q * q != square.denominator:
        raise ValueError("probe requires rational lengths AB and AC")
    return F(p, q)


def cut(b, c, t):
    return plus(b, scale(F(t), sub(c, b)))


def probe(a, b, c, d):
    """Compare an unsigned segment ratio with an independent angle predicate.

    Compare the dots of AD with the unit rays AB and AC. The common factor
    length(AD) is not needed to decide whether the two cosines agree.
    """
    ab, ac, ad, bc = sub(b, a), sub(c, a), sub(d, a), sub(c, b)
    if not det(ab, ac):
        raise ValueError("triangle must be noncollinear")
    bd = sub(d, b)
    k = 0 if bc[0] else 1
    t = F(bd[k], bc[k])
    if t in (0, 1) or d != cut(b, c, t):
        raise ValueError("D must be on line BC and distinct from B and C")

    m, n = rational_norm(ab), rational_norm(ac)
    radial_ratio = m / n
    # BD and DC are scalar multiples of a single direction, regardless
    # of whether that direction has a rational length.
    segment_ratio = abs(t) / abs(1 - t)
    unit_b, unit_c = scale(1 / m, ab), scale(1 / n, ac)
    cosine_delta_times_ad = dot(ad, sub(unit_b, unit_c))
    exterior_cosine_sum_times_ad = dot(ad, plus(unit_b, unit_c))
    interior = 0 < t < 1
    return {
        "parameter": t,
        "interior": interior,
        "segment_ratio": segment_ratio,
        "side_ratio": radial_ratio,
        "equal_ratio": segment_ratio == radial_ratio,
        "cosine_delta_times_ad": cosine_delta_times_ad,
        "interior_bisector": interior and cosine_delta_times_ad == 0,
        "external_bisector_line": exterior_cosine_sum_times_ad == 0,
    }


def construct_e(a, b, c, d):
    """Intersection of line AB and the line through C parallel to AD."""
    ab, ac, ad = sub(b, a), sub(c, a), sub(d, a)
    den = det(ab, ad)
    if not den:
        raise ValueError("lines AB and CE are parallel or coincident")
    return plus(a, scale(F(det(ac, ad), den), ab))


A, B, C = point(0, 0), point(21, 0), point(0, 28)
D, Q, P = point(12, 12), point(9, 16), point(84, -84)


def exercise_grid():
    """Interior point parameters and two exact checks for each."""
    accepted = total = 0
    for a in (point(0, 0), point(2, -3), point(F(1, 3), F(2, 5))):
        for u, v in ((point(1, 0), point(0, 1)),
                     (point(F(3, 5), F(4, 5)), point(0, 1)),
                     (point(F(3, 5), F(-4, 5)), point(0, 1))):
            for m, n in ((2, 3), (3, 2), (3, 4), (5, 5), (7, 4)):
                b, c = plus(a, scale(m, u)), plus(a, scale(n, v))
                target = F(m, m + n)
                params = {F(j, d) for d in range(2, 10) for j in range(1, d)}
                for t in sorted(params | {target}):
                    d = cut(b, c, t)
                    p = probe(a, b, c, d)
                    expected = t == target
                    if p["equal_ratio"] != expected or p["interior_bisector"] != expected:
                        raise AssertionError((a, b, c, d, p))
                    e = construct_e(a, b, c, d)
                    if det(sub(e, c), sub(d, a)) or det(sub(e, a), sub(b, a)):
                        raise AssertionError("construction not collinear/parallel")
                    if (rational_norm(sub(e, a)) == F(n)) != expected:
                        raise AssertionError("isosceles auxiliary triangle mismatch")
                    total += 1
                    accepted += expected
    return total, accepted


if __name__ == "__main__":
    total, accepted = exercise_grid()
    print(f"grid: {total} interior probes ({accepted} true, {total - accepted} false)")
