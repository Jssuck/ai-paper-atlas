"""Exact rational-pair arithmetic for Euclid VI.30."""
from dataclasses import dataclass
from fractions import Fraction as Q


@dataclass(frozen=True)
class Root5:
    a: Q = Q(0)
    b: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self,"a",Q(self.a))
        object.__setattr__(self,"b",Q(self.b))

    def __add__(self,other):
        other=coerce(other)
        return Root5(self.a+other.a,self.b+other.b)

    __radd__=__add__

    def __neg__(self):
        return Root5(-self.a,-self.b)

    def __sub__(self,other):
        return self+-coerce(other)

    def __mul__(self,other):
        other=coerce(other)
        return Root5(self.a*other.a+5*self.b*other.b,self.a*other.b+self.b*other.a)

    __rmul__=__mul__

    def sign(self):
        a,b=self.a,self.b
        sign=lambda x:(x>0)-(x<0)
        sa,sb=sign(a),sign(b)
        if not a or not b or sa==sb:
            return sa or sb
        return sa*sign(a*a-5*b*b)


def coerce(x):
    return x if isinstance(x,Root5) else Root5(Q(x))


def cut(length):
    length=Q(length)
    if length<=0:
        raise ValueError("positive total required")
    m=length/2
    x=Root5(-m,m)
    return x,coerce(length)-x


def conjugate_root(length):
    m=Q(length)/2
    return Root5(-m,-m)


def rectangle(w,h):
    z=Root5()
    w,h=coerce(w),coerce(h)
    return ((z,z),(w,z),(w,h),(z,h))


def signed_double_area(vertices):
    return sum(x*v-y*u for (x,y),(u,v) in zip(vertices,vertices[1:]+vertices[:1]))
