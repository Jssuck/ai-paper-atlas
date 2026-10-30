"""Original exact teaching model of Euclid III.22; not a formal proof assistant."""
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations

def scalar(x):
    if type(x) not in (int,F): raise TypeError('integer or Fraction required')
    return F(x)
def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2: raise ValueError('two coordinates required')
    return tuple(scalar(x) for x in p)
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def cot(a,b,c):
    """cot of the NONREFLEX angle ABC, with exact sign of dot retained."""
    u,v=sub(a,b),sub(c,b); s=abs(cross(u,v))
    if not s: raise ValueError('degenerate angle')
    return dot(u,v)/s

def certificate(vertices, center=(0,0), radius2=1):
    q=tuple(point(p) for p in vertices); o=point(center); r=scalar(radius2)
    if len(q)!=4 or len(set(q))!=4: raise ValueError('four distinct vertices required')
    if r<=0: raise ValueError('positive radius squared required')
    if any(dot(sub(p,o),sub(p,o))!=r for p in q): raise ValueError('not on the specified circle')
    turns=[cross(sub(q[(i+1)%4],q[i]),sub(q[(i+2)%4],q[(i+1)%4])) for i in range(4)]
    if not(all(t>0 for t in turns) or all(t<0 for t in turns)): raise ValueError('strict convex boundary order required')
    a,b,c,d=q
    angles=tuple(cot(q[(i-1)%4],q[i],q[(i+1)%4]) for i in range(4))
    # Two III.21 substitutions in triangle ABC, with diagonal BD splitting ADC.
    bac,bdc=cot(b,a,c),cot(b,d,c)
    acb,adb=cot(a,c,b),cot(a,d,b)
    # Cotangent addition computed independently from the triangle angles.
    denom=bac+acb
    if denom<=0: raise ArithmeticError('triangle angle sum domain failed')
    merged=(bac*acb-1)/denom
    return dict(cots=angles,opposite_sums=(angles[0]+angles[2],angles[1]+angles[3]),
                same_segment=(bac==bdc,acb==adb),split_cot=merged,
                split_matches_D=merged==angles[3],triangle_sum=merged+angles[1],
                orientation=1 if turns[0]>0 else -1)

def circle_points():
    ts=[F(-4),F(-3),F(-2),F(-1),F(-1,2),F(0),F(1,2),F(1),F(2),F(3),F(4)]
    pts=[((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in ts]+[(F(-1),F(0))]
    def half(p): return 0 if p[1]>0 or (p[1]==0 and p[0]>=0) else 1
    def cmp(a,b):
        if half(a)!=half(b): return -1 if half(a)<half(b) else 1
        z=cross(a,b); return -1 if z>0 else (1 if z<0 else 0)
    return sorted(pts,key=cmp_to_key(cmp))

def configurations():
    for q in combinations(circle_points(),4):
        for o,s in [((0,0),F(1)),((3,-2),F(5)),((-1,4),F(1,7))]:
            p=tuple((o[0]+s*x,o[1]+s*y) for x,y in q)
            yield p,o,s*s
            yield tuple(reversed(p)),o,s*s

def grid():
    n=right=obtuse=0
    for q,o,r in configurations():
        z=certificate(q,o,r)
        if z['opposite_sums']!=(0,0) or z['same_segment']!=(True,True) or not z['split_matches_D'] or z['triangle_sum']!=0:
            raise ArithmeticError('III.22 check failed')
        n+=1; right+=any(x==0 for x in z['cots']); obtuse+=any(x<0 for x in z['cots'])
    return dict(configurations=n,opposite_pairs=2*n,same_segment_equalities=2*n,right_angle_configurations=right,obtuse_angle_configurations=obtuse)
