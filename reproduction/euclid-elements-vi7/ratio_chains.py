"""Exact rational coordinate probes for Euclid VI.7, not a formal proof."""

from fractions import Fraction as Q


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def norm2(a):
    return dot(a, a)


def angle(a, b, c):
    u, v = sub(a, b), sub(c, b)
    d = dot(u, v)
    area = cross(u, v)
    if not area:
        raise ValueError("degenerate triangle")
    # Signed cotangent: strictly decreasing on the open interval (0, pi).
    return Q(d, abs(area))


def signature(tri):
    a, b, c = tri
    return angle(b, a, c), angle(a, b, c), angle(a, c, b)


def sides2(tri):
    a, b, c = tri
    return norm2(sub(a, b)), norm2(sub(b, c)), norm2(sub(a, c))


def compare(left, right):
    """Report each premise and two independently calculated conclusions."""
    xs, ys = signature(left), signature(right)
    x, y = sides2(left), sides2(right)
    fixed_angle = xs[0] == ys[0]
    ratio = x[0] * y[1] == y[0] * x[1]
    same_branch = (xs[2] > 0) == (ys[2] > 0)
    return (fixed_angle, ratio, same_branch, xs == ys,
            all(i * y[0] == j * x[0] for i, j in zip(x, y)))


def normalized_model(b, w, q):
    """Positive roots of |t*w-(b,0)|²=q give possible noncollinear C.

    q is BC squared. Return projection t, quadratic discriminant/4, and
    a classification; no irrational root needs to be approximated.
    """
    if b <= 0 or q <= 0 or w[1] == 0:
        raise ValueError("positive lengths and a noncollinear ray required")
    ww = norm2(w)
    p = Q(b * w[0], ww)
    delta = (b * w[0]) ** 2 - ww * (b * b - q)
    if delta < 0:
        outcome = "none"
    elif delta == 0:
        outcome = "right" if p > 0 else "none"
    elif p > 0:
        outcome = "two" if q < b * b else "one-acute"
    elif q > b * b:
        outcome = "one-acute"
    else:
        outcome = "none"
    return p, delta, outcome


def ray_point(w, t):
    return t * w[0], t * w[1]


def transform(tri, scale, mirror, shift):
    """Rational isometry (3-4-5 rotation plus optional reflection), with scale."""
    out = []
    for x, y in tri:
        if mirror:
            y = -y
        out.append((shift[0] + scale * Q(3*x - 4*y, 5),
                    shift[1] + scale * Q(4*x + 3*y, 5)))
    return tuple(out)


def ambiguity():
    return ((3, 0), (0, 0), (1, 2)), ((3, 0), (0, 0), (2, 1))


def sweep():
    """Check selected rational roots, the second root, and tangent/vacuous data."""
    same = opposite = right = vacuous = 0
    for b in (2, 3, 7):
        for w in ((1, 1), (2, 1), (3, 4), (5, -2)):
            ww = norm2(w)
            p = Q(b*w[0], ww)
            for factor in (Q(1, 4), Q(1, 2), Q(3, 4), Q(1),
                           Q(5, 4), Q(3, 2), Q(7, 4)):
                t = factor*p
                a, bp = (0, 0), (b, 0)
                tri = a, bp, ray_point(w, t)
                other = a, bp, ray_point(w, 2*p-t)
                q = sides2(tri)[1]
                center, delta, case = normalized_model(b, w, q)
                expected = "right" if factor == 1 else "two"
                if center != p or delta != (ww*(t-p))**2 or case != expected:
                    raise RuntimeError("unexpected quadratic classification")
                for k in (Q(1, 3), Q(1), Q(5, 2)):
                    for mirror in (False, True):
                        if compare(tri, transform(tri, k, mirror, (11, -7))) != (True,)*5:
                            raise RuntimeError("same-branch comparison failed")
                        same += 1
                        if factor == 1:
                            right += 1
                        elif compare(tri, transform(other, k, mirror, (11, -7))) == (
                                True, True, False, False, False):
                            opposite += 1
                        else:
                            raise RuntimeError("opposite-branch comparison failed")
            min_q = b*b - ww*p*p
            if normalized_model(b, w, min_q / 2)[2] != "none":
                raise RuntimeError("expected a negative discriminant")
            vacuous += 1
    return same, opposite, right, vacuous
