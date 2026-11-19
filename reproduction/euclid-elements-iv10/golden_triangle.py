"""Coordinate reconstruction of Euclid IV.10; standard library only."""
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Q5:
    """a+b√5, with rational coefficients."""
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        if not all(isinstance(x, (int, F)) for x in (self.a, self.b)):
            raise TypeError("expected exact rational coefficients")
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    def __add__(self, other):
        other = q(other)
        return Q5(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-q(other))

    def __rsub__(self, other):
        return q(other) + (-self)

    def __mul__(self, other):
        other = q(other)
        return Q5(self.a * other.a + 5 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = q(other)
        norm = other.a * other.a - 5 * other.b * other.b
        return self * Q5(other.a / norm, -other.b / norm)

    def sign(self):
        # If signs differ compare |a|² with |b√5|², then use sign(a).
        sa = (self.a > 0) - (self.a < 0)
        sb = (self.b > 0) - (self.b < 0)
        if not sa or not sb or sa == sb:
            return sa or sb
        d = self.a * self.a - 5 * self.b * self.b
        return sa * ((d > 0) - (d < 0))


def q(x):
    return x if isinstance(x, Q5) else Q5(x)


GOLDEN_SPLIT = Q5(F(-1, 2), F(1, 2))


@dataclass(frozen=True)
class Certificate:
    scale: F
    t: Q5
    y2: Q5
    branch: int
    # Points use the basis (1,0),(0,√y2) in normalized coordinates.
    A: tuple
    B: tuple
    C: tuple
    D: tuple
    O: tuple

    def vector(self, p, r):
        return tuple(a - b for a, b in zip(r, p))

    def dot(self, p, r):
        return self.scale * self.scale * (p[0] * r[0] + self.y2 * p[1] * r[1])

    def dist2(self, p, r):
        d = self.vector(p, r)
        return self.dot(d, d)

    def checks(self):
        A, B, C, D, O = self.A, self.B, self.C, self.D, self.O
        s = self.scale
        ab, ac, bd = self.dist2(A, B), self.dist2(A, C), self.dist2(B, D)
        ad, cd = self.dist2(A, D), self.dist2(C, D)
        power_product = s * s * (1 - self.t)
        apex_cos = self.dot(self.vector(A, B), self.vector(A, D)) / ab
        # |BD| = s*t since the chord check below verifies its square.
        base_denominator = s * s * self.t
        base_B_cos = self.dot(self.vector(B, A), self.vector(B, D)) / base_denominator
        base_D_cos = self.dot(self.vector(D, A), self.vector(D, B)) / base_denominator
        # cos is injective on [0,π]; apex acute ensures twice apex lies there.
        double_cos = 2 * apex_cos * apex_cos - 1
        return {
            "nondegenerate": self.y2.sign() > 0 and self.D[1].sign() == self.branch,
            "given_circle_and_chord": ab == ad and ac == bd,
            "split_product": power_product == ac,
            "circumcircle_ACD": self.dist2(O, A) == self.dist2(O, C) == self.dist2(O, D),
            "B_outside": (self.dist2(O, B) - self.dist2(O, A)).sign() > 0,
            "point_power": self.dist2(O, B) - self.dist2(O, A) == power_product,
            "tangent_at_D": self.dot(self.vector(O, D), self.vector(D, B)) == Q5(),
            "equal_BD_CD_AC": bd == cd == ac,
            "both_base_angles_double": apex_cos.sign() > 0 and base_B_cos == base_D_cos == double_cos,
        }


def construct(scale=1, t=GOLDEN_SPLIT, branch=1):
    """A–C–B; choose D above (+1) or below (-1) the AB axis."""
    if isinstance(scale, bool) or not isinstance(scale, (int, F)) or scale <= 0:
        raise ValueError("AB must be a positive rational length")
    if type(branch) is not int or branch not in (-1, 1):
        raise ValueError("branch must be +1 or -1")
    t = q(t)
    if t.sign() <= 0 or (1 - t).sign() <= 0:
        raise ValueError("C must lie strictly between A and B")
    u = 1 - t * t / 2
    y2 = 1 - u * u
    # O_x=t/2 by equal distances to A and C. Equal distances
    # to A and D then give 2*(u*O_x+branch*y2*O_y)=1.
    o_y = branch * (1 - t * u) / (2 * y2)
    return Certificate(F(scale), t, y2, branch,
                       (q(0), q(0)), (q(1), q(0)), (t, q(0)),
                       (u, q(branch)), (t / 2, o_y))


def check_grid():
    scales = [F(n, d) for n in range(1, 13) for d in (13, 17, 19, 23)]
    positive = [(s, b) for s in scales for b in (-1, 1)]
    for s, b in positive:
        result = construct(s, branch=b).checks()
        if not all(result.values()):
            raise AssertionError(result)
    controls = [(t, b) for t in (F(1, 3), F(1, 2), F(2, 3), F(9, 10)) for b in (-1, 1)]
    for t, b in controls:
        result = construct(t=t, branch=b).checks()
        keep = ("nondegenerate", "given_circle_and_chord", "circumcircle_ACD", "B_outside", "point_power")
        lose = ("split_product", "tangent_at_D", "equal_BD_CD_AC", "both_base_angles_double")
        if not all(result[k] for k in keep) or any(result[k] for k in lose):
            raise AssertionError(result)
    return len(positive), len(controls)


if __name__ == "__main__":
    pos, neg = check_grid()
    print(f"Golden split certificates: {pos}; wrong interior split controls: {neg}")
