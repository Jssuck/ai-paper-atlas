"""Exact chord/angle certificates for a modern reconstruction of Elements IV.16."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd

# Phi_15(x)=x^8-x^7+x^5-x^4+x^3-x+1, ascending coefficients.
PHI15 = (1, -1, 0, 1, -1, 1, 0, -1, 1)
ZERO = (0,) * 8


def reduce_poly(coeff):
    """Canonical representative of degree < 8 in Z[x]/(Phi_15)."""
    c = list(coeff)
    c.extend([0] * max(0, 8 - len(c)))
    for j in range(len(c) - 1, 7, -1):
        lead = c[j]
        for i, ai in enumerate(PHI15):
            c[j - 8 + i] -= lead * ai
    return tuple(c[:8])


def root(k):
    """The exact algebraic value zeta**k, for zeta=e^(2*pi*i/15)."""
    return reduce_poly([0] * (k % 15) + [1])


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(a, b):
    c = [0] * 15
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return reduce_poly(c)


def twice_dot_from_exponents(center, left, right):
    """Twice the unit-circle dot product of the two vectors from center."""
    u = sub(root(left), root(center))
    v = sub(root(right), root(center))
    uc = sub(root(-left), root(-center))
    vc = sub(root(-right), root(-center))
    return add(mul(u, vc), mul(uc, v))


def chord_sq(a, b):
    return mul(sub(root(a), root(b)), sub(root(-a), root(-b)))


def half_arc(*, pentagon_direction=1, triangle_direction=1, major=False):
    """Use A=0, B=±1/5, C=±1/3, orienting the walk as the triangle.

    major=True takes the complementary arc length as the wrong-walk control;
    it does not locate the midpoint of that long arc in the walk direction.
    """
    if pentagon_direction not in (-1, 1) or triangle_direction not in (-1, 1):
        raise ValueError("orientation must be +1 or -1")
    b = Fraction(pentagon_direction, 5) % 1
    c = Fraction(triangle_direction, 3) % 1
    gap = (triangle_direction * (c - b)) % 1
    return triangle_direction * ((1 - gap) if major else gap) / 2


def step_exponent(turn):
    n = turn * 15
    if n.denominator != 1:
        raise ValueError("turn outside the 15th-root model")
    return int(n)


def walk(start, step, count=15):
    if count < 0:
        raise ValueError("negative step count")
    return tuple((start + i * step) % 15 for i in range(count + 1))


@dataclass(frozen=True)
class Certificate:
    closed: bool
    distinct: bool
    boundary_order: bool
    equal_sides: bool
    equal_angles: bool

    @property
    def regular(self):
        return all((self.closed, self.distinct, self.boundary_order,
                    self.equal_sides, self.equal_angles))


def certify(path):
    """Input exponents by definition lie on the original circle (unit scale)."""
    if len(path) != 16 or any(not 0 <= x < 15 for x in path):
        raise ValueError("expect fifteen steps encoded by sixteen residues")
    vertices = path[:-1]
    gaps = tuple((b - a) % 15 for a, b in zip(vertices, path[1:]))
    order = gaps in ((1,) * 15, (14,) * 15)
    lengths = tuple(chord_sq(a, b) for a, b in zip(vertices, path[1:]))
    # Use cyclic neighbors of the listed vertices, independently of final return.
    dots = tuple(twice_dot_from_exponents(v, vertices[i - 1],
                                        vertices[(i + 1) % 15])
                 for i, v in enumerate(vertices))
    # Equal nonzero sides and equal dots imply equal smaller interior angles
    # only for boundary order, not for arbitrary self-crossing circuits.
    return Certificate(path[0] == path[-1], len(set(vertices)) == 15, order,
                       len(set(lengths)) == 1 and lengths[0] != ZERO,
                       len(set(dots)) == 1)


def grid():
    good = branch = short = 0
    for start in range(15):
        for direction in (1, -1):
            step = step_exponent(half_arc(pentagon_direction=direction,
                                          triangle_direction=direction))
            good += certify(walk(start, step)).regular
            wrong = step_exponent(half_arc(pentagon_direction=-direction,
                                           triangle_direction=direction))
            branch += not certify(walk(start, wrong)).regular
            path = walk(start, step)
            # Preserve the fifteen listed vertices, falsify the final return only.
            short += not certify(path[:-1] + (path[-2],)).closed
    return good, branch, short


if __name__ == "__main__":
    step = step_exponent(half_arc())
    print("half arc:", half_arc(), "| step:", step, "| orbit:", 15 // gcd(15, step))
    print("walk:", walk(3, step))
    print("exact grid (regular, opposite-side, missing return):", grid())
