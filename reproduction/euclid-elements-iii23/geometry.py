"""III.23 modern rational teaching model, not Euclid's original algebra."""
from fractions import Fraction as F
from itertools import combinations
A=(F(-1),F(0)); B=(F(1),F(0))
def point(k,t):
    k,t=F(k),F(t)
    if not t: raise ValueError('base-line ray is degenerate')
    u=2*(1+k*t)/(1+t*t)
    if not u: raise ValueError('tangent at A: second point collapses')
    return (u-1,t*u)
def residual(k,p):
    x,y=map(F,p); return x*x+y*y-2*F(k)*y-1
def cot(p):
    x,y=map(F,p)
    if not y: raise ValueError('angle vertex must be off the base')
    return (x*x+y*y-1)/(2*abs(y))
def segment_cot(k,side):
    if side not in (-1,1): raise ValueError('side must be +1 or -1')
    return F(k)*side
def inside(k,p,side=1):
    if side not in (-1,1): raise ValueError('side must be +1 or -1')
    return side*p[1]>=0 and residual(k,p)<=0
def ordered_witness(k1,k2):
    k1,k2=F(k1),F(k2)
    if k1>=k2: raise ValueError('require k1 < k2')
    t=1/(2*(1+abs(k1)+abs(k2)))
    C,D=point(k1,t),point(k2,t)
    if not (0<C[1]<D[1] and A[0]<C[0]<D[0]):
        raise ArithmeticError('A-C-D order failed')
    if not (cot(C)<cot(D) and residual(k2,C)<0 and residual(k1,D)>0):
        raise ArithmeticError('strict nested/angle certificate failed')
    return dict(t=t,C=C,D=D,cot_C=cot(C),cot_D=cot(D))
def grid():
    ks=sorted({F(n,d) for d in range(1,5) for n in range(-8,9)})
    points=0
    for k in ks:
        for n in range(1,13):
            t=F(n,24*(1+abs(k)))
            for kk,tt,s in ((k,t,1),(-k,-t,-1)):
                p=point(kk,tt)
                if residual(kk,p)!=0 or s*p[1]<=0 or cot(p)!=segment_cot(kk,s):
                    raise ArithmeticError('on-circle angle/side mismatch')
                points+=1
    pairs=0
    for lo,hi in combinations(ks,2):
        ordered_witness(lo,hi);pairs+=1
    return dict(parameters=len(ks),on_circle_angle_checks=points,strict_nested_pairs=pairs)
