"""Exact rational modern teaching model of I.40, not a formal Euclidean proof."""
from fractions import Fraction as Q
import json


def scalar(x):
    if type(x) is int: return Q(x)
    if type(x) is str:
        try: q=Q(x)
        except (ValueError, ZeroDivisionError): raise ValueError('invalid rational') from None
        if str(q)==x: return q
    raise ValueError('integer or canonical rational string required')


def parse(data):
    if type(data) is not dict or set(data)!=set('ABCDEF'):
        raise ValueError('exact A B C D E F keys required')
    points={}
    for key,value in data.items():
        if type(value) is not list or len(value)!=2: raise ValueError('point must be two-element list')
        points[key]=tuple(scalar(x) for x in value)
    return points


def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(t,a): return (t*a[0],t*a[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def norm2(a): return a[0]*a[0]+a[1]*a[1]
def area2(a,b,c): return abs(cross(sub(b,a),sub(c,a)))


def encode(x):
    if isinstance(x,Q): return str(x)
    if type(x) in (tuple,list): return [encode(v) for v in x]
    if type(x) is dict: return {k:encode(v) for k,v in x.items()}
    return x


def construction_trace(data):
    """Equal bases required; unequal areas allowed ONLY for reductio illustrations."""
    p=parse(data); A,B,C,D,E,F=(p[k] for k in 'ABCDEF');u=sub(C,B);v=sub(F,E)
    if not norm2(u) or not norm2(v): raise ValueError('zero base')
    if cross(u,sub(E,B)) or cross(u,sub(F,B)): raise ValueError('bases must lie on one line')
    if norm2(u)!=norm2(v): raise ValueError('unequal base lengths')
    a,d=cross(u,sub(A,B)),cross(u,sub(D,B))
    if not a or not d: raise ValueError('degenerate triangle')
    if a*d<=0: raise ValueError('apexes must lie on same side')
    t=a/d; G=add(E,mul(t,sub(D,E)))
    branch='inner' if t<1 else ('outer' if t>1 else 'equal')
    return encode({'schema':'euclid-i40-trace-v1','input':p,'G':G,'t':t,'branch':branch,
        'base_squared_length':norm2(u),'base_direction':'same' if u==v else 'reversed',
        'signed_height_numerators':{'A':a,'D':d},
        'double_area':{'ABC':area2(A,B,C),'DEF':area2(D,E,F),'GEF':area2(G,E,F),'GDF':area2(G,D,F)},
        'cross':{'BC_AG':cross(u,sub(G,A)),'BC_AD':cross(u,sub(D,A))},
        'whole':'DEF' if t<1 else ('GEF' if t>1 else 'equal'),
        'part':'GEF' if t<1 else ('DEF' if t>1 else 'equal'),
        'apex_relation':'coincident' if A==D else 'distinct'})


def make_certificate(data):
    trace=construction_trace(data)
    if trace['branch']!='equal': raise ValueError('unequal areas: I.40 premise fails')
    conclusion='AD undefined; common parallel through coincident apex' if trace['apex_relation']=='coincident' else 'AD parallel BC'
    return {'schema':'euclid-i40-certificate-v1','trace':trace,'conclusion':conclusion}


def certificate_types(x):
    if type(x) is str:return
    if type(x) is list:
        for v in x:certificate_types(v)
        return
    if type(x) is dict and all(type(k) is str for k in x):
        for v in x.values():certificate_types(v)
        return
    raise ValueError('certificate permits only JSON string/list/object values')


def verify_certificate(data,certificate):
    """Strict types and normalized input binding; invalid geometry never certifies."""
    try:
        expected=make_certificate(data);certificate_types(certificate)
        return json.dumps(certificate,sort_keys=True)==json.dumps(expected,sort_keys=True)
    except (ValueError,TypeError,OverflowError,RecursionError):return False
