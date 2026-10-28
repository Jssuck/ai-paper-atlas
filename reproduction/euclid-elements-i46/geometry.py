"""Original rational coordinate teaching model of Elements I.46; not ruler/compass simulation."""
from fractions import Fraction as Q

def scalar(x):
    if type(x) not in (int,Q): raise ValueError('coordinates must be integers or Fractions, not booleans/floats')
    return Q(x)
def point(p):
    if type(p) not in (tuple,list) or len(p)!=2: raise ValueError('point needs two coordinates')
    return tuple(map(scalar,p))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def scale(t,a): return (t*a[0],t*a[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def inputs(A,B,side):
    A,B=point(A),point(B)
    if type(side) is not int or side not in (-1,1): raise ValueError('side must be integer +1 or -1')
    if A==B: raise ValueError('zero base is excluded')
    return A,B,side

def construct(A,B,side=1):
    A,B,side=inputs(A,B,side); u=sub(B,A); w=(-side*u[1],side*u[0])
    # C is chosen beyond D, only to exhibit an available perpendicular ray.
    return {'points':{'A':A,'B':B,'C':add(A,scale(2,w)),'D':add(A,w),'E':add(B,w)},
            'side':side,'side_squared':dot(u,u)}

def verify(A,B,side,certificate):
    """Check geometric constraints directly; never calls construct. Reject malformed certificates."""
    A,B,side=inputs(A,B,side)
    try:
        if type(certificate) is not dict or set(certificate)!={'points','side','side_squared'}: return False
        if type(certificate['side']) is not int or certificate['side']!=side: return False
        p=certificate['points']
        if type(p) is not dict or set(p)!=set('ABCDE'):return False
        p={k:point(v) for k,v in p.items()}
        if p['A']!=A or p['B']!=B:return False
        u=sub(B,A);w=sub(p['D'],A);v=sub(p['C'],A); n=dot(u,u)
        if scalar(certificate['side_squared'])!=n:return False
        if dot(u,w)!=0 or dot(w,w)!=n or side*cross(u,w)<=0:return False
        if cross(v,w)!=0 or dot(v,w)<=n:return False # C lies strictly beyond D
        if cross(sub(p['E'],p['D']),u)!=0 or cross(sub(p['E'],B),w)!=0:return False
        poly=[p[k] for k in 'ADEB'];edges=[sub(poly[(i+1)%4],poly[i]) for i in range(4)]
        if any(dot(e,e)!=n for e in edges):return False
        if any(dot(edges[i],edges[(i+1)%4])!=0 for i in range(4)):return False
        turns=[cross(edges[i],edges[(i+1)%4]) for i in range(4)]
        if not (all(t>0 for t in turns) or all(t<0 for t in turns)):return False
        return True
    except (ValueError,TypeError,KeyError,IndexError):return False

def area(poly):
    p=[point(x) for x in poly]
    return abs(sum(cross(p[i],p[(i+1)%len(p)]) for i in range(len(p))))/Q(2)
