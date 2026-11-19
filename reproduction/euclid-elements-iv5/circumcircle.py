"""Euclid IV.5, reconstructed with exact signed determinants in the plane."""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, permutations, product


def point(p):
    x, y = p
    if any(isinstance(v, bool) or not isinstance(v, (int, Q)) for v in (x, y)):
        raise TypeError("coordinates must be int or Fraction")
    return Q(x), Q(y)


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


@dataclass(frozen=True)
class Circle:
    center: tuple[Q, Q]
    radius_squared: Q
    location: str
    angle_type: str
    # (A, B, C) order; sign invariant under orientation reversal.
    barycentric: tuple[Q, Q, Q]
    right_vertex: int | None  # zero-based; absent for nonright triangles


def circumcircle(a, b, c):
    """Solve relative to A; no roots, slopes, rounding, or tolerance."""
    a, b, c = map(point, (a, b, c))
    u, v = sub(b, a), sub(c, a)
    cross = det(u, v)
    if cross == 0:
        raise ValueError("three noncollinear vertices are required")

    # Expand |z|² = |z-u|² = |z-v|², then use Cramer's rule.
    uu, vv = dot(u, u), dot(v, v)
    bu, cv = uu / 2, vv / 2
    z = ((bu * v[1] - u[1] * cv) / cross,
         (u[0] * cv - bu * v[0]) / cross)
    o = (a[0] + z[0], a[1] + z[1])
    r2 = dot(z, z)
    lb, lc = det(z, v) / cross, det(u, z) / cross
    bary = (1 - lb - lc, lb, lc)
    location = ("outside" if min(bary) < 0 else
                "on_side" if min(bary) == 0 else "inside")

    # Independent checks of circle and position: distances, area formula,
    # and dot products at the three input vertices.
    vv_bc = dot(sub(c, b), sub(c, b))
    if not r2 > 0 or any(dot(w, w) != r2 for w in (sub(o, b), sub(o, c))):
        raise ArithmeticError("squared distance certificate failed")
    if 4 * cross * cross * r2 != uu * vv * vv_bc:
        raise ArithmeticError("area/radius certificate failed")
    turns = tuple(dot(sub(y, x), sub(w, x)) for x, y, w in
                  ((a, b, c), (b, c, a), (c, a, b)))
    least = min(turns)
    angle_type = "obtuse" if least < 0 else "right" if least == 0 else "acute"
    if location != {"acute": "inside", "right": "on_side", "obtuse": "outside"}[angle_type]:
        raise ArithmeticError("center location disagrees with angle type")
    if any((x > 0) - (x < 0) != (y > 0) - (y < 0) for x, y in zip(bary, turns)):
        raise ArithmeticError("labeled side/angle certificate failed")

    right_vertex = None
    if angle_type == "right":
        right_vertex = turns.index(0)
        p, q = (p for i, p in enumerate((a, b, c)) if i != right_vertex)
        midpoint = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        if o != midpoint or bary[right_vertex] != 0:
            raise ArithmeticError("right circle is not at the finite hypotenuse midpoint")
    return Circle(o, r2, location, angle_type, bary, right_vertex)


def grid():
    """Deterministic finite grid, each unordered base pair checked in all six labelings."""
    origin = (0, 0)
    points = [p for p in product(range(-2, 3), repeat=2) if p != origin]
    counts = dict(acute=0, right=0, obtuse=0, degenerate=0)
    right_labels = [0, 0, 0]
    for b, c in combinations(points, 2):
        tri = (origin, b, c)
        if det(b, c) == 0:
            for labels in permutations(tri):
                try:
                    circumcircle(*labels)
                except ValueError:
                    counts["degenerate"] += 1
                else:
                    raise ArithmeticError("collinear grid case accepted")
            continue
        reference = circumcircle(*tri)
        for labels in permutations(tri):
            obtained = circumcircle(*labels)
            if (obtained.center, obtained.radius_squared, obtained.location) != (
                reference.center, reference.radius_squared, reference.location
            ):
                raise ArithmeticError("circle changed after relabeling")
            counts[obtained.angle_type] += 1
            if obtained.right_vertex is not None:
                right_labels[obtained.right_vertex] += 1
    return counts, tuple(right_labels)


if __name__ == "__main__":
    counts, right_labels = grid()
    print(f"fixed-origin grid; 276 base pairs; labeled cases={sum(counts.values())}")
    print(counts)
    print("right-label counts (A, B, C):", right_labels)
