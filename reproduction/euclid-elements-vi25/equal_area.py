"""Exact teaching model for Euclid VI.25."""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt

TRIANGLE=((0,0),(6,0),(2,4))


def area(vertices):
    return Q(abs(sum(x*v-y*u for (x,y),(u,v) in
                     zip(vertices,vertices[1:]+vertices[:1]))),2)


def rectangle(b,h):
    return ((0,0),(b,0),(b,h),(0,h))


def scale(vertices,k):
    return tuple((k*x,k*y) for x,y in vertices)


def rational_sqrt(value):
    value=Q(value)
    n,d=isqrt(value.numerator),isqrt(value.denominator)
    return Q(n,d) if n*n==value.numerator and d*d==value.denominator else None


@dataclass(frozen=True)
class Certificate:
    base: Q
    height: Q
    transfer_base: Q
    output_base2: Q
    scale2: Q

    def output_base(self):
        return rational_sqrt(self.output_base2)


def construct(b,source,target):
    b,source,target=map(Q,(b,source,target))
    if min(b,source,target)<=0:
        raise ValueError("positive base and areas required")
    h=source/b
    x=target/h
    g2=b*x
    return Certificate(b,h,x,g2,g2/(b*b))
