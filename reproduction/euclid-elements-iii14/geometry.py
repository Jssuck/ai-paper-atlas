"""Exact chord certificates. No floating-point tolerance or theorem-shaped inputs."""
from fractions import Fraction as F
from dataclasses import dataclass

def scalar(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise ValueError('expected integer or Fraction')
    return F(x)
def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2:raise ValueError('expected point pair')
    return tuple(scalar(x) for x in p)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(t,a):return tuple(t*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm2(a):return dot(a,a)
@dataclass(frozen=True)
class Circle:
    center:tuple
    radius:F
    def __post_init__(self):
        object.__setattr__(self,'center',point(self.center))
        object.__setattr__(self,'radius',scalar(self.radius))
        if self.radius<=0:raise ValueError('positive radius required')

def chord(c,a,b):
    if not isinstance(c,Circle):raise ValueError('Circle required')
    a,b=point(a),point(b)
    v=sub(b,a);length2=norm2(v)
    if length2==0:raise ValueError('distinct chord endpoints required')
    r2=c.radius*c.radius
    if norm2(sub(a,c.center))!=r2 or norm2(sub(b,c.center))!=r2:
        raise ValueError('both endpoints must lie on circle')
    t=dot(sub(c.center,a),v)/length2
    foot=add(a,mul(t,v));distance2=norm2(sub(foot,c.center))
    half2=norm2(sub(a,foot))
    return {'a':a,'b':b,'foot':foot,'projection_parameter':t,
            'length2':length2,'distance2':distance2,'half_length2':half2,
            'radius2':r2,'diameter':distance2==0}

def validate(c,certificate):
    if not isinstance(certificate,dict):return False
    try:
        expected=chord(c,certificate['a'],certificate['b'])
        return (set(certificate)==set(expected) and all(type(certificate[k]) is type(v) and certificate[k]==v and (not isinstance(v,tuple) or all(type(x) is F for x in certificate[k])) for k,v in expected.items()))
    except (ValueError,TypeError,KeyError):return False

def compare(c,a,b,d,e):
    first,second=chord(c,a,b),chord(c,d,e)
    equal_chords=first['length2']==second['length2']
    equal_distances=first['distance2']==second['distance2']
    return {'first':first,'second':second,'equal_chords':equal_chords,
            'equal_distances':equal_distances,'equivalence_holds':equal_chords==equal_distances}

def rational_circle_point(c,t):
    """Rational parametrization; omits only (-r,0) before translating."""
    t=scalar(t);den=1+t*t
    return add(c.center,(c.radius*(1-t*t)/den,c.radius*2*t/den))
