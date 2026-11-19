"""Exact coordinate checks for a teaching reconstruction of Elements III.36."""
from fractions import Fraction as Q


def point(x, y):
    return Q(x), Q(y)


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(k, a):
    return k * a[0], k * a[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def norm2(a):
    return dot(a, a)


def verify(o, r, d, c, a, b):
    """Check the premises first; return exact identities for one configuration."""
    o, d, c, a, b = (point(*xy) for xy in (o, d, c, a, b))
    r = Q(r)
    if not r > 0 or norm2(sub(d, o)) <= r*r:
        raise ValueError("positive radius and exterior D required")
    if any(norm2(sub(p, o)) != r*r for p in (a, b, c)):
        raise ValueError("A, B and C must be on the circle")
    near, far = sub(c, d), sub(a, d)
    if cross(near, far) or not 0 < dot(near, far) < norm2(far):
        raise ValueError("secant order must be D, C, A with distinct points")
    if dot(sub(b, o), sub(d, b)):
        raise ValueError("DB must be tangent at B")
    # Dot product equals positive length product when the vectors share a ray.
    product, tangent_sq = dot(near, far), norm2(sub(b, d))
    f = mul(Q(1, 2), add(a, c))
    fc2, fo2, fd2 = (norm2(sub(f, p)) for p in (c, o, d))
    od2 = norm2(sub(o, d))
    if not (
        dot(sub(o, f), sub(a, c)) == 0
        and product + fc2 == fd2                       # II.6
        and fc2 + fo2 == r*r and fd2 + fo2 == od2     # I.47 or center case
        and od2 == r*r + tangent_sq                   # I.47 at B
        and product == tangent_sq
    ):
        raise ArithmeticError("an exact identity failed")
    return {
        "branch": "diameter" if f == o else "offset",
        "product": product, "tangent_squared": tangent_sq,
        "half_chord_squared": fc2, "center_offset_squared": fo2,
        "midpoint_to_d_squared": fd2,
    }


def circle_point(t):
    return (1-t*t)/(1+t*t), 2*t/(1+t*t)


def sweep():
    """Finite rational sample; derive one secant from each visible endpoint C."""
    unit = [circle_point(Q(i, 3)) for i in range(-9, 10)] + [point(-1, 0)]
    counts = {"diameter": 0, "offset": 0}
    for o, r in [(point(0, 0), Q(5)), (point(Q(1, 3), Q(-2, 5)), Q(7, 3))]:
        for ub in unit:
            b = add(o, mul(r, ub))
            for k, dscale in [(Q(3, 4), Q(5, 4)), (Q(-4, 3), Q(5, 3)),
                              (Q(5, 12), Q(13, 12))]:
                d = add(b, mul(r*k, (-ub[1], ub[0])))
                toward_d = mul(1/(r*dscale), sub(d, o))
                for uc in [*sorted(set(unit)-{toward_d}), toward_d]:
                    c = add(o, mul(r, uc))
                    w = sub(c, d)
                    h = -2 * dot(sub(c, o), w)
                    if h <= 0:
                        continue                      # tangent at C or far endpoint
                    a = add(c, mul(h/norm2(w), w))
                    cert = verify(o, r, d, c, a, b)
                    counts[cert["branch"]] += 1
    return counts


O = point(0, 0)
DIAMETER = O, 5, point(13, 0), point(5, 0), point(-5, 0), point(Q(25, 13), Q(60, 13))
OFFSET = O, 5, point(5, 3), point(4, 3), point(-4, 3), point(5, 0)


if __name__ == "__main__":
    for label, spec in [("diameter example", DIAMETER), ("offset example", OFFSET)]:
        print(label, verify(*spec))
    print("finite sweep (two circle positions/scales):", sweep())
