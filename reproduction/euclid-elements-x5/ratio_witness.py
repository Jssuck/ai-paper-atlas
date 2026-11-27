"""Exact common-measure and equimultiple certificates for Euclid X.5."""
from dataclasses import dataclass
from fractions import Fraction


def _cmp(x,y):
    return (x>y)-(x<y)


@dataclass(frozen=True)
class RatioWitness:
    measure: Fraction
    counts: tuple

    def compare(self,u,v):
        """Compare uA:vB in order and uk:vl for counts k,l."""
        if any(type(x) is not int or x<1 for x in (u,v)):
            raise ValueError("expected positive integer multipliers")
        k,l=self.counts
        left,right=u*k,v*l
        return _cmp(left*self.measure,right*self.measure),_cmp(left,right)


def ratio_witness(a,b,d):
    if any(type(x) not in (int,Fraction) or x<=0 for x in (a,b,d)):
        raise ValueError("expected exact positive rational magnitudes")
    d=Fraction(d)
    k,l=Fraction(a)/d,Fraction(b)/d
    if k.denominator!=1 or l.denominator!=1:
        raise ValueError("the proposed measure must divide both magnitudes")
    return RatioWitness(d,(int(k),int(l)))
