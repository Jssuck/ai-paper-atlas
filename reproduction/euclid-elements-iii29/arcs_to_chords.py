"""Euclid III.29 teaching model: input the specified arc, then join its endpoints."""
from dataclasses import dataclass
from fractions import Fraction
from math import cos, isfinite, sin, tau


@dataclass(frozen=True)
class Arc:
    radius: Fraction
    sweep: Fraction  # positive, counterclockwise turns; distinguishes minor and major
    start: Fraction = Fraction(0)
    center: tuple = (0, 0)

    def __post_init__(self):
        if not isinstance(self.center, tuple) or len(self.center) != 2:
            raise ValueError("center must be a two-coordinate tuple")
        for q in (self.radius, self.sweep, self.start, *self.center):
            if isinstance(q, bool) or not isinstance(q, (int, Fraction)):
                raise TypeError("use rational inputs, not floating point")
        if self.radius <= 0 or not (0 < self.sweep < 1):
            raise ValueError("radius must be positive and sweep must lie between 0 and 1")
        if not all(isfinite(float(q)) for q in (self.radius, *self.center)):
            raise ValueError("coordinates must convert to finite floats")

    def endpoints(self):
        def world(t):
            a = tau * float(t % 1)
            r = float(self.radius)
            return (float(self.center[0]) + r*cos(a),
                    float(self.center[1]) + r*sin(a))
        return world(self.start), world(self.start+self.sweep)

    def coordinate_chord2(self):
        a, b = self.endpoints()
        return (a[0]-b[0])**2 + (a[1]-b[1])**2

    def trigonometric_chord2(self):
        # Half-angle form of 2*r*r*(1-cos(tau*sweep)); avoids subtraction near zero.
        return (2*float(self.radius)*sin(tau*float(self.sweep)/2))**2

    def exact_quarter_grid_chord2(self):
        """An exact axis-point witness at integer multiples of one quarter turn."""
        def direction(t):
            q = Fraction(4*t)
            if q.denominator != 1:
                raise ValueError("axis witness only supports multiples of a quarter turn")
            return ((1, 0), (0, 1), (-1, 0), (0, -1))[q.numerator % 4]
        a, b = direction(self.start), direction(self.start+self.sweep)
        r = Fraction(self.radius)
        return sum((r*(x-y))**2 for x, y in zip(a, b))


def pair_grid():
    for r in (Fraction(1, 2), Fraction(5, 3), Fraction(7)):
        for k in range(1, 32):
            sweep = Fraction(k, 32)
            a = Arc(r, sweep, Fraction(1, 7), (3, -2))
            for t in range(-6, 7):
                b = Arc(r, sweep, Fraction(t, 13), (-4, Fraction(7, 3)))
                yield a, b


def unequal_radius_equal_length():
    # Length = tau*r*s, hence equal lengths can be checked exactly in units of tau.
    return Arc(Fraction(1), Fraction(1, 2)), Arc(Fraction(2), Fraction(1, 4))
