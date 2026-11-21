"""Exact rational coordinate reconstruction of Euclid VI.15."""
from dataclasses import dataclass
from fractions import Fraction as Q


def exact(v):
    if isinstance(v, bool) or not isinstance(v, (int, Q)):
        raise TypeError("supply exact int or Fraction values")
    return Q(v)


def vector(values):
    a, b = values
    return exact(a), exact(b)


def scale(k, u):
    return tuple(k * t for t in u)


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


@dataclass(frozen=True)
class Evidence:
    abc_vertices: tuple
    ade_vertices: tuple
    bad_vertices: tuple
    area_abc: Q
    area_ade: Q
    area_bad: Q
    ratio_ca_ad: Q
    ratio_ea_ab: Q

    @property
    def equal_areas(self):
        return self.area_abc == self.area_ade

    @property
    def reciprocal_sides(self):
        return self.ratio_ca_ad == self.ratio_ea_ab


def reconstruct(x, y, z, w, u=(1, 0), v=(0, 1)):
    """A=0, C=xu, D=-yu, B=zv, E=-wv; four positive coefficients."""
    x, y, z, w = map(exact, (x, y, z, w))
    if min(x, y, z, w) <= 0:
        raise ValueError("each segment coefficient must be positive")
    u, v = vector(u), vector(v)
    k = abs(det(u, v))
    if not k:
        raise ValueError("the directions must be noncollinear")
    a = (Q(0), Q(0))
    b, c, d, e = scale(z, v), scale(x, u), scale(-y, u), scale(-w, v)
    return Evidence(
        (a, b, c), (a, d, e), (b, a, d),
        x * z * k / 2, y * w * k / 2, y * z * k / 2, x / y, w / z,
    )
