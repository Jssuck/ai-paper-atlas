"""Exact Euclidean coordinate teaching model for I.35; boundaries A-B-C-D and E-B-C-F."""
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
    if type(data) is not dict or set(data)!=set('ABCDEF'):raise ValueError('exact A B C D E F keys required')
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
def make_certificate(data):
    p=parse(data);A,B,C,D,E,H=(p[k] for k in 'ABCDEF')
    u,v=sub(C,B),sub(A,B);delta=cross(u,v)
    if not delta:raise ValueError('base or height degenerate')
    if sub(D,A)!=u or sub(H,E)!=u:raise ValueError('paired upper edges must equal directed base')
    if cross(u,sub(E,A)):raise ValueError('upper supports differ')
    t=dot(sub(E,A),u)/norm2(u)
    # Swap the two figures for negative displacement; this is a labeled symmetry.
    if t<0:A,D,E,H=E,H,A,D;t=-t;swap='yes'
    else:swap='no'
    S=area(A,B,C,D);T=area(E,B,C,H)
    cut={'normalized_shift':t,'swapped':swap,'triangle_EAB':area(E,A,B),'triangle_FDC':area(H,D,C)}
    if t==0:cut.update({'case':'identical','common':S})
    elif t<=1:
        common=area(B,C,D,E)
        cut.update({'case':'touching' if t==1 else 'overlapping','common_BCDE':common,'first_reassembled':area(E,A,B)+common,'second_reassembled':area(H,D,C)+common})
    else:
        G=add(B,mul(1/t,sub(E,B)))
        overlap=area(D,G,E);bottom=area(G,B,C)
        cut.update({'case':'separated','G':G,'G_on_BE_cross':cross(sub(G,B),sub(E,B)),'G_on_DC_cross':cross(sub(G,D),sub(C,D)),'removed_DGE':overlap,'added_GBC':bottom,'first_reassembled':area(E,A,B)-overlap+bottom,'second_reassembled':area(H,D,C)-overlap+bottom})
    return encode({'schema':'euclid-i35-exact-v1','input':p,'signed_shift':dot(sub(p['E'],p['A']),u)/norm2(u),'base_squared':norm2(u),'determinant':delta,'area':{'ABCD':S,'EBCF':T},'cut':cut})
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
