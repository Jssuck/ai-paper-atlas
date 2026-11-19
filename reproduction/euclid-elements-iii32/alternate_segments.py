"""Exact educational model of Euclid III.32; requires only Python stdlib."""
from fractions import Fraction
from itertools import permutations

B, O, D, A, C, F, E = (0, 0), (0, 5), (4, 2), (0, 10), (3, 1), (1, 0), (-1, 0)


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def dot(u, v):
    return u[0]*v[0] + u[1]*v[1]


def cross(u, v):
    return u[0]*v[1] - u[1]*v[0]


def signature(u, v):
    """Angle in [0, π] as a pair proportional to (cos θ, sin θ)."""
    if u == (0, 0) or v == (0, 0):
        raise ValueError("angle requires two nonzero rays")
    return dot(u, v), abs(cross(u, v))


def equal_angles(s, t):
    """Same oriented half-line in descriptor space, not merely collinear."""
    return cross(s, t) == 0 and dot(s, t) > 0


def audit(o, b, d, p, t):
    """Return separate premise and conclusion checks; t is a vector."""
    radius = sub(b, o)
    r2 = dot(radius, radius)
    chord, to_p = sub(d, b), sub(p, b)
    dp = sub(d, p)
    same_circle = r2 > 0 and all(dot(sub(q, o), sub(q, o)) == r2 for q in (d, p))
    distinct = len({b, d, p}) == 3
    tangent = t != (0, 0) and dot(radius, t) == 0
    opposite = cross(chord, to_p)*cross(chord, t) < 0
    comparable = distinct and t != (0, 0)
    pair = (signature(t, chord), signature(sub(b, p), dp)) if comparable else None
    return {"same_circle": same_circle, "distinct": distinct, "tangent": tangent,
            "opposite": opposite, "pair": pair,
            "equal": equal_angles(*pair) if comparable else None}


def confirm(condition, label):
    if not condition:
        raise RuntimeError(label)


def rational_arc(radius, parameter):
    """Circle centered at (0,r), parametrized through its bottom point."""
    if parameter is None:
        return 0, 2*radius
    q = Fraction(parameter)
    return (2*radius*q/(1+q*q), 2*radius*q*q/(1+q*q))


def finite_sweep():
    params = sorted({Fraction(a, b) for a in range(-6, 7) for b in range(1, 7)} - {0}) + [None]
    rays = (E, F)
    expected, same_side, mismatch, right = 0, 0, 0, 0
    for radius in (1, 5):
        points = [rational_arc(radius, q) for q in params]
        for d, p in permutations(points, 2):
            for t in rays:
                result = audit((0, radius), B, d, p, t)
                confirm(all(result[key] for key in ("same_circle", "distinct", "tangent")),
                        "unexpected incidence or tangent")
                if result["opposite"]:
                    confirm(result["equal"], "alternate-side angle mismatch")
                    expected += 1
                    right += d == (0, 2*radius)
                else:
                    same_side += 1
                    mismatch += not result["equal"]
    confirm(expected == same_side, "one tangent ray per arc point")
    confirm(same_side - mismatch == right, "only diameter is equal on same side")
    return len(params), expected, same_side, mismatch, right


def main():
    for label, p, t in (("F and A", A, F), ("E and C", C, E),
                         ("F and C, wrong side", C, F),
                         ("non-tangent ray and A", A, C)):
        print(label, audit(O, B, D, p, t))
    for t, p in ((F, (-5, 5)), (E, (5, 5))):
        print("diameter", audit(O, B, A, p, t))
    n, good, same, bad, right = finite_sweep()
    print(f"points per radius: {n}; radii: 2; tested triples (D,P,T): {good+same}")
    print(f"alternate-side equal: {good}; of these diameter cases: {right}")
    print(f"same-side controls: {same}; unequal: {bad}; diameter equal: {same-bad}")


if __name__ == "__main__":
    main()
