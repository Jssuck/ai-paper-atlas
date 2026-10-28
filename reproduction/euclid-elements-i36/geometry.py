"""Exact Euclidean coordinate teaching model for I.36; boundaries A-B-C-D, E-F-G-H and bridge E-B-C-H."""
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
    if type(data) is not dict or set(data)!=set('ABCDEFGH'):raise ValueError('exact A B C D E F G H keys required')
    out={}
    for k,v in data.items():
        if type(v) is not list or len(v)!=2:raise ValueError('two-element point list required')
        out[k]=tuple(map(scalar,v))
    return out
def sub(p,q):return tuple(a-b for a,b in zip(p,q))
def dot(u,v):return sum(a*b for a,b in zip(u,v))
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def norm2(u):return dot(u,u)
def angle(u,v):
    if not norm2(u) or not norm2(v):raise ValueError('zero angle ray')
    d,c=dot(u,v),abs(cross(u,v));s=abs(d)+c
    return (d/s,c/s)
def encode(x):
    if isinstance(x,F):return str(x)
    if type(x) in (tuple,list):return [encode(y) for y in x]
    if type(x) is dict:return {k:encode(v) for k,v in x.items()}
    return x
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(t,a):return tuple(t*x for x in a)
def area(*ps):return abs(sum(cross(ps[i],ps[(i+1)%len(ps)]) for i in range(len(ps))))/2
def branch(t):
    if t==0:return 'identical'
    if abs(t)<1:return 'overlapping'
    if abs(t)==1:return 'touching'
    return 'separated'
def make_certificate(data):
    p=parse(data);A,B,C,D,E,Fp,G,H=(p[k] for k in 'ABCDEFGH')
    u=sub(C,B);v=sub(A,B);delta=cross(u,v)
    if not delta:raise ValueError('base or height degenerate')
    if sub(D,A)!=u:raise ValueError('first figure is not directed parallelogram')
    w=sub(G,Fp)
    if w!=u:raise ValueError('bases must be equal and equally directed')
    if sub(H,E)!=w:raise ValueError('second figure is not directed parallelogram')
    if cross(u,sub(Fp,B)):raise ValueError('lower support differs')
    if cross(u,sub(E,A)):raise ValueError('upper support differs')
    t=dot(sub(Fp,B),u)/norm2(u)
    s=dot(sub(E,A),u)/norm2(u)
    areas={'ABCD':area(A,B,C,D),'EFGH':area(E,Fp,G,H),'EBCH':area(E,B,C,H)}
    bridge={'EH_equals_BC_vector':sub(H,E),'BE_equals_CH_vector':sub(E,B),
            'CH_vector':sub(H,C),'BE_CH_cross':cross(sub(E,B),sub(H,C)),
            'first_I35_shared_base':'BC','second_I35_shared_base':'EH',
            'upper_shift':s,'lower_shift':t,'upper_case':branch(s),'lower_case':branch(t)}
    return encode({'schema':'euclid-i36-exact-v1','input':p,'base_squared':norm2(u),
                   'determinant':delta,'area':areas,'bridge':bridge})
def json_value(x):
    if type(x) is str:return
    if type(x) is list:
        for y in x:json_value(y)
        return
    if type(x) is dict and all(type(k) is str for k in x):
        for y in x.values():json_value(y)
        return
    raise ValueError('certificate must contain only JSON strings, lists, objects')
def verify_certificate(data,cert):
    try:
        expected=make_certificate(data);json_value(cert)
        return json.dumps(cert,sort_keys=True,ensure_ascii=False)==json.dumps(expected,sort_keys=True,ensure_ascii=False)
    except (ValueError,TypeError,OverflowError,RecursionError):return False
