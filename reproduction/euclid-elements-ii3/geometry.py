"""Exact rational teaching certificate for Euclid II.3, not a formal proof assistant."""
from fractions import Fraction as Q

def scalar(x):
    if type(x) not in (int,Q): raise ValueError('exact int or Fraction required')
    return Q(x)
def point(p):
    if type(p) not in (tuple,list) or len(p)!=2: raise ValueError('two coordinates required')
    return tuple(scalar(x) for x in p)
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(t,a): return (t*a[0],t*a[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def area(p): return abs(sum((det(p[i],p[(i+1)%len(p)]) for i in range(len(p))),Q(0)))/2

def inputs(A,u,v,t):
    A,u,v=map(point,(A,u,v));t=scalar(t)
    if dot(u,u)==0: raise ValueError('nonzero AB required')
    if not 0<t<1: raise ValueError('strictly internal cut required')
    if dot(u,v)!=0: raise ValueError('height must be perpendicular to AB')
    if dot(v,v)!=(1-t)**2*dot(u,u): raise ValueError('height must equal CB, not AB or AC')
    return A,u,v,t

def construct(A,u,v,t):
    A,u,v,t=inputs(A,u,v,t)
    B=add(A,u);C=add(A,mul(t,u));F=add(A,v);D=add(C,v);E=add(B,v)
    return {'points':dict(A=A,B=B,C=C,D=D,E=E,F=F),
            'AE':(A,F,E,B),'AD':(A,F,D,C),'CE':(C,D,E,B)}

def verify(A,u,v,t,cert):
    """Invert a nonsingular affine frame to check labels and complete ordered strips.
    Strict t and matching vertex cycles enforce coverage, not merely equal areas.
    The final equality is independently computed with the shoelace formula.
    """
    try:
        A,u,v,t=inputs(A,u,v,t)
        if type(cert)!=dict or set(cert)!={'points','AE','AD','CE'}: return False
        if type(cert['points'])!=dict or set(cert['points'])!=set('ABCDEF'): return False
        p={k:point(w) for k,w in cert['points'].items()}
        delta=det(u,v)
        expected={'A':(0,0),'B':(1,0),'C':(t,0),'F':(0,1),'D':(t,1),'E':(1,1)}
        for name,xy in expected.items():
            w=sub(p[name],A)
            if (det(w,v)/delta,det(u,w)/delta)!=xy: return False
        regions={}
        for name,labels in [('AE','AFEB'),('AD','AFDC'),('CE','CDEB')]:
            if type(cert[name]) not in (list,tuple) or len(cert[name])!=4: return False
            r=tuple(point(w) for w in cert[name]);regions[name]=r
            if r!=tuple(p[k] for k in labels): return False
            e=[sub(r[(i+1)%4],r[i]) for i in range(4)]
            if any(dot(w,w)==0 for w in e): return False
            if any(dot(e[i],e[(i+1)%4])!=0 for i in range(4)): return False
            if add(e[0],e[2])!=(0,0) or add(e[1],e[3])!=(0,0): return False
        square=regions['CE'];edges=[sub(square[(i+1)%4],square[i]) for i in range(4)]
        if len({dot(e,e) for e in edges})!=1: return False
        if (regions['AD'][3],regions['AD'][2])!=(regions['CE'][0],regions['CE'][1]): return False
        return area(regions['AE'])==area(regions['AD'])+area(regions['CE'])
    except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError): return False

def summary(A,u,v,t):
    cert=construct(A,u,v,t)
    if not verify(A,u,v,t,cert): raise RuntimeError('certificate rejected')
    return {name:str(area(cert[name])) for name in ('AE','AD','CE')}
