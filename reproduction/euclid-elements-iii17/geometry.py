"""III.17: rational-coordinate reconstruction, not a general real solver."""
from fractions import Fraction as Q
from math import isqrt

def q(x):
    if type(x) not in (int,Q): raise ValueError('exact int or Fraction required')
    return Q(x)
def point(p):
    if type(p) not in (tuple,list) or len(p)!=2: raise ValueError('two coordinates required')
    return tuple(q(x) for x in p)
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(t,a): return (t*a[0],t*a[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def norm(a): return dot(a,a)
def sqrtq(x):
    x=q(x)
    if x<0: raise ValueError('negative radicand')
    n,d=isqrt(x.numerator),isqrt(x.denominator)
    if n*n!=x.numerator or d*d!=x.denominator:
        raise ValueError('outside rational-square-root implementation domain')
    return Q(n,d)
def construct(radius,distance,center=(0,0),axis=(1,0),side=1):
    r,d=q(radius),q(distance); E=point(center); u=point(axis)
    if r<=0 or d<0 or norm(u)!=1: raise ValueError('invalid radius, distance or unit axis')
    if type(side)!=int or side not in (-1,1): raise ValueError('side must be +1 or -1')
    if d<r: raise ValueError('interior point: no tangent through it')
    A=add(E,mul(d,u)); v=(-u[1],u[0])
    if d==r:
        return dict(kind='boundary',r=r,d=d,E=E,A=A,B=A,direction=v)
    h=sqrtq(d*d-r*r)
    D=add(E,mul(r,u)); F=add(D,mul(side*h,v))
    B=add(E,mul(r/d,sub(F,E)))
    return dict(kind='exterior',r=r,d=d,E=E,A=A,D=D,F=F,B=B,direction=sub(A,B))
def verify(c):
    """Check explicit geometric identities; does not call construct."""
    try:
        if type(c)!=dict: return False
        kind=c['kind']; r=q(c['r']);d=q(c['d'])
        keys={'kind','r','d','E','A','B','direction'}
        if kind=='exterior': keys|={'D','F'}
        elif kind!='boundary':return False
        if set(c)!=keys or r<=0:return False
        E,A,B,w=(point(c[k]) for k in ('E','A','B','direction'))
        if norm(sub(A,E))!=d*d or norm(sub(B,E))!=r*r or norm(w)==0:return False
        if dot(sub(B,E),w)!=0:return False
        if kind=='boundary': return d==r and A==B
        if d<=r or w!=sub(A,B):return False
        D,F=point(c['D']),point(c['F'])
        return (D==add(E,mul(r/d,sub(A,E))) and norm(sub(F,E))==d*d
                and dot(sub(F,D),sub(A,E))==0
                and B==add(E,mul(r/d,sub(F,E)))
                and norm(sub(A,B))==norm(sub(D,F)))
    except (KeyError,TypeError,ValueError,ZeroDivisionError):return False

def line_power(c,t):
    t=q(t);X=add(c['B'],mul(t,c['direction']))
    return norm(sub(X,c['E']))-c['r']**2

def grid():
    count=certs=powers=0
    for r,d in [(3,5),(5,13),(8,17),(7,25),(20,29),(9,41)]:
      for scale in [Q(1,3),Q(1),Q(7,2)]:
       for E in [(0,0),(2,-3),(Q(1,7),Q(-5,11))]:
        for u in [(1,0),(0,1),(-1,0),(0,-1),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]:
         count+=1
         for side in [-1,1]:
          c=construct(scale*r,scale*d,E,u,side)
          if not verify(c):raise RuntimeError('invalid generated certificate')
          certs+=1
          for t in [-2,-1,0,1,2]:
           if line_power(c,t)!=t*t*norm(c['direction']):raise RuntimeError('line identity mismatch')
           powers+=1
    return dict(configurations=count,certificates=certs,power_checks=powers)
