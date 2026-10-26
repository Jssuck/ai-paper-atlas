"""Exact rational teaching model for Elements I.3; not a construction engine.

C denotes the *squared* target length. A certificate is a supplied radius
endpoint D and a candidate cut point E. Checking their coordinates proves no
history of ruler/compass operations and does not establish Proposition I.2.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


def rational(value):
    """Accept exact integers/Fractions only; never silently admit a float."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("use int or Fraction, not float/bool/str")
    return Fraction(value)


@dataclass(frozen=True)
class Point:
    x: Fraction
    y: Fraction

    def __post_init__(self):
        object.__setattr__(self, "x", rational(self.x))
        object.__setattr__(self, "y", rational(self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def scale(self, k):
        k = rational(k)
        return Point(k * self.x, k * self.y)


def dot(u, v):
    return u.x * v.x + u.y * v.y


def cross(u, v):
    return u.x * v.y - u.y * v.x


def norm2(u):
    return dot(u, u)


def squared_distance(a, b):
    return norm2(b - a)


def domain_status(a, b, c):
    """Strict I.3 policy; equality/zero are NOT successful strict cuts."""
    c = rational(c)
    length2 = squared_distance(a, b)
    if length2 == 0:
        return "degenerate_segment"
    if c < 0:
        return "negative_squared_length"
    if c == 0:
        return "zero_target"
    if c == length2:
        return "equal_target"
    if c > length2:
        return "longer_target"
    return "strict_cut"


@dataclass(frozen=True)
class Certificate:
    d: Point
    e: Point


@dataclass(frozen=True)
class Verification:
    domain: str
    checks: tuple

    @property
    def valid(self):
        return all(value for _, value in self.checks)

    @property
    def failures(self):
        return tuple(name for name, value in self.checks if not value)

    def as_dict(self):
        return {"domain": self.domain, "valid": self.valid,
                "checks": dict(self.checks), "failures": list(self.failures)}


def verify(a, b, c, certificate):
    """Check a rational-coordinate certificate, without taking square roots.

    I.2's length-transfer *construction* is outside this verifier. The
    supplied D is merely audited against the required squared length.
    """
    c = rational(c)
    v = b - a
    w = certificate.e - a
    length2 = norm2(v)
    ae2 = norm2(w)
    ad2 = squared_distance(a, certificate.d)
    status = domain_status(a, b, c)
    checks = (
        ("admissible_strict_input", status == "strict_cut"),
        ("supplied_AD_has_target_length", ad2 == c),
        ("E_on_circle_center_A_radius_AD", ae2 == ad2),
        ("E_on_line_AB", cross(v, w) == 0),
        ("strict_dot_bounds", 0 < dot(v, w) < length2),
        ("AE_has_target_length", ae2 == c),
    )
    return Verification(status, checks)


class RationalWitnessUnavailable(ValueError):
    """This simple witness builder deliberately does not model algebraics."""


def rational_sqrt(value):
    value = rational(value)
    if value < 0:
        raise ValueError("negative rational has no real square root")
    p, q = isqrt(value.numerator), isqrt(value.denominator)
    if p * p != value.numerator or q * q != value.denominator:
        raise RationalWitnessUnavailable("square root is not rational")
    return Fraction(p, q)


def analytic_witness(a, b, c, d=None):
    """Return an analytic witness for the rational-length subfamily.

    Computes E=A+(r/L)(B-A); this is NOT a straightedge/compass simulation.
    If D is omitted, A+(0,r) is an analytically supplied radius endpoint,
    not a reconstructed proof or execution of I.2.
    """
    c = rational(c)
    status = domain_status(a, b, c)
    if status != "strict_cut":
        raise ValueError("strict I.3 input required: " + status)
    radius = rational_sqrt(c)
    length = rational_sqrt(squared_distance(a, b))
    if d is None:
        d = a + Point(0, radius)
    if squared_distance(a, d) != c:
        raise ValueError("supplied D has incorrect squared distance from A")
    e = a + (b - a).scale(radius / length)
    return Certificate(d=d, e=e)
