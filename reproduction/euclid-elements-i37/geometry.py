"""I.37: original exact rational teaching model, not a formalization of Euclid."""
from fractions import Fraction as F
import json

def scalar(x):
    if type(x) is int:return F(x)
    if type(x) is str:
        try:y=F(x)
        except (ValueError,ZeroDivisionError):raise ValueError('invalid rational') from None
        if str(y)==x:return y
    raise ValueError('integer or canonical rational string required')
def parse(data):
    if type(data) is not dict or set(data)!=set('ABCD'):raise ValueError('exact A B C D keys required')
    p={}
    for k,v in data.items():
        if type(v) is not list or len(v)!=2:raise ValueError('two-element point list required')
        p[k]=tuple(map(scalar,v))
    return p
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def dot(u,v):return sum(x*y for x,y in zip(u,v))
def area(*p):return abs(sum(cross(p[i],p[(i+1)%len(p)]) for i in range(len(p))))/2
def encode(x):
    if isinstance(x,F):return str(x)
    if type(x) in (list,tuple):return [encode(v) for v in x]
    if type(x) is dict:return {k:encode(v) for k,v in x.items()}
    return x
def make_certificate(data):
    p=parse(data);A,B,C,D=(p[k] for k in 'ABCD');u=sub(C,B)
    delta=cross(u,sub(A,B))
    if not delta:raise ValueError('base or first triangle degenerate')
    if cross(u,sub(D,A)):raise ValueError('vertices not on same upper support')
    E=sub(A,u);Fp=add(D,u)
    t=dot(sub(D,A),u)/dot(u,u)
    return encode({'schema':'euclid-i37-exact-v1','input':p,'base_squared':dot(u,u),
        'signed_double_triangle_area':delta,'vertices':{'E':E,'F':Fp},
        'parallel_checks':{'BE_CA':cross(sub(E,B),sub(A,C)),'CF_BD':cross(sub(Fp,C),sub(D,B)),
                           'AE_BC':cross(sub(A,E),u),'DF_BC':cross(sub(Fp,D),u)},
        'area':{'ABC':area(A,B,C),'DBC':area(D,B,C),'EBCA':area(E,B,C,A),'DBCF':area(D,B,C,Fp)},
        'halves':{'AB_diagonal_ABC':area(A,B,C),'AB_diagonal_EBA':area(E,B,A),
                  'DC_diagonal_DBC':area(D,B,C),'DC_diagonal_DCF':area(D,C,Fp)},
        'top_shift':t,'top_case':'coincident' if t==0 else ('forward' if t>0 else 'backward')})
def json_value(x):
    if type(x) is str:return
    if type(x) is list:
        for v in x:json_value(v)
        return
    if type(x) is dict and all(type(k) is str for k in x):
        for v in x.values():json_value(v)
        return
    raise ValueError('only JSON string/list/object certificate values allowed')
def verify_certificate(data,cert):
    try:
        expected=make_certificate(data);json_value(cert)
        return json.dumps(cert,sort_keys=True,ensure_ascii=False)==json.dumps(expected,sort_keys=True,ensure_ascii=False)
    except (ValueError,TypeError,OverflowError,RecursionError):return False
