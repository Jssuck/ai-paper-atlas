"""Exact rational circle-pair classification: a modern teaching reconstruction."""
from fractions import Fraction as F
from math import isqrt

def scalar(x):
    if isinstance(x,bool) or not isinstance(x,(int,str,F)):
        raise ValueError('expected integer, rational string, or Fraction')
    try:return F(x)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('invalid rational') from e

def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2:raise ValueError('expected 2D point')
    return tuple(map(scalar,p))

def circle(center,radius_squared):
    o=point(center);r=scalar(radius_squared)
    if r<=0:raise ValueError('radius squared must be positive')
    return o,r

def sqdist(a,b):return sum((x-y)**2 for x,y in zip(point(a),point(b)))

def classify(o1,r1,o2,r2):
    """r1,r2 are squared radii, not radii. No tolerance or floating point."""
    a,R=circle(o1,r1);b,S=circle(o2,r2)
    v=(b[0]-a[0],b[1]-a[1]);D=sum(x*x for x in v)
    if D==0:
        return {'kind':'coincident' if R==S else 'concentric-disjoint','count':None if R==S else 0}
    T=R-S+D;N=4*D*R-T*T
    h=(a[0]+T*v[0]/(2*D),a[1]+T*v[1]/(2*D))
    return {'kind':'secant' if N>0 else 'tangent' if N==0 else 'disjoint',
            'count':2 if N>0 else 1 if N==0 else 0,
            'direction':v,'distance_squared':D,'radical_constant':T,
            'discriminant':N,'foot':h}

def rational_intersections(o1,r1,o2,r2):
    """Return exact points only when coordinates are rational; None means irrational/infinite."""
    c=classify(o1,r1,o2,r2)
    if c['count']==0:return ()
    if c['count'] is None:return None
    h=c['foot'];N=c['discriminant']
    if N==0:return (h,)
    p,q=isqrt(N.numerator),isqrt(N.denominator)
    if p*p!=N.numerator or q*q!=N.denominator:return None
    k=F(p,q)/(2*c['distance_squared']);x,y=c['direction']
    return ((h[0]-k*y,h[1]+k*x),(h[0]+k*y,h[1]-k*x))

def same_circle_from_three(points,o1,r1,o2,r2):
    """Check supplied common points; noncollinearity gives equal circle parameters."""
    if not isinstance(points,(list,tuple)) or len(points)!=3:raise ValueError('exactly three points required')
    A,B,C=map(point,points)
    det=(B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0])
    if det==0:raise ValueError('three noncollinear points required')
    a,R=circle(o1,r1);b,S=circle(o2,r2)
    if any(sqdist(p,a)!=R or sqdist(p,b)!=S for p in (A,B,C)):
        raise ValueError('points are not common to both supplied circles')
    return {'determinant':det,'equal_centers':a==b,'equal_squared_radii':R==S}

def printable(obj):
    if isinstance(obj,F):return str(obj)
    if isinstance(obj,dict):return {k:printable(v) for k,v in obj.items()}
    if isinstance(obj,(tuple,list)):return [printable(v) for v in obj]
    return obj
