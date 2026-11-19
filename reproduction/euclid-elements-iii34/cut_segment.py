"""Exact coordinate classroom model of Euclid's Elements III.34."""
from fractions import Fraction as Q
from itertools import product

B = (Q(0), Q(0))
F = (Q(1), Q(0))


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def scale(k, a):
    return k*a[0], k*a[1]


def signature(a, b):
    if a == B or b == B:
        raise ValueError("angle needs two nonzero rays")
    return dot(a, b), abs(det(a, b))


def same_angle(a, b):
    return det(a, b) == 0 and dot(a, b) > 0


def second_hit(radius, ray):
    """Intersect an inward ray from B with the circle centered at (0,R)."""
    r, u, v = Q(radius), Q(ray[0]), Q(ray[1])
    if r <= 0 or v <= 0:
        raise ValueError("positive radius and strictly inward ray required")
    return scale(2*r*v/(u*u+v*v), (u, v))


def construct(radius, ray):
    """Return chord endpoint C, alternate-arc P and same-side control Q."""
    u, v = map(Q, ray)
    c = second_hit(radius, (u, v))
    k = v/(abs(u)+v)
    p = second_hit(radius, (-1, k))
    q = second_hit(radius, (1, k))
    return c, p, q


def inspect(radius, ray, c, p, q):
    """Check exact geometric predicates directly, separate from generation."""
    r, (u, v) = Q(radius), tuple(map(Q, ray))
    o = (0, r)
    same_circle = all(dot(sub(a, o), sub(a, o)) == r*r for a in (B, c, p, q))
    distinct = len({B,c,p,q}) == 4
    chord_ray = c != B and det(c, (u, v)) == 0 and dot(c, (u, v)) > 0
    tangent = dot(sub(B, o), F) == 0
    alternate = det(c, F)*det(c, p) < 0
    same_side = det(c, F)*det(c, q) > 0
    endpoint_ok = distinct and v > 0
    target = signature(F, (u, v)) if endpoint_ok else None
    matched = signature(sub(B, p), sub(c, p)) if endpoint_ok else None
    control = signature(sub(B, q), sub(c, q)) if endpoint_ok else None
    return {
        "radius_positive": r > 0, "strictly_inward": v > 0, "tangent": tangent,
        "same_circle": same_circle, "distinct": distinct, "positive_chord_ray": chord_ray,
        "alternate_side": alternate, "same_side_control": same_side,
        "matched_angle": endpoint_ok and same_angle(target, matched),
        "control_supplement": endpoint_ok and same_angle((-target[0],target[1]), control),
        "control_equal_iff_right": endpoint_ok and (same_angle(target,control) == (u == 0)),
    }


def finite_sweep():
    directions = sorted({Q(u, v) for u in range(-8,9) for v in range(1,8)})
    counts = {"acute": 0, "right": 0, "obtuse": 0}
    for radius, slope in product((Q(1,3), Q(1), Q(5)), directions):
        ray = (slope, Q(1))
        found = inspect(radius, ray, *construct(radius, ray))
        if not all(found.values()):
            raise RuntimeError(f"failed exact certificate: {radius=}, {ray=}, {found=}")
        counts["acute" if slope > 0 else "obtuse" if slope < 0 else "right"] += 1
    return sum(counts.values()), counts


def main():
    for name, u in (("acute",3), ("right",0), ("obtuse",-3)):
        ray = (u,4)
        c, p, q = construct(5,ray)
        printable = lambda z: tuple(map(str,z))
        print(name, "C", printable(c), "P", printable(p), "Q", printable(q))
        print(inspect(5,ray,c,p,q))
    total, counts = finite_sweep()
    print("exact cases:", total, counts)


if __name__ == "__main__":
    main()
