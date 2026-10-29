"""Exact rational teaching model, not a proof assistant or circle-intersection solver."""
from fractions import Fraction as Q
from dataclasses import dataclass

def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,Q)): raise TypeError('exact rational required')
    return Q(x)
def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2: raise TypeError('two coordinates required')
    return tuple(rational(x) for x in p)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def d2(a,b):return dot(sub(a,b),sub(a,b))
@dataclass(frozen=True)
class Circle:
    center:tuple
    radius:Q
    def __post_init__(self):
        object.__setattr__(self,'center',point(self.center));object.__setattr__(self,'radius',rational(self.radius))
        if self.radius<=0:raise ValueError('positive radius required')
def require_circle(c):
    if not isinstance(c,Circle):raise TypeError('Circle required')
def on(c,p):require_circle(c);return d2(c.center,point(p))==c.radius**2
def relation(a,b):
    require_circle(a);require_circle(b);s=d2(a.center,b.center);lo=(a.radius-b.radius)**2;hi=(a.radius+b.radius)**2
    if s==0:return 'coincident' if a.radius==b.radius else 'concentric_distinct'
    if s<lo:return 'strict_containment'
    if s==lo:return 'internal_contact'
    if s<hi:return 'two_intersections'
    if s==hi:return 'external_contact'
    return 'separate'
def contains(outer,inner):
    require_circle(outer);require_circle(inner)
    return outer.radius>=inner.radius and d2(outer.center,inner.center)<=(outer.radius-inner.radius)**2

def interiors_disjoint(a,b):
    require_circle(a);require_circle(b)
    return d2(a.center,b.center)>=(a.radius+b.radius)**2

def contact_certificate(a,b,t,kind):
    """Input premises: separation or proper containment AND a supplied common boundary point.
    The distance-sum/difference geometric equivalences are proved in the essay.
    Output conclusions use explicit checks, including under Python optimization.
    """
    require_circle(a);require_circle(b);t=point(t)
    if kind not in ('external','internal'):raise ValueError('unknown contact kind')
    if not on(a,t) or not on(b,t):raise ValueError('not a common boundary point')
    if kind=='external':
        if not interiors_disjoint(a,b):raise ValueError('interiors overlap')
        den=a.radius+b.radius
        expected=tuple((b.radius*x+a.radius*y)/den for x,y in zip(a.center,b.center))
    else:
        outer,inner=(a,b) if a.radius>=b.radius else (b,a)
        if outer==inner or not contains(outer,inner):raise ValueError('proper containment required')
        den=outer.radius-inner.radius
        if den<=0:raise RuntimeError('distinct nested contacting circles need unequal radii')
        expected=tuple(x+outer.radius*(y-x)/den for x,y in zip(outer.center,inner.center))
    if t!=expected:raise RuntimeError('unique-point formula failed')
    return {'kind':kind,'point':t,'unique_candidate':expected}

def same_contact(a,b,p,q,kind):
    """Both witnesses must satisfy premises independently, then compare conclusions."""
    x=contact_certificate(a,b,p,kind);y=contact_certificate(a,b,q,kind)
    if x['point']!=y['point']:raise RuntimeError('uniqueness failed')
    return True

def chord_midpoint_certificate(a,b,p,q):
    """For two distinct common boundary points, their midpoint is inside both disks."""
    require_circle(a);require_circle(b);p=point(p);q=point(q)
    if p==q:raise ValueError('distinct endpoints required')
    if not all(on(c,x) for c in (a,b) for x in (p,q)):raise ValueError('common boundary endpoints required')
    m=tuple((x+y)/2 for x,y in zip(p,q));gap=d2(p,q)/4
    for c in (a,b):
        actual=c.radius**2-d2(c.center,m)
        if actual!=gap or actual<=0:raise RuntimeError('strict chord identity failed')
    return {'midpoint':m,'strict_squared_gap':gap}
