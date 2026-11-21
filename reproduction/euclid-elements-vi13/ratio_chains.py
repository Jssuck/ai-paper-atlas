"""Exact coordinate reconstruction of Euclid VI.13, not the ancient proof."""

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

Rational = int | Fraction


def _positive(value: Rational) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("lengths must be int or Fraction")
    x = Fraction(value)
    if x <= 0:
        raise ValueError("lengths must be positive")
    return x


@dataclass(frozen=True)
class Certificate:
    left: Fraction
    right: Fraction
    center_x: Fraction
    radius: Fraction
    altitude_squared: Fraction

    @property
    def right_angle_dot(self) -> Fraction:
        """Dot product (A-D)·(C-D), valid even for irrational D_y."""
        return (-self.left) * self.right + self.altitude_squared

    @property
    def rational_altitude(self) -> Fraction | None:
        """Positive height if rational; None means irrational, not absent."""
        n, d = self.altitude_squared.as_integer_ratio()
        p, q = isqrt(n), isqrt(d)
        return Fraction(p, q) if (p*p, q*q) == (n, d) else None


def construct(left: Rational, right: Rational) -> Certificate:
    """Intersect the vertical through B with the upper semicircle on AC."""
    a, b = _positive(left), _positive(right)
    center = (b - a) / 2
    radius = (a + b) / 2
    return Certificate(a, b, center, radius, radius**2 - center**2)
