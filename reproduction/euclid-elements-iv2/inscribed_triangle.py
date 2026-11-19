"""Exact coordinate teaching reconstruction of Elements IV.2."""
from fractions import Fraction as Q
from itertools import product


def pt(p):
    x, y = p
    if not all(isinstance(v, (int, Q)) and not isinstance(v, bool) for v in (x, y)):
        raise TypeError("use integers or Fraction for coordinates")
    return Q(x), Q(y)


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def triangle(points):
    a, b, c = map(pt, points)
    if not det(sub(b, a), sub(c, a)):
        raise ValueError("triangle must be noncollinear")
    return a, b, c


def radius(r):
    r, _ = pt((r, 0))
    if r <= 0:
        raise ValueError("radius must be positive")
    return r


def angle_pair(vertex, p, q):
    """(dot, |cross|) encodes an angle in (0, pi) up to positive scale."""
    a, b = sub(p, vertex), sub(q, vertex)
    c = abs(det(a, b))
    if not c:
        raise ValueError("non-straight interior angle required")
    return dot(a, b), c


def angle_keys(points):
    """Unique angle keys cot(theta); negative for obtuse, 0 for right."""
    a, b, c = triangle(points)
    pairs = (angle_pair(a, b, c), angle_pair(b, a, c), angle_pair(c, a, b))
    return tuple(d / k for d, k in pairs)


def second_hit(r, q):
    """Circle x²+(y-r)²=r²; origin and a distinct forward hit."""
    r = radius(r)
    x, y = q = pt(q)
    if y <= 0:
        raise ValueError("ray must point into circle's half-plane")
    t = 2 * r * y / dot(q, q)
    return t * x, t * y


def inscribe(def_points, r):
    d, e, f = triangle(def_points)
    r = radius(r)
    ec, es = angle_pair(e, d, f)
    fc, fs = angle_pair(f, d, e)
    a = Q(0), Q(0)
    b = second_hit(r, (-fc, fs))
    c = second_hit(r, (ec, es))
    return a, b, c


def verifies(def_points, abc_points, r):
    """Check fixed anchoring, circle incidence, and labeled angles, not rays."""
    r = radius(r)
    want = angle_keys(def_points)
    try:
        abc = triangle(abc_points)
    except ValueError:
        return False
    if abc[0] != (0, 0):
        return False
    if not all(x*x + (y-r)*(y-r) == r*r for x, y in abc):
        return False
    return angle_keys(abc) == want


OBTUSE = ((-1, 2), (0, 0), (4, 0))


def sweep():
    """Small deterministic integer-grid inputs at two rational radii."""
    counts = {"acute": 0, "right": 0, "obtuse": 0, "degenerate": 0}
    points = list(product(range(-2, 3), repeat=2))
    for r, d, f in product((Q(1, 3), Q(5)), points, points):
        template = d, (0, 0), f
        try:
            keys = angle_keys(template)
        except ValueError:
            counts["degenerate"] += 1
            continue
        target = inscribe(template, r)
        if not verifies(template, target, r):
            raise AssertionError("constructed triangle failed independent checks")
        kind = "obtuse" if min(keys) < 0 else "right" if min(keys) == 0 else "acute"
        counts[kind] += 1
    return counts


if __name__ == "__main__":
    abc = inscribe(OBTUSE, 5)
    print("obtuse labeled example A,B,C:", abc)
    print("D,E,F angle cotangents:", angle_keys(OBTUSE))
    print("A,B,C angle cotangents:", angle_keys(abc))
    print("valid:", verifies(OBTUSE, abc, 5), "| swap B,C:",
          verifies(OBTUSE, (abc[0], abc[2], abc[1]), 5))
    print("finite sweep:", sweep())
