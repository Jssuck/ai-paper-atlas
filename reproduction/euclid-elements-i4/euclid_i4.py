"""Original exact-rational teaching model of Euclid I.4, not a proof assistant.

Only int (not bool) and fractions.Fraction coordinates are accepted.  Equality
of the included angle is represented by equal dot products AFTER the two
incident squared lengths agree; no arbitrary angle function is evaluated.
"""

from dataclasses import dataclass, field
from fractions import Fraction


class InputError(ValueError):
    """Malformed, inexact, or degenerate geometric input."""


class VerificationError(RuntimeError):
    """An explicitly checked algebraic invariant unexpectedly failed."""


def rational(value, label="coordinate"):
    if type(value) is int:
        return Fraction(value)
    if type(value) is Fraction:
        return value
    raise InputError(
        f"{label}: expected int or Fraction; bool, float (including NaN/Infinity), "
        "strings and other numeric types are not accepted"
    )


def point(value, label="point"):
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise InputError(f"{label}: expected a list/tuple of exactly two coordinates")
    return tuple(rational(x, f"{label}[{i}]") for i, x in enumerate(value))


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def matvec(m, p):
    return (dot(m[0], p), dot(m[1], p))


def matmul(m, n):
    return tuple(tuple(sum(m[i][k] * n[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def transpose(m):
    return ((m[0][0], m[1][0]), (m[0][1], m[1][1]))


IDENTITY = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))


@dataclass(frozen=True)
class Triangle:
    """A nondegenerate, ordered (A,B,C) triangle, interpreted over R^2."""

    a: tuple
    b: tuple
    c: tuple
    u: tuple = field(init=False)
    v: tuple = field(init=False)
    determinant: Fraction = field(init=False)
    gram: tuple = field(init=False)

    def __post_init__(self):
        for name in ("a", "b", "c"):
            object.__setattr__(self, name, point(getattr(self, name), name))
        u, v = sub(self.b, self.a), sub(self.c, self.a)
        determinant = cross(u, v)
        if determinant == 0:
            raise InputError("triangle: collinear or repeated vertices; nonzero determinant required")
        object.__setattr__(self, "u", u)
        object.__setattr__(self, "v", v)
        object.__setattr__(self, "determinant", determinant)
        object.__setattr__(self, "gram", (dot(u, u), dot(v, v), dot(u, v)))

    @property
    def vertices(self):
        return self.a, self.b, self.c

    @property
    def side_squares(self):
        """AB^2, AC^2, BC^2, in the declared correspondence."""
        return self.gram[0], self.gram[1], dot(sub(self.c, self.b), sub(self.c, self.b))

    @property
    def angle_data(self):
        """At each vertex: (first incident length^2, dot, second length^2).

        Equality of this data implies equal ordinary interior angles in R^2;
        this routine neither computes nor independently checks an angle function.
        """
        a, b, c = self.vertices
        pairs = ((sub(b, a), sub(c, a)),
                 (sub(a, b), sub(c, b)),
                 (sub(a, c), sub(b, c)))
        return tuple((dot(x, x), dot(x, y), dot(y, y)) for x, y in pairs)


def triangle(value, label="triangle"):
    if isinstance(value, Triangle):
        return value
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise InputError(f"{label}: expected three ordered points (A,B,C)")
    return Triangle(*value)


def matrix(value):
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise InputError("matrix: expected two rows of two exact rational entries")
    return point(value[0], "matrix row 0"), point(value[1], "matrix row 1")


@dataclass(frozen=True)
class Certificate:
    q: tuple
    t: tuple

    def __post_init__(self):
        object.__setattr__(self, "q", matrix(self.q))
        object.__setattr__(self, "t", point(self.t, "translation"))

    @property
    def determinant(self):
        return cross(self.q[0], self.q[1])

    def apply(self, p):
        return add(matvec(self.q, point(p)), self.t)


def verify_certificate(source, target, certificate):
    """Independent exact checks; does not call compare_sas or a SAS theorem."""
    source, target = triangle(source, "source"), triangle(target, "target")
    if not isinstance(certificate, Certificate):
        raise InputError("certificate: expected Certificate(q,t)")
    mapped = tuple(certificate.apply(p) for p in source.vertices)
    return {
        "orthogonal": matmul(transpose(certificate.q), certificate.q) == IDENTITY,
        "maps_A_to_D": mapped[0] == target.a,
        "maps_B_to_E": mapped[1] == target.b,
        "maps_C_to_F": mapped[2] == target.c,
        "remaining_side_squared_equal": source.side_squares[2] == target.side_squares[2],
        "all_corresponding_side_squares_equal": source.side_squares == target.side_squares,
        "all_corresponding_angle_data_equal": source.angle_data == target.angle_data,
    }


@dataclass(frozen=True)
class SASResult:
    sas_equal: tuple
    congruent: bool
    orientation_preserving: bool | None
    accepted: bool
    reason: str
    certificate: Certificate | None
    checks: tuple


def compare_sas(source, target, *, require_direct=False):
    """Check labelled SAS data and construct/verify the unique affine map.

    ``accepted`` also applies the optional direct-motion (det Q=+1) policy.
    ``congruent`` permits reflections and remains True for a verified reflection
    excluded by that policy.  Invalid/degenerate input raises InputError.
    """
    if type(require_direct) is not bool:
        raise InputError("require_direct: expected bool")
    source, target = triangle(source, "source"), triangle(target, "target")
    sas = tuple(x == y for x, y in zip(source.gram, target.gram))
    if not all(sas):
        return SASResult(sas, False, None, False, "sas_mismatch", None, ())

    # P=[u v], R=[U V]; calculate P^-1 by its explicit 2x2 formula.
    u, v, d = source.u, source.v, source.determinant
    inverse = ((v[1] / d, -v[0] / d), (-u[1] / d, u[0] / d))
    U, V = target.u, target.v
    R = ((U[0], V[0]), (U[1], V[1]))
    q = matmul(R, inverse)
    cert = Certificate(q, sub(target.a, matvec(q, source.a)))
    checks = verify_certificate(source, target, cert)
    if not all(checks.values()) or cert.determinant not in (Fraction(-1), Fraction(1)):
        raise VerificationError("constructed map failed exact isometry/correspondence checks")
    direct = cert.determinant == 1
    accepted = direct or not require_direct
    return SASResult(sas, True, direct, accepted,
                     "verified" if accepted else "reflection_excluded",
                     cert, tuple(checks.items()))


def json_exact(value):
    """JSON-compatible exact values: rational numbers become strings."""
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_exact(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_exact(v) for v in value]
    return value


def result_record(result):
    cert = result.certificate
    return json_exact({
        "sas_equal": result.sas_equal,
        "congruent_allowing_reflection": result.congruent,
        "orientation_preserving": result.orientation_preserving,
        "accepted_under_policy": result.accepted,
        "reason": result.reason,
        "Q": None if cert is None else cert.q,
        "t": None if cert is None else cert.t,
        "det_Q": None if cert is None else cert.determinant,
        "checks": dict(result.checks),
    })
