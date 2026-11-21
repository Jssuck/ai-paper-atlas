"""Exact Cartesian teaching model for Euclid VI.2, not Euclid's own proof."""
from dataclasses import dataclass
from fractions import Fraction as Q


def rational(value):
    if type(value) not in (int, Q):
        raise TypeError("use an integer or Fraction, not an approximate coordinate")
    return Q(value)


def point(value):
    x, y = value
    return rational(x), rational(y)


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def lerp(a, b, t):
    return tuple(x + t * (y - x) for x, y in zip(a, b))


def parameter(a, b, p):
    direction = sub(b, a)
    offset = sub(p, a)
    if det(direction, offset):
        raise ValueError("cut point is not on the required supporting line")
    i = 0 if direction[0] else 1
    return offset[i] / direction[i]


@dataclass(frozen=True)
class Evidence:
    parameters: tuple
    segment_ratios: tuple
    double_areas: tuple
    area_ratios: tuple
    parallel_det: Q
    side_values: tuple

    @property
    def same_side(self):
        b, c = self.side_values
        return b * c > 0

    @property
    def forward(self):
        return self.parallel_det != 0 or self.segment_ratios[0] == self.segment_ratios[1]

    @property
    def converse(self):
        return self.segment_ratios[0] != self.segment_ratios[1] or self.parallel_det == 0


def examine(a, b, c, d, e, *, interior=True):
    """Measure unsigned ratios, actual doubled areas and signed side tests."""
    a, b, c, d, e = map(point, (a, b, c, d, e))
    if not det(sub(b, a), sub(c, a)):
        raise ValueError("ABC must be nondegenerate")
    t, s = parameter(a, b, d), parameter(a, c, e)
    if interior and not (0 < t < 1 and 0 < s < 1):
        raise ValueError("D and E must be strictly inside AB and AC")
    if t in (0, 1) or s in (0, 1):
        raise ValueError("probe excludes endpoint degeneracies")
    de = sub(e, d)
    f = det(de, sub(a, d))
    g = det(de, sub(b, d))
    h = det(de, sub(c, d))
    areas = abs(f), abs(g), abs(h)
    return Evidence(
        (t, s), (abs(1 - t) / abs(t), abs(1 - s) / abs(s)), areas,
        (areas[1] / areas[0], areas[2] / areas[0]),
        det(de, sub(c, b)), (g, h),
    )


A, B, C, D, E = (0, 0), (3, 0), (0, 3), (1, 0), (0, 1)

CASES = {
    "parallel": (A, B, C, D, E),
    "nonparallel": (A, B, C, D, (0, 2)),
    "outside": (A, B, C, (2, 0), (0, 6)),
}


def examples():
    for name, points in CASES.items():
        x = examine(*points, interior=name != "outside")
        pairs = " : ".join(map(str, x.segment_ratios))
        print(f"{name}: ratios {pairs}; doubled areas "
              f"{tuple(map(str, x.double_areas))}; det={x.parallel_det}; "
              f"same side={x.same_side}; forward={x.forward}; converse={x.converse}")


if __name__ == "__main__":
    examples()
