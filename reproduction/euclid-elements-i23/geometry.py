"""I.23 exact coordinate reconstruction, not Euclid's original algorithm."""
from fractions import Fraction as Q
import json

def rat(x):
    if type(x) not in (int,str,Q): raise ValueError('exact rational required')
    try:return Q(x)
    except (ValueError,ZeroDivisionError):raise ValueError('invalid rational') from None

def point(p):
    if type(p) not in (list,tuple) or len(p)!=2:raise ValueError('two coordinates required')
    return tuple(rat(x) for x in p)

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def perpendicular(w):return (-w[1],w[0])
def encode(p):return [str(x) for x in p]

def construct(C,D,E,A,B,side=1):
    C,D,E,A,B=map(point,(C,D,E,A,B))
    if type(side) is not int or side not in (-1,1):raise ValueError('side must be integer +/-1')
    u,v,w=sub(D,C),sub(E,C),sub(B,A)
    U,V,W=dot(u,u),dot(v,v),dot(w,w)
    T,X=dot(u,v),cross(v,u)
    if not U or not V or not W:raise ValueError('zero ray')
    if not X:raise ValueError('ordinary nondegenerate angle required')
    d=V/W;p=T/V;q=side*abs(X)/V;j=perpendicular(w)
    # F=A+sqrt(d)*f; G=A+sqrt(d)*g, with rational f and g.
    g=w;f=tuple(p*w[i]+q*j[i] for i in range(2))
    checks={'AF2':d*dot(f,f),'AG2':d*dot(g,g),'FG2':d*dot(sub(g,f),sub(g,f)),
            'AF_dot_AG':d*dot(f,g),'AG_cross_AF':d*cross(g,f)}
    expected={'AF2':U,'AG2':V,'FG2':dot(sub(v,u),sub(v,u)),
              'AF_dot_AG':T,'AG_cross_AF':side*abs(X)}
    if checks!=expected:raise ArithmeticError('exact identities failed')
    return {'schema_version':1,'input':dict(zip(('C','D','E','A','B'),map(encode,(C,D,E,A,B)))),
            'side':side,'radicand':str(d),'F':{'constant':encode(A),'sqrt_coefficient':encode(f)},
            'G':{'constant':encode(A),'sqrt_coefficient':encode(g)},
            'checks':{k:str(v) for k,v in checks.items()},'source_cross':str(X),
            'ordinary_angle_preserved':True,'signed_orientation_preserved':side==(1 if X>0 else -1)}

def strict_json(x):
    if x is None or type(x) in (str,bool,int):return
    if type(x) is list:
        for v in x:strict_json(v)
        return
    if type(x) is dict and all(type(k) is str for k in x):
        for v in x.values():strict_json(v)
        return
    raise ValueError('noncanonical JSON type')

def verify(certificate,C,D,E,A,B,side=1):
    try:
        strict_json(certificate)
        expected=construct(C,D,E,A,B,side)
        return json.dumps(certificate,sort_keys=True,separators=(',',':'))==json.dumps(expected,sort_keys=True,separators=(',',':'))
    except (ValueError,TypeError,ZeroDivisionError,OverflowError):return False
