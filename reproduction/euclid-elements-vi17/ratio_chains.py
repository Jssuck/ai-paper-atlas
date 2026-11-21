"""Exact rational coordinate reconstruction of Euclid VI.17."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

Q = Fraction
Point = tuple[Q, Q]
Rectangle = tuple[Point, Point, Point, Point]


def _length(value: int | Q) -> Q:
    if type(value) not in (int, Q):
        raise TypeError("length must be an int or Fraction")
    result = Q(value)
    if result <= 0:
        raise ValueError("length must be positive")
    return result


def _rectangle(origin: Point, width: Q, height: Q) -> Rectangle:
    x, y = origin
    return ((x, y), (x + width, y), (x + width, y + height), (x, y + height))


def polygon_area(vertices: Rectangle) -> Q:
    """Area from cyclic vertex coordinates via the shoelace formula."""
    twice_signed = sum(x * yn - y * xn
                       for (x, y), (xn, yn) in zip(vertices, vertices[1:] + vertices[:1]))
    return abs(Q(twice_signed)) / 2


@dataclass(frozen=True)
class Comparison:
    ratios: tuple[Q, Q]
    extremes: Rectangle
    middle_square: Rectangle

    @property
    def areas(self) -> tuple[Q, Q]:
        return polygon_area(self.extremes), polygon_area(self.middle_square)

    @property
    def proportional(self) -> bool:
        return self.ratios[0] == self.ratios[1]

    @property
    def equal_area(self) -> bool:
        return self.areas[0] == self.areas[1]


def compare(a: int | Q, b: int | Q, c: int | Q) -> Comparison:
    """Compare a:b=b:c against equality of rectangle AC and square B."""
    a, b, c = map(_length, (a, b, c))
    copied_middle = b
    return Comparison((a / b, copied_middle / c),
                      _rectangle((Q(-2), Q(3)), a, c),
                      _rectangle((a + Q(5), Q(-7)), b, copied_middle))


def rational_middle(a: int | Q, c: int | Q) -> Q | None:
    """Positive mean when representable as a Fraction; otherwise None."""
    square = _length(a) * _length(c)
    n, d = isqrt(square.numerator), isqrt(square.denominator)
    if n * n == square.numerator and d * d == square.denominator:
        return Q(n, d)
    return None
