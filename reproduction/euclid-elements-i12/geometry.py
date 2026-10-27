"""Original exact-coordinate teaching reconstruction of Euclid I.12.

Inputs are rational points. Output lies in Q(sqrt(delta)); finite runs are not
proofs of Euclid's general theorem. Floats are intentionally not accepted.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('expected int or Fraction, not floating point')
    return F(x)


@dataclass(frozen=True, eq=False)
class Q:
    a: F = F(0)
    b: F = F(0)
    d: F = F(0)

    def __post_init__(self):
        a,b,d=map(rational,(self.a,self.b,self.d))
        if d<0:
            raise ValueError('real radicand must be nonnegative')
        n,m=isqrt(d.numerator),isqrt(d.denominator)
        if n*n==d.numerator and m*m==d.denominator:
            a,b,d=a+b*F(n,m),F(0),F(0)
        if b==0:
            d=F(0)
        object.__setattr__(self,'a',a);object.__setattr__(self,'b',b);object.__setattr__(self,'d',d)

    def pair(self,other):
        other=other if isinstance(other,Q) else Q(rational(other))
        if self.b and other.b and self.d!=other.d:
            raise ValueError('mixed nonsquare radicands not supported')
        return other,self.d if self.b else other.d

    def __add__(self,other):
        other,d=self.pair(other)
        return Q(self.a+other.a,self.b+other.b,d)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b,self.d)
    def __sub__(self,other):return self+-asq(other)
    def __rsub__(self,other):return asq(other)+-self
    def __mul__(self,other):
        other,d=self.pair(other)
        return Q(self.a*other.a+self.b*other.b*d,self.a*other.b+self.b*other.a,d)
    __rmul__=__mul__
    def __truediv__(self,other):
        other,d=self.pair(other)
        den=other.a*other.a-other.b*other.b*d
        if den==0:raise ZeroDivisionError('zero quadratic denominator')
        num=self*Q(other.a,-other.b,d)
        return Q(num.a/den,num.b/den,d)
    def __eq__(self,other):
        try:
            other,d=self.pair(other)
        except (TypeError,ValueError):return False
        return self.a==other.a and self.b==other.b
    def sign(self):
        if not self.b:return (self.a>0)-(self.a<0)
        if not self.a:return (self.b>0)-(self.b<0)
        if self.a>0 and self.b>0:return 1
        if self.a<0 and self.b<0:return -1
        cmp=(self.a*self.a>self.b*self.b*self.d)-(self.a*self.a<self.b*self.b*self.d)
        return cmp if self.a>0 else -cmp
    def __str__(self):
        return str(self.a) if not self.b else f'({self.a})+({self.b})*sqrt({self.d})'


def asq(x):return x if isinstance(x,Q) else Q(rational(x))
def point(x,y):return (asq(x),asq(y))
def add(p,q):return tuple(x+y for x,y in zip(p,q))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def scale(s,p):return tuple(asq(s)*x for x in p)
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def norm2(p):return dot(p,p)
def dist2(p,q):return norm2(sub(p,q))

def rational_point(p):
    return isinstance(p,tuple) and len(p)==2 and all(isinstance(x,Q) and not x.b for x in p)

@dataclass(frozen=True)
class Certificate:
    center: tuple
    radius_squared: Q
    e: tuple
    g: tuple
    h: tuple


def parameters(a,b,c,d):
    if not all(rational_point(p) for p in (a,b,c,d)):
        raise TypeError('inputs must be rational point() pairs')
    u=sub(b,a); length=norm2(u)
    if length==0:raise ValueError('A and B must differ')
    side_c=cross(u,sub(c,a));side_d=cross(u,sub(d,a))
    if side_c==0:raise ValueError('C must be off the line')
    if (side_c*side_d).sign()>=0:raise ValueError('D must be strictly on the other side')
    # Solve |A+t(B-A)-C|^2=|C-D|^2. t0 is the mean of its roots.
    t0=dot(sub(c,a),u)/length
    radius=dist2(c,d)
    delta=(radius-dist2(a,c))/length+t0*t0
    if delta.sign()<=0:raise ValueError('circle must be a true secant')
    return u,t0,radius,delta


def construct(a,b,c,d):
    u,t0,radius,delta=parameters(a,b,c,d)
    root=Q(0,1,delta.a)
    e=add(a,scale(t0+root,u));g=add(a,scale(t0-root,u))
    h=scale(F(1,2),add(e,g))
    return Certificate(c,radius,e,g,h)


def check_certificate(a,b,c,d,k):
    """Input-bound construction certificate, stricter than perpendicular-only.

    Wrong fields/mixed extensions return a rejection, not a partial success.
    """
    try:
        u,t0,radius,delta=parameters(a,b,c,d)
        if not isinstance(k,Certificate):return {'well_formed':False}
        e,g,h=k.e,k.g,k.h
        if not all(isinstance(p,tuple) and len(p)==2 and all(isinstance(x,Q) for x in p)
                   for p in (k.center,e,g,h)):
            return {'well_formed':False}
        return {
          'center_bound_to_C':k.center==c,
          'radius_bound_to_CD':k.radius_squared==radius,
          'E_on_line':cross(u,sub(e,a))==0,
          'G_on_line':cross(u,sub(g,a))==0,
          'distinct_intersections':e!=g,
          'E_on_prescribed_circle':dist2(c,e)==radius,
          'G_on_prescribed_circle':dist2(c,g)==radius,
          'H_is_midpoint':scale(2,h)==add(e,g),
          'H_on_line':cross(u,sub(h,a))==0,
          'H_between_E_G':dot(sub(e,h),sub(g,h)).sign()<0,
          'equal_half_chords':dist2(e,h)==dist2(g,h),
          'CH_nonzero':dist2(c,h).sign()>0,
          'nondegenerate_triangle':cross(sub(c,h),sub(e,h)).sign()!=0,
          'perpendicular_modern_check':dot(sub(c,h),u)==0,
        }
    except (ValueError,TypeError,ZeroDivisionError,AttributeError,IndexError):
        return {'well_formed':False}


def accepted(a,b,c,d,k):return all(check_certificate(a,b,c,d,k).values())

def foot_parameter(a,b,h):return dot(sub(h,a),sub(b,a))/norm2(sub(b,a))
