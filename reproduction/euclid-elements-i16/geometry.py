"""Exact rational, planar teaching reconstruction of Euclid I.16, not a proof assistant."""
from fractions import Fraction as Q
import json


def scalar(x):
    if type(x) is int:
        return Q(x)
    if type(x) is str:
        try:
            return Q(x)
        except (ValueError, ZeroDivisionError) as e:
            raise ValueError('invalid rational string') from e
    raise ValueError('coordinate must be an integer or rational string, not bool/float')


def point(p):
    if type(p) is not list or len(p) != 2:
        raise ValueError('point must be a two-item JSON list')
    return tuple(scalar(x) for x in p)


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def scale(a, t): return tuple(x*t for x in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return a[0]*b[1]-a[1]*b[0]
def norm2(a): return dot(a, a)
def encoded(p): return [str(x) for x in p]


def same_angle(u, v, w, z):
    """Equality of ordinary nonzero-ray angles using exact cosine sign and square."""
    if not all(norm2(t) > 0 for t in (u, v, w, z)):
        return False
    p, q = dot(u, v), dot(w, z)
    if (p > 0)-(p < 0) != (q > 0)-(q < 0):
        return False
    return p*p*norm2(w)*norm2(z) == q*q*norm2(u)*norm2(v)


def strict_inside(u, v, w):
    """w is strictly inside the ordinary wedge from independent u to v (< pi)."""
    d = cross(u, v)
    return d != 0 and cross(u, w)*d > 0 and cross(w, v)*d > 0


def parse(payload):
    if type(payload) is not dict or set(payload) != {'A','B','C','D'}:
        raise ValueError('exactly A B C D are required')
    a,b,c,d = (point(payload[k]) for k in 'ABCD')
    if cross(sub(b,a), sub(c,a)) == 0:
        raise ValueError('triangle must be noncollinear')
    bc,cd = sub(c,b),sub(d,c)
    if cross(bc,cd) != 0 or dot(bc,cd) <= 0:
        raise ValueError('D must lie strictly beyond C on ray B C')
    return a,b,c,d


def construct(payload):
    a,b,c,d = parse(payload)
    e = scale(add(a,c), Q(1,2))
    f = sub(add(a,c), b)
    m = scale(add(b,c), Q(1,2))
    n = sub(add(b,c), a)
    g = add(c,sub(c,a))
    # First branch: AEB ~ CEF by SAS; second: BMA ~ CMN by SAS.
    checks = {
        'AE_equals_EC': norm2(sub(a,e)) == norm2(sub(c,e)),
        'BE_equals_EF': norm2(sub(b,e)) == norm2(sub(f,e)),
        'vertical_at_E': same_angle(sub(a,e),sub(b,e),sub(c,e),sub(f,e)),
        'BAC_equals_ECF': same_angle(sub(b,a),sub(c,a),sub(e,c),sub(f,c)),
        'CF_inside_ACD': strict_inside(sub(a,c),sub(d,c),sub(f,c)),
        'BM_equals_MC': norm2(sub(b,m)) == norm2(sub(c,m)),
        'AM_equals_MN': norm2(sub(a,m)) == norm2(sub(n,m)),
        'vertical_at_M': same_angle(sub(b,m),sub(a,m),sub(c,m),sub(n,m)),
        'ABC_equals_MCN': same_angle(sub(a,b),sub(c,b),sub(m,c),sub(n,c)),
        'CN_inside_BCG': strict_inside(sub(b,c),sub(g,c),sub(n,c)),
        'BCG_equals_ACD': same_angle(sub(b,c),sub(g,c),sub(a,c),sub(d,c)),
    }
    if not all(checks.values()):
        raise RuntimeError('construction invariant failed')
    # lambda > 0 with CD=lambda*(C-B), so CF=CA+CD/lambda.
    lam = dot(sub(d,c),sub(c,b))/norm2(sub(c,b))
    return {'schema': 1,
            'input': {k:encoded(p) for k,p in zip('ABCD',(a,b,c,d))},
            'points': {k:encoded(p) for k,p in zip('EFMNG',(e,f,m,n,g))},
            'coefficients': {'CF_in_CA_CD':['1',str(1/lam)],
                             'CN_in_CB_CG':['1','1']},
            'checks': checks,
            'conclusions': ['angle ACD > angle BAC', 'angle ACD > angle ABC'],
            'scope': 'rational Euclidean plane; finite execution is not a general proof'}


def canonical_json(value):
    def check(x):
        if x is None or type(x) in (bool,int,str): return
        if type(x) is list:
            for v in x: check(v)
            return
        if type(x) is dict and all(type(k) is str for k in x):
            for v in x.values(): check(v)
            return
        raise ValueError('strict JSON values only; floats and non-JSON containers rejected')
    check(value)
    return json.dumps(value, sort_keys=True, separators=(',',':'), ensure_ascii=False)


def verify(payload, certificate):
    """Input-bound recomputation, not self-asserted certificate checks."""
    try:
        return canonical_json(certificate) == canonical_json(construct(payload))
    except (ValueError, TypeError, ZeroDivisionError):
        return False
