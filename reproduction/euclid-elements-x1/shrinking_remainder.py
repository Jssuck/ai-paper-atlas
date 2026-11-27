"""Exact finite remainder certificates for Euclid X.1."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Audit:
    reference_count: int
    dyadic_steps: int
    first_below: int


def audit_remainders(threshold, remainders, *, allow_half=False):
    """Check every positive remainder, then audit when one is below threshold."""
    remainders=tuple(remainders)
    if any(type(v) not in (int,Fraction) for v in (threshold,*remainders)):
        raise ValueError("use integers and Fraction only")
    x=Fraction(threshold)
    r=tuple(map(Fraction,remainders))
    if len(r)<2 or not 0<x<r[0] or any(v<=0 for v in r):
        raise ValueError("need a smaller positive threshold and positive remainder chain")
    for a,b in zip(r,r[1:]):
        if 2*b>a or (2*b==a and not allow_half):
            raise ValueError("each new remainder must be less than half, or optionally at most half")
    n=r[0]//x+1
    k=0
    ceiling=r[0]
    while ceiling>=x:
        ceiling/=2
        k+=1
    for i,y in enumerate(r):
        if i<n and not y < (n-i)*x:
            raise ArithmeticError("linear reference ladder invariant failed")
        if y*2**i>r[0]:
            raise ArithmeticError("dyadic upper bound failed")
    below=next((i for i,y in enumerate(r) if y<x),None)
    if below is None:
        raise ValueError("finite input stopped before a strict crossing")
    if below>min(k,n-1):
        raise ArithmeticError("crossing exceeded the audited bound")
    return Audit(n,k,below)
