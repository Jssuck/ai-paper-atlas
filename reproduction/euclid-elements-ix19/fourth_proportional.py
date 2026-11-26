"""Exact teaching certificates for the ordered fourth proportional in IX.19."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Optional


@dataclass(frozen=True)
class Fourth:
    continued: bool
    coprime_endpoints: bool
    quotient: int
    remainder: int
    witness: Optional[int]
    auxiliary: Fraction


def fourth_proportional(a,b,c):
    """Return a witness for A:B=C:D, alongside the four-case flags."""
    if any(type(x) is not int or x<1 for x in (a,b,c)):
        raise ValueError("expected three positive integers")
    q,r=divmod(b*c,a)
    return Fourth(a*c==b*b,gcd(a,c)==1,q,r,q if not r else None,Fraction(c*c,a))


def nonunit_inputs(a,b,c):
    """Restrict the three given terms to nonunits; unit witness remains modern."""
    result=fourth_proportional(a,b,c)
    if min(a,b,c)<2:
        raise ValueError("expected nonunit given terms")
    return result
