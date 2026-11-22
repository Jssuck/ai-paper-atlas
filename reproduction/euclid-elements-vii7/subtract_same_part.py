"""VII.7: build an auxiliary whole, add matched parts, cancel the common segment."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Witness:
    n: int
    eb: int
    cg: int
    gf: int
    fd: int
    coordinates: tuple


def _validate(ab,cd,ae,cf,modern_units):
    if any(type(x) is not int or x<1 for x in (ab,cd,ae,cf)):
        raise ValueError("positive integer inputs required")
    if not (ae<ab<cd and ae<cf<cd):
        raise ValueError("proper parts and strictly positive remainders required")
    if not modern_units and min(ab,cd,ae,cf)==1:
        raise ValueError("a given ancient number is not a unit")


def reconstruct(ab,cd,ae,cf,modern_units=False):
    _validate(ab,cd,ae,cf,modern_units)
    n,r=divmod(cd,ab)
    m,s=divmod(cf,ae)
    if r or s or n!=m:
        raise ValueError("matching unit fractions required")
    eb=ab-ae
    cg=n*eb
    # VII.5 style: each of the n matched portions contributes AE+EB.
    gf=sum(a+b for a,b in zip((ae,)*n,(eb,)*n))
    fd=cd-cf
    return Witness(n,eb,cg,gf,fd,(-cg,0,cf,cd))


def ratios(ab,cd,ae,cf):
    _validate(ab,cd,ae,cf,True)
    return Fraction(ab,cd),Fraction(ae,cf),Fraction(ab-ae,cd-cf)
