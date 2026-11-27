"""Exact rational teaching reconstruction of Euclid X.4."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Certificate:
    pair_measure: Fraction
    measure: Fraction
    branch: str
    counts: tuple


def _pair(a,b):
    while b:
        a,b=b,a%b
    return a


def greatest_common_measure(a,b,c):
    """First combine A,B, then retain their measure if it also measures C."""
    if any(type(x) not in (int,Fraction) or x<=0 for x in (a,b,c)):
        raise ValueError("expected three exact positive rational magnitudes")
    a,b,c=map(Fraction,(a,b,c))
    pair=_pair(a,b)
    if c%pair==0:
        measure,branch=pair,"direct"
    else:
        measure,branch=_pair(pair,c),"delayed"
    counts=(a/measure,b/measure,c/measure)
    if any(q.denominator!=1 for q in counts):
        raise ArithmeticError("measure did not divide all three magnitudes")
    return Certificate(pair,measure,branch,tuple(map(int,counts)))
