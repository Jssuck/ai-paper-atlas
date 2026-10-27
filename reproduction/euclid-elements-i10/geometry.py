"""Original teaching reconstruction of Elements I.10, exact over Q(sqrt(3)).

Arithmetic/angle predicates are adapted from this project's original I.9 model.
The I.10 construction, intersection solver and input-bound checker are new.
This models Euclidean geometry in modern coordinates, not ancient computation.
"""
from dataclasses import dataclass
from fractions import Fraction


def rational(value):
    """Deliberately reject floats/bools rather than silently rounding input."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError('use int or fractions.Fraction for exact rational input')
    return Fraction(value)


@dataclass(frozen=True)
class Q3:
    """a + b sqrt(3), with exact rational coefficients."""
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', rational(self.a))
        object.__setattr__(self, 'b', rational(self.b))

    @staticmethod
    def of(value):
        return value if isinstance(value, Q3) else Q3(value)

    def __add__(self, value):
        value = self.of(value)
        return Q3(self.a + value.a, self.b + value.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, value):
        return self + -self.of(value)

    def __rsub__(self, value):
        return self.of(value) + -self

    def __mul__(self, value):
        value = self.of(value)
        return Q3(self.a * value.a + 3 * self.b * value.b,
                  self.a * value.b + self.b * value.a)

    __rmul__ = __mul__

    def __truediv__(self, value):
        value = self.of(value)
        denominator = value.a * value.a - 3 * value.b * value.b
        if not denominator:
            raise ZeroDivisionError('zero element of Q(sqrt(3))')
        return self * Q3(value.a / denominator, -value.b / denominator)

    def __rtruediv__(self, value):
        return self.of(value) / self

    def sign(self):
        """Exact order; opposite signs are compared using a² versus 3b²."""
        sign_a = (self.a > 0) - (self.a < 0)
        sign_b = (self.b > 0) - (self.b < 0)
        if not sign_b:
            return sign_a
        if not sign_a:
            return sign_b
        if sign_a == sign_b:
            return sign_a
        delta = self.a * self.a - 3 * self.b * self.b
        return sign_a * ((delta > 0) - (delta < 0))

    def __str__(self):
        if not self.b:
            return str(self.a)
        return f'({self.a})+({self.b})*sqrt(3)'


ZERO = Q3()
ONE = Q3(1)
SQRT3 = Q3(0, 1)
HALF = Fraction(1, 2)


def point(x, y):
    return (Q3.of(x), Q3.of(y))


def is_point(p):
    return isinstance(p, tuple) and len(p) == 2 and all(isinstance(x, Q3) for x in p)


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def scale(k, p):
    return (Q3.of(k) * p[0], Q3.of(k) * p[1])


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def norm2(p):
    return dot(p, p)


def dist2(p, q):
    return norm2(sub(p, q))


def rotate90(p):
    return (-p[1], p[0])


def equilateral_vertices(a, b):
    """I.1 coordinate model: return the two candidates in +/− orientation."""
    center = scale(HALF, add(a, b))
    offset = scale(SQRT3 / 2, rotate90(sub(b, a)))
    return (add(center, offset), sub(center, offset))


def inside(u, v, w):
    """w lies strictly inside the convex (< pi) angle from u to v."""
    orientation = cross(u, v).sign()
    return (orientation != 0 and cross(u, w).sign() == orientation
            and cross(w, v).sign() == orientation)


def equal_angles(u, v, w):
    """angle(u,w) = angle(v,w) in [0,pi]; this alone does NOT mean internal.

    Squared cosine cross-products need the dot-product sign check, otherwise
    supplementary angles may be mistaken for equal angles. No arccos or float.
    """
    if any(norm2(z).sign() <= 0 for z in (u, v, w)):
        return False
    p, q = dot(u, w), dot(v, w)
    return p.sign() == q.sign() and p * p * norm2(v) == q * q * norm2(u)


def i9_vertex(c, a, b):
    """I.9 for the already equal cuts CA=CB: choose F opposite C across AB.

    No I.3 length transfer is needed for this equilateral input. The candidates
    are an I.1 coordinate model, not a physical ruler/compass implementation.
    """
    u, v = sub(a, c), sub(b, c)
    if norm2(u).sign() <= 0 or norm2(u) != norm2(v) or cross(u, v).sign() == 0:
        raise ValueError('I.9 requires equal positive cuts and a nondegenerate angle')
    baseline = sub(b, a)
    c_side = cross(baseline, sub(c, a)).sign()
    for f in equilateral_vertices(a, b):
        if c_side * cross(baseline, sub(f, a)).sign() == -1:
            return f
    raise ArithmeticError('no opposite-side equilateral candidate')


def intersect_open_ray_segment(origin, direction, a, b):
    """Solve origin+s*direction = a+t*(b-a), then require s>0, 0<t<1.

    Returns D,s,t. In particular, D is NOT assigned the midpoint formula.
    The determinant also certifies a unique intersection of the two lines.
    """
    edge = sub(b, a)
    if norm2(direction).sign() <= 0 or norm2(edge).sign() <= 0:
        raise ValueError('nonzero ray direction and nondegenerate segment required')
    denominator = cross(direction, edge)
    if denominator.sign() == 0:
        raise ValueError('parallel or coincident supporting lines')
    offset = sub(a, origin)
    s = cross(offset, edge) / denominator
    t = cross(offset, direction) / denominator
    if s.sign() <= 0 or t.sign() <= 0 or (ONE - t).sign() <= 0:
        raise ValueError('intersection is not on the open ray and segment interior')
    return add(origin, scale(s, direction)), s, t


@dataclass(frozen=True)
class Certificate:
    branch: int
    c: tuple
    f: tuple
    d: tuple
    s: Q3
    t: Q3


def valid_input(a, b):
    return (is_point(a) and is_point(b)
            and all(x.b == 0 for x in (*a, *b)) and dist2(a, b).sign() > 0)


def construct(a, b, branch=1):
    """Input: distinct rational points; branch +1 or −1 selects I.1 apex C."""
    if not valid_input(a, b):
        raise ValueError('A and B must be distinct rational-coordinate points')
    if type(branch) is not int or branch not in (-1, 1):
        raise ValueError('branch must be +1 or -1')
    c = equilateral_vertices(a, b)[0 if branch == 1 else 1]
    f = i9_vertex(c, a, b)
    d, s, t = intersect_open_ray_segment(c, sub(f, c), a, b)
    return Certificate(branch, c, f, d, s, t)


def check_certificate(a, b, cert):
    """Recompute facts from trusted input and claimed geometry, not stored flags.

    This is a mathematical consistency checker, not a signature/authentication
    system. Acceptance means these geometric predicates hold, not that the
    certificate has a particular trusted author or untampered file history.
    """
    names = (
        'input_rational_nondegenerate', 'certificate_format',
        'I1_branch_matches', 'I1_equilateral', 'I9_equal_positive_cuts',
        'I9_equilateral_on_AB', 'I9_opposite_side', 'I9_nonzero_ray',
        'I9_strictly_inside', 'I9_equal_angles', 'intersection_unique_lines',
        'intersection_on_claimed_ray', 'intersection_on_claimed_segment',
        'intersection_collinear_AB', 'intersection_positive_ray_parameter',
        'intersection_strict_segment_parameter', 'I4_equal_CA_CB',
        'I4_common_positive_CD', 'I4_equal_included_angles', 'I4_nondegenerate_triangles',
        'I4_SAS_premises', 'conclusion_AD_equals_DB',
    )
    facts = dict.fromkeys(names, False)
    facts['input_rational_nondegenerate'] = valid_input(a, b)
    facts['certificate_format'] = (
        isinstance(cert, Certificate) and type(cert.branch) is int
        and cert.branch in (-1, 1) and all(is_point(p) for p in (cert.c, cert.f, cert.d))
        and isinstance(cert.s, Q3) and isinstance(cert.t, Q3))
    if not facts['input_rational_nondegenerate'] or not facts['certificate_format']:
        return facts
    c, f, d = cert.c, cert.f, cert.d
    edge, ray = sub(b, a), sub(f, c)
    ca, cb, cd = sub(a, c), sub(b, c), sub(d, c)
    length2 = dist2(a, b)
    facts.update({
        'I1_branch_matches': c == equilateral_vertices(a, b)[0 if cert.branch == 1 else 1],
        'I1_equilateral': dist2(a, c) == length2 == dist2(b, c),
        'I9_equal_positive_cuts': norm2(ca) == norm2(cb) and norm2(ca).sign() > 0,
        'I9_equilateral_on_AB': dist2(a, f) == length2 == dist2(b, f),
        'I9_opposite_side': cross(edge, sub(c, a)).sign() * cross(edge, sub(f, a)).sign() == -1,
        'I9_nonzero_ray': norm2(ray).sign() > 0,
        'I9_strictly_inside': inside(ca, cb, ray),
        'I9_equal_angles': equal_angles(ca, cb, ray),
        'intersection_unique_lines': cross(ray, edge).sign() != 0,
        'intersection_on_claimed_ray': d == add(c, scale(cert.s, ray)),
        'intersection_on_claimed_segment': d == add(a, scale(cert.t, edge)),
        'intersection_collinear_AB': cross(edge, sub(d, a)).sign() == 0,
        'intersection_positive_ray_parameter': cert.s.sign() > 0,
        'intersection_strict_segment_parameter': cert.t.sign() > 0 and (ONE - cert.t).sign() > 0,
        'I4_equal_CA_CB': norm2(ca) == norm2(cb),
        'I4_common_positive_CD': norm2(cd).sign() > 0,
        'I4_equal_included_angles': equal_angles(ca, cb, cd),
        'I4_nondegenerate_triangles': cross(ca, cd).sign() != 0 and cross(cb, cd).sign() != 0,
        'conclusion_AD_equals_DB': dist2(a, d) == dist2(b, d),
    })
    # CD is literally the same edge in triangles ACD and BCD, so the positive
    # common-side check plus these equal-side/equal-angle checks model SAS.
    facts['I4_SAS_premises'] = all(facts[k] for k in (
        'I4_equal_CA_CB', 'I4_common_positive_CD', 'I4_equal_included_angles',
        'I4_nondegenerate_triangles'))
    return facts


def accepted(a, b, cert):
    return all(check_certificate(a, b, cert).values())


def encode(value):
    """Lossless public JSON form; coefficients are rational strings."""
    if isinstance(value, Q3):
        return {'a': str(value.a), 'b': str(value.b)}
    if isinstance(value, tuple):
        return [encode(x) for x in value]
    if isinstance(value, Certificate):
        return {k: encode(getattr(value, k)) for k in ('branch', 'c', 'f', 'd', 's', 't')}
    return value
