"""Exact modern VI.28 deficit model, including a radical certificate."""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt


@dataclass(frozen=True)
class Solution:
    half: Q
    maximum: Q
    residual: Q
    gap2: Q

    def rational_cuts(self):
        n,d=isqrt(self.gap2.numerator),isqrt(self.gap2.denominator)
        if n*n!=self.gap2.numerator or d*d!=self.gap2.denominator:
            return None
        gap=Q(n,d)
        return (self.half-gap,self.half+gap) if gap else (self.half,)


def solve(length,r,target):
    length,r,target=map(Q,(length,r,target))
    if min(length,r,target)<=0:
        raise ValueError("positive length, height ratio and target required")
    half=length/2
    maximum=r*half*half
    residual=maximum-target
    if residual<0:
        raise ValueError("target exceeds maximum")
    return Solution(half,maximum,residual,residual/r)


def polygon(width,height,slant,left=0):
    return ((left,0),(left+width,0),(left+width+slant,height),(left+slant,height))


def area(vertices):
    return Q(abs(sum(x*v-y*u for (x,y),(u,v) in zip(vertices,vertices[1:]+vertices[:1]))),2)


def applied(length,r,cut,skew=Q(1,3)):
    return polygon(length-cut,r*cut,skew*cut)


def remaining(length,r,cut,skew=Q(1,3)):
    return polygon(cut,r*cut,skew*cut,length-cut)


def residual_shape(gap,r,skew=Q(1,3)):
    return polygon(gap,r*gap,skew*gap)


def radical_area_terms(half,gap2,r,sign):
    """Coefficients (constant, sqrt(gap2)) after multiplying the two bases."""
    if sign not in (-1,1):
        raise ValueError("sign must be ±1")
    # (half + sign*sqrt(gap2)) (half - sign*sqrt(gap2)) * r
    return r*(half*half-sign*sign*gap2), r*(sign*half-sign*half)


def diagonal_cells(half,gap,r,skew=Q(1,3)):
    """One modern coordinate realization of four cells, split at gap of half-width."""
    small,large=gap,half-gap
    shifted=skew*gap
    lift=r*gap
    return (polygon(small,lift,shifted),
            polygon(large,lift,shifted,gap),
            tuple((x+shifted,y+lift) for x,y in polygon(small,r*large,skew*large)),
            tuple((x+shifted,y+lift) for x,y in polygon(large,r*large,skew*large,gap)))
