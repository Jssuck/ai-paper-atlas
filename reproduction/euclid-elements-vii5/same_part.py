"""VII.5: two unit-fraction relations and a pooled copy witness."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Witness:
    divisor: int
    left: tuple
    right: tuple
    pooled: tuple

    def totals(self):
        return tuple(map(sum,(self.left,self.right,self.pooled)))


def _parse(a,b,c,d,allow_unit):
    if any(type(x) is not int or x<=0 for x in (a,b,c,d)):
        raise ValueError("positive integer inputs required")
    if not (a<b and c<d):
        raise ValueError("each part must be strictly smaller than its whole")
    if not allow_unit and min(a,c)==1:
        raise ValueError("the unit is not a number in the ancient domain")


def witness(a,b,c,d,allow_unit=False):
    """Obtain exact copy arrays (bounded teaching examples, not scalable storage)."""
    _parse(a,b,c,d,allow_unit)
    m,r=divmod(b,a)
    n,s=divmod(d,c)
    if r or s or m!=n:
        raise ValueError("the pairs must have the same integer denominator")
    left=(a,)*m
    right=(c,)*n
    return Witness(m,left,right,tuple(x+y for x,y in zip(left,right)))


def ratios(a,b,c,d):
    """Modern comparison, including examples where equal unit denominator fails."""
    _parse(a,b,c,d,True)
    return Fraction(a,b),Fraction(c,d),Fraction(a+c,b+d)
