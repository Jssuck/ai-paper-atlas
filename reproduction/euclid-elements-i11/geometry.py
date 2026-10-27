"""I.11 modern exact-coordinate teaching model, not an ancient algorithm.
Q3 arithmetic and vector helpers adapted from this project's original I.10.
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

def parameter(a, b, p):
    """Unique affine parameter of collinear P on the supporting line AB."""
    v = sub(b, a)
    if norm2(v).sign() <= 0 or cross(v, sub(p, a)) != ZERO:
        raise ValueError('nondegenerate line and collinear point required')
    i = 0 if v[0] != ZERO else 1
    return (p[i] - a[i]) / v[i]


def valid_input(a, b, c, h):
    if not all(is_point(p) for p in (a,b,c)):
        return False
    if any(x.b for p in (a,b,c) for x in p):
        return False
    try:
        h = rational(h)
        t = parameter(a,b,c)
    except (TypeError,ValueError,ZeroDivisionError):
        return False
    return h > 0 and t.sign() >= 0 and (ONE-t).sign() >= 0


@dataclass(frozen=True)
class Certificate:
    branch: int
    d: tuple
    e: tuple
    f: tuple


def construct(a,b,c,h=Fraction(1,4),branch=1):
    """C on closed AB; h>0 is distance CD / length AB, not a distance unit.

    Endpoints and large h may require extending AB. The public checker records
    that fact rather than silently treating D,E as contained in the segment.
    """
    if not valid_input(a,b,c,h):
        raise ValueError('distinct rational A,B, C on closed AB, positive rational h required')
    if type(branch) is not int or branch not in (-1,1):
        raise ValueError('branch must be integer +1 or -1')
    offset = scale(h,sub(b,a))
    d,e = sub(c,offset),add(c,offset)
    f = equilateral_vertices(d,e)[0 if branch==1 else 1]
    return Certificate(branch,d,e,f)


def check_certificate(a,b,c,h,cert):
    """Recompute geometric obligations from trusted inputs, not trusted flags."""
    facts={'input_valid':valid_input(a,b,c,h)}
    if not facts['input_valid']:return facts
    facts['format_valid']=(isinstance(cert,Certificate) and type(cert.branch) is int
         and cert.branch in (-1,1) and all(is_point(p) for p in (cert.d,cert.e,cert.f)))
    if not facts['format_valid']:return facts
    d,e,f=cert.d,cert.e,cert.f
    v,u,w,z=sub(b,a),sub(d,c),sub(e,c),sub(f,c)
    offset=scale(h,v)
    facts.update({
        'cut_parameter_bound':d==sub(c,offset) and e==add(c,offset),
        'D_C_E_collinear':cross(u,v)==ZERO and cross(w,v)==ZERO,
        'opposite_nonzero_rays':dot(u,w).sign()<0 and norm2(u).sign()>0 and norm2(w).sign()>0,
        'CD_equals_CE':norm2(u)==norm2(w),
        'equilateral_DFE':dist2(d,f)==dist2(e,f)==dist2(d,e) and dist2(d,e).sign()>0,
        'branch_bound':f==equilateral_vertices(d,e)[0 if cert.branch==1 else 1],
        'FC_common_positive':norm2(z).sign()>0,
        'nondegenerate_triangles':cross(u,z).sign()!=0 and cross(w,z).sign()!=0,
        'DF_equals_EF':dist2(d,f)==dist2(e,f),
    })
    facts['I8_SSS_premises']=(facts['CD_equals_CE'] and facts['FC_common_positive']
        and facts['DF_equals_EF'] and facts['nondegenerate_triangles'])
    # Equal-angle verification via signed cosine, not via I.8 as an oracle.
    p,q=dot(u,z),dot(w,z)
    facts['equal_adjacent_angles_modern_check']=(facts['FC_common_positive']
        and norm2(u).sign()>0 and norm2(w).sign()>0 and p.sign()==q.sign()
        and p*p*norm2(w)==q*q*norm2(u))
    facts['right_angle_definition_configuration']=(facts['D_C_E_collinear']
        and facts['opposite_nonzero_rays'] and facts['equal_adjacent_angles_modern_check'])
    facts['perpendicular_modern_check']=norm2(z).sign()>0 and dot(v,z)==ZERO
    return facts


def accepted(a,b,c,h,cert):
    return all(check_certificate(a,b,c,h,cert).values())


def extension_report(a,b,cert):
    td,te=parameter(a,b,cert.d),parameter(a,b,cert.e)
    return {'D_parameter':str(td),'E_parameter':str(te),
            'D_outside_segment':td.sign()<0 or (ONE-td).sign()<0,
            'E_outside_segment':te.sign()<0 or (ONE-te).sign()<0}


def record(a,b,c,h,cert):
    return {'A':list(map(str,a)),'B':list(map(str,b)),'C':list(map(str,c)),
            'h':str(h),'branch':cert.branch,
            'D':list(map(str,cert.d)),'E':list(map(str,cert.e)),'F':list(map(str,cert.f)),
            'facts':check_certificate(a,b,c,h,cert),'extension':extension_report(a,b,cert)}
