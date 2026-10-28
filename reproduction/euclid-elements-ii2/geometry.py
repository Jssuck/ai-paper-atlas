"""Original exact rational teaching model of Euclid, Elements II.2.
Not a formalization of Euclid's axiom system or a proof by numerical sampling.
"""
from fractions import Fraction as Q

def scalar(x):
    if type(x) not in (int,Q):raise ValueError('exact int or Fraction required')
    return Q(x)
def point(p):
    if type(p) not in (tuple,list) or len(p)!=2:raise ValueError('two coordinates required')
    return tuple(scalar(x) for x in p)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def mul(t,a):return (t*a[0],t*a[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area(p):
    return abs(sum((det(p[i],p[(i+1)%len(p)]) for i in range(len(p))),Q(0)))/2

def inputs(A,B,D,t):
    A,B,D=map(point,(A,B,D));t=scalar(t)
    u,v=sub(B,A),sub(D,A)
    if dot(u,u)==0:raise ValueError('nonzero AB required')
    if dot(u,v)!=0:raise ValueError('AB and AD must be perpendicular')
    if dot(u,u)!=dot(v,v):raise ValueError('AB and AD must have equal lengths')
    if not 0<t<1:raise ValueError('cut must be strictly interior')
    return A,B,D,t,u,v

def construct(A,B,D,t):
    A,B,D,t,u,v=inputs(A,B,D,t)
    C=add(A,mul(t,u));E=add(B,v);F=add(C,v)
    return {'points':{'A':A,'B':B,'C':C,'D':D,'E':E,'F':F},
            'square':(A,D,E,B),'AF':(A,D,F,C),'CE':(C,F,E,B)}

def verify(A,B,D,t,cert):
    """Verify point binding and ordered strips before computing shoelace areas.
    The affine coordinates are a modern certificate: [0,t] and [t,1]
    have disjoint interiors and cover [0,1]; height is identical [0,1].
    """
    try:
        A,B,D,t,u,v=inputs(A,B,D,t)
        if type(cert)!=dict or set(cert)!={'points','square','AF','CE'}:return False
        if type(cert['points'])!=dict or set(cert['points'])!=set('ABCDEF'):return False
        p={k:point(w) for k,w in cert['points'].items()}
        if (p['A'],p['B'],p['D'])!=(A,B,D):return False
        # Invert the nonsingular frame, independently checking each named location.
        delta=det(u,v)
        expected={'A':(0,0),'B':(1,0),'C':(t,0),'D':(0,1),'E':(1,1),'F':(t,1)}
        for name,xy in expected.items():
            w=sub(p[name],A)
            if (det(w,v)/delta,det(u,w)/delta)!=xy:return False
        regions={}
        for name,labels in [('square','ADEB'),('AF','ADFC'),('CE','CFEB')]:
            r=tuple(point(w) for w in cert[name]);regions[name]=r
            if r!=tuple(p[k] for k in labels):return False
            e=[sub(r[(i+1)%4],r[i]) for i in range(4)]
            if any(dot(w,w)==0 for w in e):return False
            if any(dot(e[i],e[(i+1)%4])!=0 for i in range(4)):return False
            if add(e[0],e[2])!=(0,0) or add(e[1],e[3])!=(0,0):return False
        # CF is common boundary, not duplicated interior; order is part of certificate.
        if (regions['AF'][3],regions['AF'][2])!=(regions['CE'][0],regions['CE'][1]):return False
        return area(regions['square'])==area(regions['AF'])+area(regions['CE'])
    except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError):return False

def summary(A,B,D,t):
    c=construct(A,B,D,t)
    if not verify(A,B,D,t,c):raise RuntimeError('certificate rejected')
    return {name:str(area(c[name])) for name in ('square','AF','CE')}
