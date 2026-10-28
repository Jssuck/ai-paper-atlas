"""Exact rational I.38 teaching checks, not Euclid's proof or a proof assistant."""
from fractions import Fraction as Q
import json


def scalar(value):
    if type(value) is int:
        return Q(value)
    if type(value) is str:
        try:
            number = Q(value)
        except (ValueError, ZeroDivisionError):
            raise ValueError('invalid rational') from None
        if str(number) == value:
            return number
    raise ValueError('integer or canonical rational string required')


def parse(data):
    if type(data) is not dict or set(data) != set('ABCDEF'):
        raise ValueError('exact A B C D E F keys required')
    points = {}
    for key, value in data.items():
        if type(value) is not list or len(value) != 2:
            raise ValueError('point must be a two-element list')
        points[key] = tuple(scalar(x) for x in value)
    return points


def add(a, b): return tuple(x+y for x,y in zip(a,b))
def sub(a, b): return tuple(x-y for x,y in zip(a,b))
def cross(a, b): return a[0]*b[1]-a[1]*b[0]
def dot(a, b): return a[0]*b[0]+a[1]*b[1]
def area(*points):
    return abs(sum(cross(points[i], points[(i+1)%len(points)])
                   for i in range(len(points)))) / 2


def encode(value):
    if isinstance(value, Q): return str(value)
    if type(value) in (list, tuple): return [encode(x) for x in value]
    if type(value) is dict: return {k:encode(v) for k,v in value.items()}
    return value


def make_certificate(data):
    p = parse(data)
    A,B,C,D,E,F = (p[k] for k in 'ABCDEF')
    u,w = sub(C,B),sub(F,E)
    squared = dot(u,u)
    if not squared or not dot(w,w):
        raise ValueError('zero base')
    if cross(u,sub(E,B)) or cross(u,sub(F,B)):
        raise ValueError('bases must share one support line')
    if squared != dot(w,w):
        raise ValueError('base lengths differ')
    delta = cross(u,sub(A,B))
    if not delta:
        raise ValueError('triangle ABC degenerate')
    if cross(u,sub(D,A)):
        raise ValueError('A and D must share the same non-base parallel')
    G,H = sub(A,u),add(D,w)
    return encode({
        'schema':'euclid-i38-exact-v1', 'input':p,
        'base_squared':squared,
        'base_direction':'same' if dot(u,w)>0 else 'opposite',
        'signed_double_areas':{'ABC':cross(sub(B,A),sub(C,A)),
                               'DEF':cross(sub(E,D),sub(F,D))},
        'vertices':{'G':G,'H':H},
        'parallel_checks':{'BG_CA':cross(sub(G,B),sub(A,C)),
                           'FH_DE':cross(sub(H,F),sub(E,D)),
                           'GA_BC':cross(sub(A,G),u),
                           'DH_EF':cross(sub(H,D),w)},
        'area':{'ABC':area(A,B,C),'DEF':area(D,E,F),
                'GBCA':area(G,B,C,A),'DEFH':area(D,E,F,H)},
        'halves':{'AB_ABC':area(A,B,C),'AB_GBA':area(G,B,A),
                  'DF_DEF':area(D,E,F),'DF_DFH':area(D,F,H)},
        'coincidences':{'A_D':'yes' if A==D else 'no',
                         'G_H':'yes' if G==H else 'no'},
    })


def certificate_types(value):
    if type(value) is str: return
    if type(value) is list:
        for item in value: certificate_types(item)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for item in value.values(): certificate_types(item)
        return
    raise ValueError('certificate permits only JSON string/list/object values')


def verify_certificate(data, certificate):
    """Recompute all fields; binding is to normalized coordinates, not area alone."""
    try:
        expected = make_certificate(data)
        certificate_types(certificate)
        return json.dumps(certificate, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (ValueError, TypeError, OverflowError, RecursionError):
        return False
