"""I.44 exact coordinate teaching model; not a formal Euclidean prover."""
from fractions import Fraction as F

def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)): raise TypeError('exact int or Fraction required')
    return F(x)
def add(u,v): return (u[0]+v[0],u[1]+v[1])
def sub(u,v): return (u[0]-v[0],u[1]-v[1])
def mul(t,u): return (t*u[0],t*u[1])
def det(u,v): return u[0]*v[1]-u[1]*v[0]
def dot(u,v): return u[0]*v[0]+u[1]*v[1]
def area(points):
    return abs(sum(det(p,points[(i+1)%len(points)]) for i,p in enumerate(points)))/2

def construct(a,b,S,p,q):
    a,b,S,p,q=map(rational,(a,b,S,p,q))
    if min(a,b,S,q)<=0: raise ValueError('a,b,S,q must be positive: nondegenerate prescribed configuration')
    v=(S*p/(b*q),S/b); z=(F(0),F(0))
    pts={'A':(-a,F(0)),'B':z,'E':(b,F(0)),'G':v}
    pts['F']=add(pts['E'],v);pts['H']=add(pts['A'],v)
    pts['M']=mul(-b/a,v);pts['L']=add(pts['A'],pts['M']);pts['K']=add(pts['E'],pts['M'])
    cert={'parameters':(a,b,S,p,q),'points':pts,'v':v}
    if not verify(cert): raise ArithmeticError('construction invariant failed')
    return cert

def verify(c):
    try:
        a,b,S,p,q=c['parameters'];P=c['points'];v=c['v']
        if any(type(t) not in (int,F) or isinstance(t,bool) for t in (a,b,S,p,q)):return False
        if min(a,b,S,q)<=0:return False
        if v!=(S*p/(b*q),S/b):return False
        expected={'A':(-a,0),'B':(0,0),'E':(b,0),'G':v,'F':add((b,0),v),'H':add((-a,0),v),'M':mul(-b/a,v),'L':add((-a,0),mul(-b/a,v)),'K':add((b,0),mul(-b/a,v))}
        if any(len(w)!=2 or any(isinstance(t,bool) or not isinstance(t,(int,F)) for t in w) for w in list(P.values())+[v]):return False
        if set(P)!=set(expected) or any(P[k]!=expected[k] for k in P):return False
        poly=lambda names:area([P[k] for k in names])
        # B is between H and K; E between F and K. These are strict.
        if P['K']!=add(P['H'],mul((a+b)/a,sub(P['B'],P['H']))):return False
        if P['K']!=add(P['E'],mul(-b/a,sub(P['F'],P['E']))):return False
        if not(poly('BEFG')==poly('ABML')==S):return False
        if det(sub(P['L'],P['H']),sub(P['K'],P['F']))!=0:return False
        if det(sub(P['F'],P['H']),sub(P['K'],P['L']))!=0:return False
        # Angle ABM equals EBG: both rays reversed with positive scales.
        if sub(P['A'],P['B'])!=(-a/b*sub(P['E'],P['B'])[0],0):return False
        if sub(P['M'],P['B'])!=mul(-b/a,sub(P['G'],P['B'])):return False
        return True
    except (KeyError,TypeError,ValueError,ZeroDivisionError):return False
