"""Exact-coordinate teaching reconstruction of Euclid Elements IV.6."""
from fractions import Fraction
from itertools import product


def exact_point(pair):
    x, y = pair
    if any(type(value) is not int and not isinstance(value, Fraction)
           for value in (x, y)):
        raise TypeError("coordinates must be int or Fraction")
    return Fraction(x), Fraction(y)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def subtract(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def inscribe(o, a):
    """Return A, B, C, D in boundary order from center O and boundary point A."""
    o, a = exact_point(o), exact_point(a)
    x, y = subtract(a, o)
    if x == y == 0:
        raise ValueError("the radius must be positive")
    v = -y, x
    return a, add(o, v), subtract(o, (x, y)), subtract(o, v)


def measurements(o, vertices):
    """Measure candidate vertices in order; none of these checks invokes inscribe."""
    points = tuple(map(exact_point, vertices))
    if len(points) != 4:
        raise ValueError("expected four vertices in boundary order")
    offsets = tuple(subtract(p, exact_point(o)) for p in points)
    edges = tuple(subtract(points[(i + 1) % 4], points[i]) for i in range(4))
    diagonals = subtract(points[2], points[0]), subtract(points[3], points[1])
    return {
        "radii_squared": tuple(dot(p, p) for p in offsets),
        "sides_squared": tuple(dot(e, e) for e in edges),
        "adjacent_dot": tuple(dot(edges[i], edges[(i + 1) % 4]) for i in range(4)),
        "turns": tuple(det(edges[i], edges[(i + 1) % 4]) for i in range(4)),
        "diagonals_squared": tuple(dot(d, d) for d in diagonals),
        "diagonal_dot": dot(*diagonals),
        "signed_area": sum(det(points[i], points[(i + 1) % 4]) for i in range(4)) / 2,
    }


def verify(o, a, vertices):
    """Check exact candidate against necessary invariants of the constructed square."""
    o, a = exact_point(o), exact_point(a)
    vertices = tuple(map(exact_point, vertices))
    m = measurements(o, vertices)
    radial = subtract(a, o)
    r2 = dot(radial, radial)
    if (r2 <= 0 or vertices[0] != a or len(set(vertices)) != 4
        or m["radii_squared"] != (r2,) * 4
        or m["sides_squared"] != (2 * r2,) * 4
        or m["adjacent_dot"] != (0,) * 4
        or m["turns"] != (2 * r2,) * 4
        or m["diagonals_squared"] != (4 * r2,) * 2
        or m["diagonal_dot"] != 0
        or m["signed_area"] != 2 * r2):
        raise ValueError("candidate violates IV.6 teaching invariants")
    return m


def grid_sweep():
    """Three distinct rational centers times 120 nonzero rational directions."""
    accepted = rejected = 0
    for o in ((0, 0), (Fraction(1, 2), Fraction(-1, 3)),
              (Fraction(-7, 4), Fraction(5, 7))):
        for x, y in product(range(-5, 6), repeat=2):
            a = add(o, (Fraction(x, 3), Fraction(y, 5)))
            if (x, y) == (0, 0):
                try:
                    inscribe(o, a)
                except ValueError:
                    rejected += 1
                else:
                    raise RuntimeError("zero-radius circle was accepted")
                continue
            verify(o, a, inscribe(o, a))
            accepted += 1
    return accepted, rejected


def rectangle_control():
    """Two equal-length but nonperpendicular diameters yield a nonsquare rectangle."""
    return (5, 0), (3, 4), (-5, 0), (-3, -4)


if __name__ == "__main__":
    o = Fraction(1, 2), Fraction(-1, 3)
    a = add(o, (2, 1))
    vertices = inscribe(o, a)
    print("O:", tuple(map(str, o)))
    print("A, B, C, D:", [tuple(map(str, v)) for v in vertices])
    m = verify(o, a, vertices)
    print("r^2, side^2, diagonal^2, area:",
          *(str(x) for x in (m["radii_squared"][0], m["sides_squared"][0],
                             m["diagonals_squared"][0], m["signed_area"])))
    m = measurements((0, 0), rectangle_control())
    print("nonperpendicular control: sides^2=", tuple(map(int, m["sides_squared"])),
          "adjacent dot=", tuple(map(int, m["adjacent_dot"])))
    accepted, rejected = grid_sweep()
    print(f"rational grid: accepted={accepted}, zero-radius rejected={rejected}")
