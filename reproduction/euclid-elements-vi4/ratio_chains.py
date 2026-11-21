"""Exact finite coordinate checks for Euclid VI.4 (Python standard library only)."""
from fractions import Fraction as Q
from math import isqrt


def point(x, y):
    return Q(x), Q(y)


def add(u, v):
    return u[0]+v[0], u[1]+v[1]


def sub(u, v):
    return u[0]-v[0], u[1]-v[1]


def scale(k, u):
    return k*u[0], k*u[1]


def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]


def det(u, v):
    return u[0]*v[1]-u[1]*v[0]


def length2(a, b):
    v = sub(a, b)
    return Q(dot(v, v))


def length(a, b):
    n = length2(a, b)
    p, q = isqrt(n.numerator), isqrt(n.denominator)
    if p*p != n.numerator or q*q != n.denominator:
        raise ValueError("this printable length is irrational; use squared length")
    return Q(p, q)


def angle_signature(a, b, c):
    """Sign(cosine), cosine squared at b; injective for angles in [0, pi]."""
    u, v = sub(a, b), sub(c, b)
    d = dot(u, v)
    return (d > 0)-(d < 0), Q(d*d, dot(u, u)*dot(v, v))


def equal_angles(a, b, c, d, e):
    """Check A↔D, B↔C, C↔E independently of side-ratio products."""
    if not det(sub(b, a), sub(c, a)) or not det(sub(c, d), sub(e, d)):
        raise ValueError("triangles must be nondegenerate")
    return all(angle_signature(*u) == angle_signature(*v) for u, v in (
        ((b, a, c), (c, d, e)), ((a, b, c), (d, c, e)),
        ((a, c, b), (d, e, c))))


def interior(a, p, b):
    u, v = sub(p, a), sub(b, a)
    return not det(u, v) and 0 < dot(u, v) < dot(v, v)


def sratio(a, b, c, d):
    """Return square of the positive length ratio AB:CD."""
    return length2(a, b)/length2(c, d)


def audit(a, b, c, d, e):
    if not interior(b, c, e) or det(sub(c, b), sub(a, b))*det(sub(c, b), sub(d, c)) <= 0:
        raise ValueError("require B–C–E and A,D on same side")
    if not equal_angles(a, b, c, d, e):
        raise ValueError("correspondence is not equiangular")
    ba, ed = sub(a, b), sub(d, e)
    den = det(ba, ed)
    if not den:
        raise ValueError("rays do not meet at one point")
    f = add(b, scale(Q(det(sub(e, b), ed), den), ba))
    if not interior(b, a, f) or not interior(e, d, f):
        raise ValueError("require B–A–F and E–D–F")
    mids = sratio(b, c, c, e)
    cuts = (sratio(b, a, a, f), mids, sratio(f, d, d, e))
    replacements = (length2(a, f) == length2(d, c),
                    length2(f, d) == length2(a, c))
    parallel = (not det(sub(a, c), sub(f, e)),
                not det(sub(c, d), sub(b, f)))
    cross = (sratio(a, b, d, c), mids, sratio(a, c, d, e))
    chains = ((sratio(a, b, b, c), sratio(d, c, c, e)),
              (sratio(b, c, c, a), sratio(c, e, e, d)),
              (sratio(a, b, a, c), sratio(d, c, d, e)))
    return dict(f=f, cuts=cuts, replacements=replacements, parallel=parallel,
                cross=cross, chains=chains)


def require_audit(r):
    if (not all(r["parallel"]) or not all(r["replacements"])
        or len(set(r["cuts"])) != 1 or len(set(r["cross"])) != 1
        or any(a != b for a, b in r["chains"])):
        raise AssertionError(r)


A, B, C, D, E = (point(0, 3), point(0, 0), point(4, 0),
                  point(4, Q(9, 2)), point(10, 0))


def exercise_grid():
    """Construct target triangles by known homothety, then independently audit."""
    total = 0
    for b in (point(0, 0), point(2, -3), point(Q(1, 3), Q(-2, 5))):
        for u in (point(4, 0), point(3, 1), point(-1, 2)):
            for h in (Q(1, 3), Q(1), Q(3, 2), Q(5, 2)):
                for skew in (-2, 0, 1):
                    for sign in (-1, 1):
                        v = add(scale(skew, u), scale(sign, (-u[1], u[0])))
                        a, c = add(b, v), add(b, u)
                        d, e = add(c, scale(h, v)), add(c, scale(h, u))
                        r = audit(a, b, c, d, e)
                        require_audit(r)
                        if r["f"] != add(b, scale(1+h, v)) or r["cross"] != (1/h**2,)*3:
                            raise AssertionError((h, r))
                        total += 1
    return total


if __name__ == "__main__":
    print(f"grid: {exercise_grid()} exact configurations (both orientations)")
