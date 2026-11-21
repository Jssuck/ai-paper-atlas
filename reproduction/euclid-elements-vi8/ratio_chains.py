"""Exact rational projection and angle/side witnesses for Euclid VI.8."""
from fractions import Fraction as Q


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b, strict=True))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def dist2(a, b):
    return dot(sub(a, b), sub(a, b))


def point(p):
    x, y = p
    if any(type(v) not in (int, Q) for v in (x, y)):
        raise TypeError("coordinates must be integers or fractions")
    return Q(x), Q(y)


def projection(a, b, c):
    """Orthogonal projection of A onto the line BC and its affine parameter."""
    a, b, c = map(point, (a, b, c))
    u = sub(c, b)
    denom = dot(u, u)
    if not denom:
        raise ValueError("B and C must differ")
    t = dot(sub(a, b), u) / denom
    return tuple(x + t * v for x, v in zip(b, u, strict=True)), t


def angle_key(origin, a, b):
    """Sign and squared cosine distinguish all angles in [0, pi]."""
    u, v = sub(a, origin), sub(b, origin)
    d = dot(u, v)
    return (d > 0) - (d < 0), Q(d * d, dot(u, u) * dot(v, v))


def angles(tri):
    return tuple(angle_key(tri[i], tri[(i + 1) % 3], tri[(i + 2) % 3])
                 for i in range(3))


def sides2(tri):
    return tuple(dist2(tri[i], tri[(i + 1) % 3]) for i in range(3))


def compare(first, second):
    u, v = sides2(first), sides2(second)
    return angles(first) == angles(second), all(a * v[0] == b * u[0]
                                                 for a, b in zip(u, v, strict=True))


def witnesses(a, b, c):
    a, b, c = map(point, (a, b, c))
    foot, t = projection(a, b, c)
    if dot(sub(b, a), sub(c, a)) or a in (b, c):
        raise ValueError("A must be the nondegenerate right vertex")
    if not (0 < t < 1):
        raise ArithmeticError("right-triangle projection must be interior")
    large, left, right = (a, b, c), (foot, b, a), (foot, a, c)
    similarity = tuple(compare(first, second) for first, second in
                       ((large, left), (large, right), (left, right)))
    bc2, bd2, dc2 = dist2(b, c), dist2(b, foot), dist2(foot, c)
    identities2 = ((dist2(a, foot)**2, bd2 * dc2),
                   (dist2(a, b)**2, bc2 * bd2),
                   (dist2(a, c)**2, bc2 * dc2))
    return foot, t, similarity, identities2


def sweep():
    count = mirrors = 0
    for origin in [(0, 0), (7, -3), (Q(1, 2), Q(2, 3))]:
        x, y = origin
        for u, v in [(1, 0), (0, 1), (1, 2), (3, -2)]:
            for b in [Q(1), Q(3, 2), Q(2)]:
                for c in [Q(2, 3), Q(1), Q(4)]:
                    for flip in [-1, 1]:
                        B = x + b*u, y + b*v
                        C = x - flip*c*v, y + flip*c*u
                        foot, t, sims, identities = witnesses(origin, B, C)
                        if (t != b*b/(b*b+c*c) or dot(sub(foot, origin), sub(C, B)) != 0
                                or sims != ((True, True),)*3
                                or any(l != r for l, r in identities)):
                            raise ArithmeticError("VI.8 mismatch")
                        count += 1
                        mirrors += flip < 0
    return count, mirrors, count*3, count*3
