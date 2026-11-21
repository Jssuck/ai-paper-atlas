"""Exact rational coordinate reconstruction of Euclid VI.14."""
from dataclasses import dataclass
from fractions import Fraction


def exact(v):
    if isinstance(v, bool) or not isinstance(v, (int, Fraction)):
        raise TypeError("supply exact int or Fraction values")
    return Fraction(v)


def vector(values):
    a, b = values
    return exact(a), exact(b)


def scale(k, u):
    return tuple(k * t for t in u)


def add(u, v):
    return tuple(a + b for a, b in zip(u, v, strict=True))


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


@dataclass(frozen=True)
class Evidence:
    # Listed in cyclic order, starting at the shared vertex B.
    ab_vertices: tuple
    bc_vertices: tuple
    fe_vertices: tuple
    area_ab: Fraction
    area_bc: Fraction
    area_fe: Fraction
    ratio_db_be: Fraction
    ratio_gb_bf: Fraction

    @property
    def equal_areas(self):
        return self.area_ab == self.area_bc

    @property
    def reciprocal_sides(self):
        return self.ratio_db_be == self.ratio_gb_bf


def reconstruct(x, y, z, w, u=(1, 0), v=(0, 1)):
    """B=0, D=-xu, E=yu, F=-zv, G=wv; all four factors >0."""
    x, y, z, w = map(exact, (x, y, z, w))
    if min(x, y, z, w) <= 0:
        raise ValueError("each segment coefficient must be positive")
    u, v = vector(u), vector(v)
    jacobian = abs(det(u, v))
    if jacobian == 0:
        raise ValueError("the two directions must be noncollinear")
    b = (Fraction(0), Fraction(0))
    d, e, f, g = scale(-x, u), scale(y, u), scale(-z, v), scale(w, v)
    return Evidence(
        (b, d, add(d, f), f), (b, e, add(e, g), g), (b, e, add(e, f), f),
        x * z * jacobian, y * w * jacobian, y * z * jacobian, x / y, w / z,
    )
