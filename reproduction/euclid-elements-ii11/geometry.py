"""Exact teaching model of Elements II.11. No floating-point proof checks."""
from dataclasses import dataclass
from fractions import Fraction as F

def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise ValueError('expected int or Fraction, not bool/float')
    return F(x)

@dataclass(frozen=True)
class Q5:
    p: F = F(0)
    q: F = F(0)
    def __post_init__(self):
        object.__setattr__(self,'p',rational(self.p));object.__setattr__(self,'q',rational(self.q))
    @staticmethod
    def coerce(x):return x if isinstance(x,Q5) else Q5(rational(x))
    def __add__(self,o):
        o=self.coerce(o);return Q5(self.p+o.p,self.q+o.q)
    __radd__=__add__
    def __neg__(self):return Q5(-self.p,-self.q)
    def __sub__(self,o):return self+-self.coerce(o)
    def __rsub__(self,o):return self.coerce(o)+-self
    def __mul__(self,o):
        o=self.coerce(o);return Q5(self.p*o.p+5*self.q*o.q,self.p*o.q+self.q*o.p)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.coerce(o);d=o.p*o.p-5*o.q*o.q
        if not d:raise ZeroDivisionError('zero divisor')
        return self*Q5(o.p/d,-o.q/d)
    def __pow__(self,n):
        if type(n)!=int or n<0:raise ValueError('nonnegative integral exponent required')
        r=Q5(1)
        for _ in range(n):r=r*self
        return r
    def sign(self):
        p,q=self.p,self.q
        if not q:return (p>0)-(p<0)
        if not p:return (q>0)-(q<0)
        if p>0 and q>0:return 1
        if p<0 and q<0:return -1
        d=p*p-5*q*q
        return ((d>0)-(d<0))*(1 if p>0 else -1)
    def __lt__(self,o):return (self-self.coerce(o)).sign()<0
    def __le__(self,o):return (self-self.coerce(o)).sign()<=0
    def __gt__(self,o):return (self-self.coerce(o)).sign()>0
    def __ge__(self,o):return (self-self.coerce(o)).sign()>=0
    def __str__(self):return f'{self.p} + ({self.q})*sqrt(5)'

def vector(x):
    if not isinstance(x,(tuple,list)) or len(x)!=2:raise ValueError('two rational coordinates required')
    return tuple(rational(t) for t in x)
def dot(u,v):return sum(x*y for x,y in zip(u,v))
def sub(u,v):return tuple(x-y for x,y in zip(u,v))
def distance2(u,v):return dot(sub(u,v),sub(u,v))
def area(points):
    s=Q5(0)
    for a,b in zip(points,points[1:]+points[:1]):s+=a[0]*b[1]-a[1]*b[0]
    return (s if s>=0 else -s)/2

def parameters(a,origin,u,v):
    a=rational(a);origin=vector(origin);u=vector(u);v=vector(v)
    if a<=0:raise ValueError('a must be positive')
    s=dot(u,u)
    if not s or dot(v,v)!=s or dot(u,v)!=0:raise ValueError('nonzero equal orthogonal basis required')
    return a,origin,u,v,s

def canonical_points(a,origin,u,v):
    x=Q5(-a/2,a/2)
    local={'A':(0,0),'B':(a,0),'C':(0,a),'D':(a,a),'E':(0,a/2),'F':(0,-x),'G':(x,-x),'H':(x,0),'K':(x,a)}
    return {k:tuple(Q5(origin[j])+u[j]*Q5.coerce(z[0])+v[j]*Q5.coerce(z[1]) for j in range(2)) for k,z in local.items()}

def make_certificate(a,origin=(0,0),u=(1,0),v=(0,1)):
    a,origin,u,v,_=parameters(a,origin,u,v)
    return dict(a=a,origin=origin,u=u,v=v,points=canonical_points(a,origin,u,v))

def validate_certificate(c):
    if not isinstance(c,dict) or set(c)!={'a','origin','u','v','points'}:raise ValueError('certificate fields')
    a,o,u,v,s=parameters(c['a'],c['origin'],c['u'],c['v'])
    pts=c['points'];expected=canonical_points(a,o,u,v)
    if not isinstance(pts,dict) or set(pts)!=set(expected):raise ValueError('point fields')
    for name,p in pts.items():
        if not isinstance(p,(tuple,list)) or len(p)!=2 or any(type(t)!=Q5 for t in p):raise ValueError('exact Q5 point required')
        if tuple(p)!=expected[name]:raise ValueError('construction point mismatch: '+name)
    A,B,C,D,E,Fp,G,H,K=[pts[k] for k in ['A','B','C','D','E','F','G','H','K']]
    x=Q5(-a/2,a/2)
    if not 0<x<a:raise ValueError('H not strictly interior')
    m={'x':x,'scale2':s,'EF2':distance2(E,Fp),'EB2':distance2(E,B),'AE2':distance2(A,E),'square_AB':distance2(A,B)}
    m['II6_left']=(a+x)*x*s+m['AE2']
    m.update(FK=area([Fp,G,K,C]),AK=area([A,H,K,C]),FH=area([Fp,G,H,A]),HD=area([H,B,D,K]))
    m['target_left']=a*(a-x)*s;m['target_right']=x*x*s
    checks=[(m['EF2'],m['EB2']),(m['II6_left'],m['EF2']),(m['square_AB']+m['AE2'],m['EB2']),(m['FK'],m['square_AB']),(m['FK']-m['AK'],m['FH']),(m['square_AB']-m['AK'],m['HD']),(m['FH'],m['HD']),(m['target_left'],m['target_right']),(distance2(A,Fp),distance2(Fp,G)),(distance2(A,H),distance2(A,Fp))]
    for left,right in checks:
        if left!=right:raise ValueError('proof identity failed')
    if dot(sub(A,Fp),sub(G,Fp))!=Q5(0):raise ValueError('FH right angle failed')
    return m
