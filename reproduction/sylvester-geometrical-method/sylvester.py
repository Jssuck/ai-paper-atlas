"""Original standard-library reconstruction of selected Sylvester (1852) equations.

Angles supplied to the public geometry API are in degrees. No universal statement
about which proof methods are possible is implemented or inferred.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import cos, hypot, isfinite, pi, radians, sin, sqrt, tan
from typing import Callable

EPS = 1e-12


class DomainError(ValueError):
    """An input is outside the explicitly supported mathematical domain."""


class DegenerateIntersection(DomainError):
    """A dividing line is parallel to, or coincident with, its target line."""


def positive(value: float, name: str) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0:
        raise DomainError(f"{name} must be finite and strictly positive")
    return value


@dataclass(frozen=True)
class Triangle:
    """Nondegenerate triangle, A=(0,0), B=(base,0), C above the base."""

    A_deg: float
    B_deg: float
    base: float = 1.0

    def __post_init__(self) -> None:
        for name in ("A_deg", "B_deg", "base"):
            object.__setattr__(self, name, positive(getattr(self, name), name))
        if self.A_deg + self.B_deg >= 180:
            raise DomainError("A+B must be strictly smaller than 180 degrees")

    @property
    def A(self) -> float:
        return radians(self.A_deg)

    @property
    def B(self) -> float:
        return radians(self.B_deg)

    @property
    def C(self) -> tuple[float, float]:
        AC = self.base * sin(self.B) / sin(self.A + self.B)
        return (AC * cos(self.A), AC * sin(self.A))


def valid_n(n: float) -> float:
    n = float(n)
    if not isfinite(n) or n == 0:
        raise DomainError("n must be finite and nonzero")
    return n


def parameters(triangle: Triangle, n: float) -> tuple[float, float, float, float]:
    """Return alpha, beta, theta=A/n, phi=B/n in radians, without reduction mod pi."""
    n = valid_n(n)
    theta, phi = triangle.A / n, triangle.B / n
    if not isfinite(theta) or not isfinite(phi):
        raise DomainError("the chosen n overflows the angle representation")
    return theta / 2, phi / 2, theta, phi


def sine_residual(triangle: Triangle, n: float) -> float:
    """Page 367 left ratio minus right ratio; NOT an existence test for cevians."""
    _, _, theta, phi = parameters(triangle, n)
    return sin(triangle.A + phi) / sin(triangle.A) - sin(triangle.B + theta) / sin(triangle.B)


def cross_residual(triangle: Triangle, n: float) -> float:
    """The division-free sine equation; can vanish for parallel intersections."""
    _, _, theta, phi = parameters(triangle, n)
    return sin(triangle.A + phi) * sin(triangle.B) - sin(triangle.B + theta) * sin(triangle.A)


def checked_tan(angle: float) -> float:
    if abs(cos(angle)) <= EPS:
        raise DomainError("tangent has a pole (or is within numerical tolerance)")
    return tan(angle)


def tangent_ratios(triangle: Triangle, n: float) -> tuple[float, float]:
    """Page 367 tangent ratios on their smaller, explicitly checked domain.

    At A=B the first ratio is 0/0; the original sine equation remains meaningful.
    Clearing these divisions and then forgetting their domain is not allowed.
    """
    alpha, beta, _, _ = parameters(triangle, n)
    d, s = alpha - beta, alpha + beta
    ld, rd = checked_tan(n * d), checked_tan(n * s)
    if abs(ld) <= EPS or abs(rd) <= EPS:
        raise DomainError("a tangent ratio denominator vanishes")
    return checked_tan((n - 1) * d) / ld, checked_tan((n + 1) * s) / rd


@dataclass(frozen=True)
class DividerGeometry:
    triangle: Triangle
    n: float
    theta: float
    phi: float
    t_A: float
    t_B: float
    D: tuple[float, float]
    E: tuple[float, float]
    bc_fraction: float
    ac_fraction: float

    @property
    def ordinary_lengths(self) -> tuple[float, float]:
        return abs(self.t_A), abs(self.t_B)

    @property
    def both_forward_rays(self) -> bool:
        return self.t_A > 0 and self.t_B > 0

    @property
    def both_internal_cevians(self) -> bool:
        return (self.both_forward_rays and 0 < self.theta < self.triangle.A
                and 0 < self.phi < self.triangle.B
                and 0 < self.bc_fraction < 1 and 0 < self.ac_fraction < 1)

    def as_dict(self) -> dict:
        result = asdict(self)
        result["ordinary_lengths"] = list(self.ordinary_lengths)
        result["both_forward_rays"] = self.both_forward_rays
        result["both_internal_cevians"] = self.both_internal_cevians
        result["sine_residual"] = sine_residual(self.triangle, self.n)
        return result


def divider_geometry(triangle: Triangle, n: float) -> DividerGeometry:
    """Intersect the two supporting lines and preserve their signed parameters.

    A+t_A(cos theta,sin theta) lies on BC;
    B+t_B(-cos phi,sin phi) lies on AC.
    A negative parameter is not a point on the chosen forward ray. Ordinary
    segment lengths are abs(t_A), abs(t_B), whose equality has two sign branches.
    """
    _, _, theta, phi = parameters(triangle, n)
    den_A, den_B = sin(triangle.B + theta), sin(triangle.A + phi)
    if abs(den_A) <= EPS or abs(den_B) <= EPS:
        raise DegenerateIntersection("a divider and its target are parallel/coincident or numerically near-parallel")
    t_A = triangle.base * sin(triangle.B) / den_A
    t_B = triangle.base * sin(triangle.A) / den_B
    D = (t_A * cos(theta), t_A * sin(theta))
    E = (triangle.base - t_B * cos(phi), t_B * sin(phi))
    C = triangle.C
    bc = (C[0] - triangle.base, C[1])
    dc = (D[0] - triangle.base, D[1])
    bc_fraction = (bc[0] * dc[0] + bc[1] * dc[1]) / (bc[0] ** 2 + bc[1] ** 2)
    ac_fraction = (C[0] * E[0] + C[1] * E[1]) / (C[0] ** 2 + C[1] ** 2)
    return DividerGeometry(triangle, float(n), theta, phi, t_A, t_B, D, E, bc_fraction, ac_fraction)


def validate_sides(a: float, b: float, c: float) -> tuple[float, float, float]:
    a, b, c = positive(a, "a"), positive(b, "b"), positive(c, "c")
    scale = max(a, b, c)
    aa, bb, cc = a / scale, b / scale, c / scale
    if min(aa + bb - cc, aa + cc - bb, bb + cc - aa) <= 0:
        raise DomainError("strict triangle inequalities are required")
    return a, b, c


def bisector_squares(a: float, b: float, c: float) -> tuple[float, float]:
    """Internal bisectors from A and B; a=BC, b=AC, c=AB."""
    a, b, c = validate_sides(a, b, c)
    scale = max(a, b, c)
    aa, bb, cc = a / scale, b / scale, c / scale
    x = (bb * cc * (1 - (aa / (bb + cc)) ** 2) * scale) * scale
    y = (aa * cc * (1 - (bb / (aa + cc)) ** 2) * scale) * scale
    if not all(isfinite(v) and v > 0 for v in (x, y)):
        raise DomainError("squared bisector lengths are outside floating-point representability")
    return x, y


def factor_polynomial(a, b, c):
    """Positive-coefficient polynomial; accepts Fraction for exact tests."""
    return a*a*b + a*b*b + 3*a*b*c + a*c*c + b*c*c + c*c*c


def factored_bisector_difference(a: float, b: float, c: float) -> float:
    a, b, c = validate_sides(a, b, c)
    scale = max(a, b, c)
    aa, bb, cc = a / scale, b / scale, c / scale
    normalized = ((bb - aa) * cc * (aa + bb + cc) * factor_polynomial(aa, bb, cc)
                  / ((aa + cc) ** 2 * (bb + cc) ** 2))
    value = (normalized * scale) * scale
    if not isfinite(value) or (normalized != 0 and value == 0):
        raise DomainError("squared difference is outside floating-point representability")
    return value


def near_segment(remote: float, half_chord: float) -> float:
    """Unique positive root of x²+remote*x=half_chord², for both inputs > 0.

    half_chord means the chord of HALF THE ARC, b=PU=PV, not half of UV.
    Scaling and rationalization reduce avoidable cancellation. The equation alone
    does not encode every incidence restriction of a fixed circle and base chord.
    """
    a, b = positive(remote, "remote"), positive(half_chord, "half_chord")
    if a >= b:
        ratio = b / a
        x = b * (2 * ratio / (hypot(1, 2 * ratio) + 1))
    else:
        ratio = a / b
        x = b * (2 / (hypot(ratio, 2) + ratio))
    if not isfinite(x) or x <= 0:
        raise DomainError("positive root cannot be represented at this floating-point scale")
    return x


def remote_segment(near: float, half_chord: float) -> float:
    """Converse p369: a(a+x)=b². A positive remote segment needs 0<a<b.

    half_chord is the chord of half the arc, b=PU=PV, not half of UV."""
    a, b = positive(near, "near"), positive(half_chord, "half_chord")
    if a >= b:
        raise DomainError("positive remote segment requires near < half_chord")
    ratio = a / b
    if ratio == 0:
        raise DomainError("positive remote segment is outside floating-point representability")
    value = ((b - a) * (1 + ratio)) / ratio
    if not isfinite(value) or value <= 0:
        raise DomainError("positive remote segment is outside floating-point representability")
    return value


def circle_chord(theta_deg: float) -> dict:
    """Unit circle example: P=(0,1), base y=1/2, |theta|<60 degrees.

    P is the midpoint of the minor arc between U=(-sqrt(3)/2,1/2) and
    V=(sqrt(3)/2,1/2). The chord PQ meets UV in S. near=PS, remote=SQ.
    """
    theta_deg = float(theta_deg)
    if not isfinite(theta_deg) or abs(theta_deg) >= 60:
        raise DomainError("this fixed-circle construction requires |theta| < 60 degrees")
    theta = radians(theta_deg)
    direction = (sin(theta), -cos(theta))
    x = 0.5 / cos(theta)
    total = 2 * cos(theta)
    return {"theta_deg": theta_deg, "P": (0.0, 1.0),
            "S": (x * direction[0], 1 + x * direction[1]),
            "Q": (total * direction[0], 1 + total * direction[1]),
            "near": x, "remote": total - x, "half_chord": 1.0}


def bisect_root(function: Callable[[float], float], lo: float, hi: float, steps: int = 80) -> float:
    """Deterministic bracketed approximation, not a certificate of a universal claim."""
    fl, fh = function(lo), function(hi)
    if not isfinite(fl) or not isfinite(fh) or fl * fh > 0:
        raise DomainError("root finder needs finite opposite-sign endpoint values")
    if fl == 0:
        return lo
    if fh == 0:
        return hi
    for _ in range(steps):
        mid = (lo + hi) / 2
        fm = function(mid)
        if not isfinite(fm):
            raise DomainError("root finder encountered a non-finite interior value")
        if fm == 0 or mid in (lo, hi):
            return mid
        if fl * fm <= 0:
            hi = mid
        else:
            lo, fl = mid, fm
    return (lo + hi) / 2


def opposite_sign_example() -> DividerGeometry:
    """n=-2 example with equal absolute, but opposite signed, divider lengths."""
    A = pi / 2
    def function(B_deg):
        B = radians(B_deg)
        return sin(B) * sin(A - B / 2) + sin(A) * sin(B - A / 2)
    B_deg = bisect_root(function, 1, 44)
    return divider_geometry(Triangle(90, B_deg), -2)


def exact_opposite_sign_example() -> DividerGeometry:
    """Exact-angle unsigned extension case: n=-2, A=96°, B=24°, t_A=-1,t_B=1.

    sin(B-A/2)=sin(-24°); sin(A-B/2)=sin84°=sin96°.
    The returned coordinates still use ordinary floating-point trigonometry.
    """
    return divider_geometry(Triangle(96,24),-2)
