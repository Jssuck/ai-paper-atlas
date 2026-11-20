"""Euclid IV.15 in rational coefficients of a rotated, scaled sqrt(3) basis."""
from fractions import Fraction as Q
from math import isqrt

Point = tuple[Q, Q]


def neg(p):
    return (-p[0], -p[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def dot(p, q):
    # Coordinates (x,y) stand for x*u + sqrt(3)*y*J(u).
    # This dot product is normalized by the actual radius squared.
    return p[0] * q[0] + 3 * p[1] * q[1]


def det(p, q):
    # The omitted factor sqrt(3)*R^2 is strictly positive.
    return p[0] * q[1] - p[1] * q[0]


def norm2(p):
    return dot(p, p)


def rational_root(p):
    p, q = p.numerator, p.denominator
    m, n = isqrt(p), isqrt(q)
    if m*m != p or n*n != q:
        raise ValueError("intersection outside the rational-coefficient model")
    return Q(m, n)


def construct(u, aux_ratio2=1):
    """Return A,B,C,D,E,F; u is the rational vector from G to D."""
    a, b = map(Q, u)
    if not (a or b):
        raise ValueError("the input circle must have positive radius")
    q = Q(aux_ratio2)
    if not 0 < q < 4:
        raise ValueError("the circles must have two distinct intersections")
    x = 1 - q/2  # Subtract main-circle equation from auxiliary circle equation.
    y = rational_root((1-x*x)/3)
    d, e, c = (Q(1), Q(0)), (x, y), (x, -y)
    return neg(d), neg(e), c, d, e, neg(c)


def radius2(u):
    a, b = map(Q, u)
    return a*a+b*b


def certificate(vertices, u):
    """Report independent normalized point, edge, angle and traversal checks."""
    r2 = radius2(u)
    if r2 <= 0 or len(vertices) != 6:
        raise ValueError("six vertices and a positive radius required")
    v = tuple(vertices)
    edges2 = tuple(norm2(sub(v[(i+1)%6], v[i])) * r2 for i in range(6))
    radii2 = tuple(norm2(p)*r2 for p in v)
    angle_dots = tuple(
        dot(sub(v[i-1], v[i]), sub(v[(i+1)%6], v[i])) * r2
        for i in range(6)
    )
    turns = tuple(det(v[i], v[(i+1)%6]) for i in range(6))
    distinct = len(set(v)) == 6
    on_circle = all(n == r2 for n in radii2)
    # All six CCW steps, together with six distinct points and 60-degree
    # chords, certify the simple cyclic order rather than just a point set.
    ccw_steps = all(t > 0 for t in turns)
    regular = (distinct and on_circle and ccw_steps
               and all(n == r2 for n in edges2)
               and all(d == -r2/2 for d in angle_dots))
    return dict(radii2=radii2, edges2=edges2, angle_dots=angle_dots,
                distinct=distinct, on_circle=on_circle, ccw_steps=ccw_steps,
                regular=regular)


def grid():
    good = wrong = permuted = 0
    for i in range(1, 49):
        for sign in (-1, 1):
            u = (Q(sign*i, 7), Q(i+2, 11))
            v = construct(u)
            positive = certificate(v, u)
            bad_radius = certificate(construct(u, Q(12,19)), u)
            bad_order = certificate((v[0],v[2],v[1],*v[3:]),u)
            if not (positive["regular"]
                    and bad_radius["on_circle"] and not bad_radius["regular"]
                    and bad_order["on_circle"] and not bad_order["regular"]):
                raise RuntimeError("unexpected certificate in exact sample grid")
            good += 1
            wrong += 1
            permuted += 1
    return good, wrong, permuted


if __name__ == "__main__":
    print("Exact grid (regular, altered auxiliary radius, swapped order):", grid())
