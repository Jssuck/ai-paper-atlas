"""Exact Euclidean coordinate teaching model for I.34; boundary A-C-D-B."""
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
def make_certificate(data):
    p=parse(data);A,B,C,D=(p[k] for k in 'ABCD')
    ab,ac,cd,bd=sub(B,A),sub(C,A),sub(D,C),sub(D,B)
    if not norm2(ab) or not norm2(ac) or not norm2(cd) or not norm2(bd):raise ValueError('zero side')
    det=cross(ab,ac)
    if not det:raise ValueError('degenerate supporting lines')
    if cross(ab,cd) or cross(ac,bd):raise ValueError('both opposite pairs must be parallel')
    # Distinct opposite supporting lines plus consistency imply a genuine parallelogram.
    if not cross(ab,sub(C,A)) or not cross(ac,sub(B,A)):raise ValueError('coincident support')
    bc=sub(C,B)
    ang=lambda X,Y,Z:angle(sub(p[X],p[Y]),sub(p[Z],p[Y]))
    return encode({'schema':'euclid-i34-exact-v1','input':p,
      'premises':{'AB_cross_CD':cross(ab,cd),'AC_cross_BD':cross(ac,bd),'AB_cross_AC':det},
      'alternate_angles':{'ABC':ang('A','B','C'),'BCD':ang('B','C','D'),'ACB':ang('A','C','B'),'CBD':ang('C','B','D')},
      'opposite_sides_squared':{'AB':norm2(ab),'CD':norm2(cd),'AC':norm2(ac),'BD':norm2(bd)},
      'opposite_angles':{'BAC':ang('B','A','C'),'CDB':ang('C','D','B'),'ABD':ang('A','B','D'),'ACD':ang('A','C','D')},
      'triangles':{'ABC_squared':[norm2(ab),norm2(bc),norm2(ac)],'DCB_squared':[norm2(cd),norm2(bc),norm2(bd)],
        'ABC_twice_area':abs(cross(sub(B,A),sub(C,A))),
        'DCB_twice_area':abs(cross(sub(C,D),sub(B,D))),
        'BC_side_A':cross(bc,sub(A,B)),'BC_side_D':cross(bc,sub(D,B))},
      'area':{'parallelogram':abs(det),'ABC':abs(det)/2,'DCB':abs(det)/2}})
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
