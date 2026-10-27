"""I.22 teaching reconstruction over rational numbers and one quadratic field."""
from dataclasses import dataclass
from fractions import Fraction as Q
import json


def rational(value):
    if type(value) is int or type(value) is Q:
        return Q(value)
    if type(value) is str:
        return Q(value)
    raise ValueError('expected exact integer, fraction string, or Fraction')


def sides(a, b, c):
    values = tuple(rational(v) for v in (a,b,c))
    if min(values) <= 0:
        raise ValueError('three strictly positive lengths required')
    return values


def classify(a,b,c):
    a,b,c=sides(a,b,c)
    if c > a+b: return 'separate'
    if c < abs(a-b): return 'contained'
    if c == a+b: return 'external_tangent_degenerate'
    if c == abs(a-b): return 'internal_tangent_degenerate'
    return 'two_intersections'


@dataclass(frozen=True)
class Quad:
    """p+q*sqrt(d), used only within a single positive rational radicand."""
    p: Q
    q: Q
    d: Q
    def __post_init__(self):
        for key in ('p','q','d'):
            object.__setattr__(self,key,rational(getattr(self,key)))
        if self.d <= 0: raise ValueError('positive radicand required')
    def coerce(self, value):
        if isinstance(value,Quad):
            if value.d != self.d: raise ValueError('different quadratic fields')
            return value
        return Quad(rational(value),0,self.d)
    def __add__(self,other):
        other=self.coerce(other)
        return Quad(self.p+other.p,self.q+other.q,self.d)
    __radd__=__add__
    def __neg__(self): return Quad(-self.p,-self.q,self.d)
    def __sub__(self,other): return self+-self.coerce(other)
    def __mul__(self,other):
        other=self.coerce(other)
        return Quad(self.p*other.p+self.q*other.q*self.d,
                    self.p*other.q+self.q*other.p,self.d)
    __rmul__=__mul__
    def rational_value(self):
        if self.q: raise ValueError('expression not reduced to rational coefficient')
        return self.p


def construct(a,b,c,orientation=1):
    a,b,c=sides(a,b,c)
    if type(orientation) is not int or orientation not in (-1,1):
        raise ValueError('orientation must be integer -1 or +1')
    if classify(a,b,c) != 'two_intersections':
        raise ValueError('strict triangle inequalities required')
    x=(a*a+c*c-b*b)/(2*c)
    h2=a*a-x*x
    factored=((a+b)**2-c*c)*(c*c-(a-b)**2)/(4*c*c)
    if h2 <= 0 or h2 != factored: raise ArithmeticError('height identity failed')
    y=Quad(0,orientation,h2)
    xx=Quad(x,0,h2)
    left=(xx*xx+y*y).rational_value()
    right=((xx-c)*(xx-c)+y*y).rational_value()
    if (left,right)!=(a*a,b*b): raise ArithmeticError('distance identity failed')
    return {'schema_version':1,'input':{'a':str(a),'b':str(b),'c':str(c)},
            'orientation':orientation,'F':['0','0'],'G':[str(c),'0'],
            'K':{'x':str(x),'y':{'coefficient':str(orientation),'radicand':str(h2)}},
            'height_squared':str(h2),'factorized_height_squared':str(factored),
            'squared_distances':{'FK':str(left),'GK':str(right),'FG':str(c*c)},
            'strict_triangle':True,'noncollinear':True}


def canonical(value):
    """Only a strict JSON subset; bool and int remain different encodings."""
    def visit(v):
        if type(v) in (str,int,bool) or v is None:return
        if type(v) is list:
            for e in v:visit(e)
            return
        if type(v) is dict and all(type(k) is str for k in v):
            for e in v.values():visit(e)
            return
        raise ValueError('noncanonical JSON type')
    visit(value)
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)


def verify(certificate,a,b,c,orientation=1):
    try:return canonical(certificate)==canonical(construct(a,b,c,orientation))
    except (ValueError,TypeError,ZeroDivisionError,OverflowError):return False
