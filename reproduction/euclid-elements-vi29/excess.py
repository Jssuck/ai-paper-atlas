"""VI.29 exact modern overshoot and prescribed-shape area model."""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt


@dataclass(frozen=True)
class Certificate:
    half: Q
    diagonal_base2: Q

    def overshoot(self):
        q=self.diagonal_base2
        n,d=isqrt(q.numerator),isqrt(q.denominator)
        return Q(n,d)-self.half if n*n==q.numerator and d*d==q.denominator else None

    def radical_area(self,r,sign=1):
        """Coefficients (constant, root) for r*x*(L+x) on either branch."""
        if sign not in (-1,1):
            raise ValueError("expected ±1")
        # x=-m±√q, L+x=m±√q.
        return r*(self.diagonal_base2-self.half**2),r*(-self.half*sign+sign*self.half)


def solve(length,r,target):
    length,r,target=map(Q,(length,r,target))
    if min(length,r,target)<=0:
        raise ValueError("positive length, ratio and target required")
    half=length/2
    return Certificate(half,half**2+target/r)


def polygon(width,height,slant,left=0,lift=0):
    return ((left,lift),(left+width,lift),
            (left+width+slant,lift+height),(left+slant,lift+height))


def area(vertices):
    return Q(abs(sum(x*v-y*u for (x,y),(u,v) in zip(vertices,vertices[1:]+vertices[:1]))),2)


def area_cells(m,x,r,s):
    """Base corner, two complements, excess corner, using the common shear s/r."""
    return (polygon(m,r*m,s*m),
            polygon(x,r*m,s*m,m),
            polygon(m,r*x,s*x,s*m,r*m),
            polygon(x,r*x,s*x,m+s*m,r*m))


def applied(length,x,r,s):
    return polygon(length+x,r*x,s*x)
