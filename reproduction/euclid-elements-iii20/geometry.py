"""Exact rational teaching model of III.20 plus explicitly modern arc extension."""
from fractions import Fraction as F
from itertools import permutations
from collections import Counter

def point(p):
    if len(p)!=2 or any(not isinstance(x,(int,F)) or isinstance(x,bool) for x in p):
        raise ValueError('points require two exact integers or Fractions')
    return tuple(F(x) for x in p)
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sign(x):return (x>0)-(x<0)
def rational_point(t):
    if t is None:return (F(-1),F(0))
    t=F(t);return ((1-t*t)/(1+t*t),2*t/(1+t*t))
def evaluate(A,B,C,O=(0,0)):
    A,B,C,O=map(point,(A,B,C,O));a,b,c=[sub(x,O) for x in (A,B,C)]
    r2=dot(a,a)
    if not r2 or dot(b,b)!=r2 or dot(c,c)!=r2:raise ValueError('one nonzero circle required')
    if len({A,B,C})!=3:raise ValueError('three distinct circle points required')
    u,v=sub(B,A),sub(C,A);d,k=dot(u,v),cross(u,v)
    den=dot(u,u)*dot(v,v)
    # Left of directed chord B->C selects its counterclockwise arc, and vice versa.
    orientation=sign(cross(sub(C,B),sub(A,B)))
    central=(dot(b,c)/r2,orientation*cross(b,c)/r2)
    doubled=((d*d-k*k)/den,2*d*abs(k)/den)
    # Barycentric ray coefficients locate O in the ordinary angle BAC.
    w=sub(O,A);lam,mu=cross(w,v)/k,cross(u,w)/k
    location='inside' if lam>0 and mu>0 else ('boundary' if lam>=0 and mu>=0 else 'outside')
    arc='minor' if d>0 else ('major' if d<0 else 'semicircle')
    return dict(central=central,doubled=doubled,arc=arc,orientation=orientation,center_location=location,side_through_center=(lam==0 or mu==0),base_diameter=(b[0]==-c[0] and b[1]==-c[1]))
def check(A,B,C,O=(0,0)):
    r=evaluate(A,B,C,O)
    if r['central']!=r['doubled']:raise ArithmeticError('double-angle mismatch')
    return r
def sample_points():return [rational_point(F(i,2)) for i in range(-4,5)]+[rational_point(None)]
def transform(p,kind):
    x,y=p
    if kind==0:return (x,y)
    if kind==1:return (3+2*y,-2-2*x) # rotate, scale and translate
    if kind==2:return (F(2,3)-3*x,F(-5,7)+3*y) # reflection, scale, translation
    raise ValueError('unknown transform')
def grid():
    counts=Counter();n=0
    for triple in permutations(sample_points(),3):
        for kind in range(3):
            r=check(*(transform(p,kind) for p in triple),O=transform((0,0),kind));n+=1
            for field in ('arc','center_location'):counts[field+':'+r[field]]+=1
            for field in ('side_through_center','base_diameter'):
                if r[field]:counts[field]+=1
    return {'cases':n,'counts':dict(sorted(counts.items()))}
EXAMPLES={
 'addition':((0,1),(-1,0),(F(3,5),F(-4,5))),
 'subtraction':((1,0),(F(-3,5),F(4,5)),(0,1)),
 'side_boundary':((1,0),(-1,0),(0,-1)),
 'base_diameter':((0,1),(-1,0),(1,0)),
 'reflex_extension':((0,1),(-1,0),(F(3,5),F(4,5))),
}
