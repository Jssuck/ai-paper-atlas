"""Exact rational-coordinate teaching check for I.28, not a proof kernel."""
from fractions import Fraction
import hashlib
import json


def rational(s):
    if type(s) is not str:
        raise ValueError('coordinates must be canonical rational strings')
    try:
        q = Fraction(s)
    except (ValueError, ZeroDivisionError):
        raise ValueError('invalid rational') from None
    if str(q) != s:
        raise ValueError('noncanonical rational')
    return q


def point(p):
    if type(p) is not list or len(p) != 2:
        raise ValueError('point needs two coordinates')
    return tuple(rational(x) for x in p)


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return (all(type(k) is str for k in a) and a.keys() == b.keys()
                and all(strict_equal(a[k], b[k]) for k in a))
    if type(a) is list:
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    if type(a) in (str, int, bool, type(None)):
        return a == b
    return False


def make_certificate(data):
    if type(data) is not dict or set(data) != {'E', 'F', 'B', 'D', 'case'}:
        raise ValueError('expected exactly E,F,B,D,case')
    if type(data['case']) is not str or data['case'] not in ('corresponding', 'interior_sum'):
        raise ValueError('unknown angle condition')
    e, f, b, d = [point(data[k]) for k in ('E', 'F', 'B', 'D')]
    t, u, v = sub(f, e), sub(b, e), sub(d, f)
    h, j = cross(t, u), cross(t, v)
    if h*j <= 0:
        raise ValueError('nonzero rays EB,FD must lie on same side of transversal EF')
    # cot(angle) is injective on (0,pi); cot(pi-angle) = -cot(angle).
    k_external, k_interior_e, k_interior_f = -dot(t,u)/abs(h), dot(t,u)/abs(h), -dot(t,v)/abs(j)
    if data['case'] == 'corresponding':
        keys = [k_external, k_interior_f]
        if keys[0] != keys[1]: raise ValueError('corresponding angles not equal')
    else:
        keys = [k_interior_e, k_interior_f]
        if sum(keys) != 0: raise ValueError('interior angles not supplementary')
    determinant = cross(u,v)
    lam = dot(u,v)/dot(u,u)
    if determinant != 0 or lam <= 0 or any(v[i] != lam*u[i] for i in range(2)):
        raise ValueError('parallel direction check failed')
    return {'schema': 1, 'input': json.loads(canonical(data)),
            'input_sha256': hashlib.sha256(canonical(data).encode()).hexdigest(),
            'angle_keys': [str(k) for k in keys],
            'transversal_side_determinants': [str(h), str(j)],
            'direction_determinant': str(determinant), 'same_scale': str(lam),
            'conclusion': 'distinct coplanar lines EB and FD do not intersect'}


def verify_certificate(expected_input, certificate):
    try:
        return strict_equal(make_certificate(expected_input), certificate)
    except (ValueError, TypeError, KeyError, ZeroDivisionError, OverflowError):
        return False
