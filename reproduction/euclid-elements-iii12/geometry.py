"""III.12: exact rational teaching model; finite checking, not a proof assistant."""
from dataclasses import dataclass
from fractions import Fraction as Q

def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,Q)): raise TypeError('int or Fraction required')
    return Q(x)
def point(p):
    if not isinstance(p,(list,tuple)) or len(p)!=2: raise ValueError('two coordinates required')
    return tuple(rational(x) for x in p)
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def distance2(a,b):
    v=sub(point(a),point(b));return dot(v,v)
@dataclass(frozen=True)
class Circle:
    center:tuple
    radius:Q
    def __post_init__(self):
        object.__setattr__(self,'center',point(self.center))
        object.__setattr__(self,'radius',rational(self.radius))
        if self.radius<=0:raise ValueError('positive radius required')
    def on_boundary(self,p):return distance2(self.center,p)==self.radius**2

def relation(a,b):
    d2=distance2(a.center,b.center)
    if d2==0:return 'coincident' if a.radius==b.radius else 'concentric_disjoint'
    if d2<(a.radius-b.radius)**2:return 'strictly_nested'
    if d2==(a.radius-b.radius)**2:return 'internal_tangent'
    if d2<(a.radius+b.radius)**2:return 'secant'
    if d2==(a.radius+b.radius)**2:return 'external_tangent'
    return 'separate'
def interiors_disjoint(a,b):
    """Modern disk-interior disjointness criterion; positive radii checked by Circle.
    Its geometric equivalence to d>=R+r is justified in the prose, not by this code.
    """
    return distance2(a.center,b.center)>=(a.radius+b.radius)**2

def verify_contact(a,b,t):
    """Premises: disjoint open disks and independently supplied common boundary point.
    Do NOT require equality, collinearity or betweenness as input premises.
    """
    t=point(t)
    if not interiors_disjoint(a,b):raise ValueError('disk interiors overlap')
    if not a.on_boundary(t) or not b.on_boundary(t):raise ValueError('not a common boundary point')
    v=sub(b.center,a.center);w=sub(t,a.center);d2=dot(v,v)
    metric=d2==(a.radius+b.radius)**2
    determinant=cross(v,w);projection=dot(v,w)
    between=0<projection<d2
    if not (metric and determinant==0 and between):raise ArithmeticError('III.12 conclusion failed')
    return {'common_boundary':True,'interiors_disjoint':True,'distance2':d2,'radius_sum2':(a.radius+b.radius)**2,'cross':determinant,'projection':projection,'strictly_between':between}

def contact_candidate(a,b):
    """Separate construction, not premise checking or proof by sampling."""
    if relation(a,b)!='external_tangent':raise ValueError('external tangent pair required')
    return tuple(x+a.radius*(y-x)/(a.radius+b.radius) for x,y in zip(a.center,b.center))

def grid():
    directions=[(1,0),(0,1),(-1,0),(0,-1),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]
    count=0
    for shift in [(0,0),(2,-3),(-7,5),(Q(1,3),Q(-2,7))]:
      for u in directions:
       for R in [Q(1,2),Q(1),Q(3),Q(7,3)]:
        for r in [Q(i,5) for i in range(1,11)]:
         a=Circle(shift,R);b=Circle(tuple(shift[i]+(R+r)*u[i] for i in range(2)),r)
         t=tuple(shift[i]+R*u[i] for i in range(2))
         verify_contact(a,b,t);verify_contact(b,a,t)
         if contact_candidate(a,b)!=t or contact_candidate(b,a)!=t:raise ArithmeticError('candidate mismatch')
         count+=1
    return count
