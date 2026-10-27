"""Exact real quadratic arithmetic, adapted from this repository I.12 teaching code.
One common radicand only; not a general computer algebra system.
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

