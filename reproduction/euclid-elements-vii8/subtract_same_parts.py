"""VII.8: copied whole, local subtraction of matched parts, and summation."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Witness:
    m: int
    n: int
    u: int
    v: int
    endpoints: tuple
    cuts: tuple
    leftovers: tuple

    def gh(self):
        return self.endpoints[-1]-self.endpoints[0]


def _validate(ab,cd,ae,cf):
    if any(type(x) is not int or x<=1 for x in (ab,cd,ae,cf)):
        raise ValueError("given terms must be positive nonunit integers")
    if not (ae<ab<cd and ae<cf<cd):
        raise ValueError("proper ratios and positive partial removal required")


def construct(ab,cd,ae,cf):
    _validate(ab,cd,ae,cf)
    u,v=gcd(ab,cd),gcd(ae,cf)
    m,n=ab//u,cd//u
    if m==1 or (ae//v,cf//v)!=(m,n):
        raise ValueError("matching reduced multiple-part ratios required")
    endpoints=tuple(i*u for i in range(m+1))
    cuts=tuple(z+v for z in endpoints[:-1])
    leftovers=tuple(z-cut for z,cut in zip(endpoints[1:],cuts))
    return Witness(m,n,u,v,endpoints,cuts,leftovers)


def ratios(ab,cd,ae,cf):
    _validate(ab,cd,ae,cf)
    return Fraction(ab,cd),Fraction(ae,cf),Fraction(ab-ae,cd-cf)
