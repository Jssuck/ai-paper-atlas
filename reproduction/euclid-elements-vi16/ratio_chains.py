"""Exact rational coordinate reconstruction of Euclid VI.16."""
from dataclasses import dataclass
from fractions import Fraction

Q = Fraction
Point = tuple[Q, Q]
Rectangle = tuple[Point, Point, Point, Point]


def _length(value: int | Q) -> Q:
    if type(value) not in (int, Q):
        raise TypeError("length must be an int or Fraction")
    value = Q(value)
    if value <= 0:
        raise ValueError("length must be positive")
    return value


def _rectangle(origin: Point, width: Q, height: Q) -> Rectangle:
    x, y = origin
    return ((x, y), (x + width, y), (x + width, y + height), (x, y + height))


def polygon_area(vertices: Rectangle) -> Q:
    """Use the shoelace formula on actual cyclic vertices, not dimensions."""
    twice_signed = sum(x * yn - y * xn
                       for (x, y), (xn, yn) in zip(vertices, vertices[1:] + vertices[:1]))
    return abs(Q(twice_signed)) / 2


@dataclass(frozen=True)
class Comparison:
    ratios: tuple[Q, Q]
    extremes: Rectangle
    means: Rectangle

    @property
    def areas(self) -> tuple[Q, Q]:
        return polygon_area(self.extremes), polygon_area(self.means)

    @property
    def proportional(self) -> bool:
        return self.ratios[0] == self.ratios[1]

    @property
    def equal_area(self) -> bool:
        outer, inner = self.areas
        return outer == inner


def compare(a: int | Q, b: int | Q, c: int | Q, d: int | Q) -> Comparison:
    """Compare a:b and c:d; first rectangle is a by d, second b by c."""
    a, b, c, d = map(_length, (a, b, c, d))
    return Comparison((a / b, c / d),
                      _rectangle((Q(-2), Q(3)), a, d),
                      _rectangle((a + Q(5), Q(-7)), b, c))
