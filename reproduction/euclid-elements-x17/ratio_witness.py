"""X.17: exact reconstruction of two parts and their commensurability."""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


@dataclass(frozen=True)
class Witness:
    gap_squared: Fraction
    parts: tuple[Fraction, Fraction] | None  # smaller, larger


def divide(b,a):
    """Divide B>A>0 with product of the parts equal to A²/4."""
    if any(type(x) not in (int,Fraction) or x<=0 for x in (b,a)):
        raise ValueError("expected exact positive rational lengths")
    b,a = Fraction(b),Fraction(a)
    if b<=a:
        raise ValueError("B must exceed A")
    q = b*b-a*a
    p,d = isqrt(q.numerator),isqrt(q.denominator)
    if p*p!=q.numerator or d*d!=q.denominator:
        return Witness(q,None)
    gap=Fraction(p,d)
    return Witness(q,((b-gap)/2,(b+gap)/2))
