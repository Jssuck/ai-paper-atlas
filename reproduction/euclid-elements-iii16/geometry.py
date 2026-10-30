"""Exact rational point/line certificates for the modern model of III.16.
Finite execution is not proof; no angle magnitude is assigned to a horn.
"""
from fractions import Fraction as F
from dataclasses import dataclass

def number(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):raise TypeError('exact int/Fraction required')
    return F(x)
def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2:raise TypeError('two coordinates required')
    return tuple(number(x) for x in p)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def scale(a,t):return (a[0]*t,a[1]*t)
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
@dataclass(frozen=True)
class Circle:
    center:tuple
    radius2:F
    def __post_init__(self):
        object.__setattr__(self,'center',point(self.center))
        object.__setattr__(self,'radius2',number(self.radius2))
        if self.radius2<=0:raise ValueError('positive squared radius required')
def power(c,p):
    v=sub(point(p),c.center)
    return dot(v,v)-c.radius2

def analyze(c,p,u):
    if not isinstance(c,Circle):raise TypeError('Circle required')
    p,u=point(p),point(u)
    if power(c,p)!=0:raise ValueError('contact must be on circle')
    q=dot(u,u)
    if not q:raise ValueError('nonzero direction required')
    k=dot(sub(c.center,p),u)
    foot_t=k/q;foot=add(p,scale(u,foot_t))
    d2=dot(sub(foot,c.center),sub(foot,c.center))
    kind='tangent' if k==0 else ('inward' if k>0 else 'outward')
    t2=2*k/q
    return {'point':p,'direction':u,'q':q,'k':k,'kind':kind,
            'foot_parameter':foot_t,'foot':foot,'distance2':d2,
            'second_parameter':None if k==0 else t2,
            'second_point':None if k==0 else add(p,scale(u,t2)),
            'interior_parameter':foot_t if k>0 else None,
            'interior_point':foot if k>0 else None,
            'interior_power':power(c,foot) if k>0 else None}

def verify(c,p,u,certificate):
    """Recompute exactly; reject altered/malformed certificate values, including bool."""
    expected=analyze(c,p,u)
    def signature(x):
        if isinstance(x,F):return ('fraction',x.numerator,x.denominator)
        if isinstance(x,tuple):return ('tuple',tuple(signature(v) for v in x))
        return (type(x).__name__,x)
    if not isinstance(certificate,dict) or certificate.keys()!=expected.keys():return False
    return all(signature(certificate[k])==signature(v) for k,v in expected.items())

def ray_power(c,p,u,t):
    t=number(t)
    if t<0:raise ValueError('ray parameter must be nonnegative')
    a=analyze(c,p,u)
    return power(c,add(a['point'],scale(a['direction'],t)))

def narrow_example(n):
    """Circle center(0,1), P=(0,0), u=(n,1). Each finite n has interior ray points."""
    n=number(n)
    if n<=0:raise ValueError('positive n required')
    return analyze(Circle((0,1),1),(0,0),(n,1))
