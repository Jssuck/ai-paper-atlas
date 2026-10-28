"""Exact rational teaching reconstruction of I.39; not a proof assistant."""
from fractions import Fraction as Q
import json


def scalar(value):
    if type(value) is int: return Q(value)
    if type(value) is str:
        try: number=Q(value)
        except (ValueError, ZeroDivisionError): raise ValueError('invalid rational') from None
        if str(number)==value: return number
    raise ValueError('integer or canonical rational string required')


def parse(data):
    if type(data) is not dict or set(data)!=set('ABCD'):
        raise ValueError('exact A B C D keys required')
    p={}
    for k,v in data.items():
        if type(v) is not list or len(v)!=2: raise ValueError('point must be two-element list')
        p[k]=tuple(scalar(x) for x in v)
    return p


def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(t,a): return (t*a[0],t*a[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def signed2(a,b,c): return cross(sub(b,a),sub(c,a))
def area(a,b,c): return abs(signed2(a,b,c))/2


def encode(value):
    if isinstance(value,Q): return str(value)
    if type(value) in (tuple,list): return [encode(x) for x in value]
    if type(value) is dict: return {k:encode(v) for k,v in value.items()}
    return value


def construction_trace(data):
    """Unequal areas allowed ONLY to illustrate contradiction branches."""
    p=parse(data);A,B,C,D=(p[k] for k in 'ABCD');u=sub(C,B)
    if B==C: raise ValueError('zero base')
    a,d=cross(u,sub(A,B)),cross(u,sub(D,B))
    if not a or not d: raise ValueError('degenerate triangle')
    if a*d<=0: raise ValueError('apexes must lie on same side')
    if A==D: raise ValueError('coincident apexes do not determine line AD')
    t=a/d;E=add(B,mul(t,sub(D,B)))
    branch='inner' if t<1 else ('outer' if t>1 else 'equal')
    return encode({'schema':'euclid-i39-trace-v1','input':p,'t':t,'E':E,'branch':branch,
        'signed_double_area':{'ABC':a,'DBC':d},
        'area':{'ABC':area(A,B,C),'DBC':area(D,B,C),'EBC':area(E,B,C),'EDC':area(E,D,C)},
        'cross':{'BC_AE':cross(u,sub(E,A)),'BC_AD':cross(u,sub(D,A))},
        'whole':'DBC' if t<1 else ('EBC' if t>1 else 'equal'),
        'part':'EBC' if t<1 else ('DBC' if t>1 else 'equal')})


def make_certificate(data):
    trace=construction_trace(data)
    if trace['branch']!='equal': raise ValueError('unequal areas: I.39 premise fails')
    return {'schema':'euclid-i39-certificate-v1','trace':trace,'conclusion':'AD parallel BC'}


def certificate_types(value):
    if type(value) is str:return
    if type(value) is list:
        for x in value:certificate_types(x)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for x in value.values():certificate_types(x)
        return
    raise ValueError('certificate permits only JSON string/list/object values')


def verify_certificate(data,certificate):
    """Recompute every field, bound to all normalized original coordinates."""
    try:
        expected=make_certificate(data);certificate_types(certificate)
        return json.dumps(certificate,sort_keys=True)==json.dumps(expected,sort_keys=True)
    except (ValueError,TypeError,OverflowError,RecursionError):return False
