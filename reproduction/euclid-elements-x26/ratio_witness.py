"""X.26 in exact reference-relative rational/radical coordinates."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def positive(x):
    if type(x) not in (int,F) or x<=0:
        raise ValueError("expected a positive int or Fraction")
    return F(x)


def root(q):
    a,b=isqrt(q.numerator),isqrt(q.denominator)
    return F(a,b) if (a*a,b*b)==(q.numerator,q.denominator) else None


def medial(q):
    q=positive(q)
    if root(q) is not None:
        raise ValueError("relative squared area must not be a rational square")
    return q


@dataclass(frozen=True)
class WidthSquare:
    constant: F
    radical_coefficient: F
    radicand: F


def contradiction(q,gap,base_squared):
    """Width²=(sqrt(q)+gap)²/base_squared under the alleged rational gap."""
    q,r,b=medial(q),positive(gap),positive(base_squared)
    return WidthSquare((q+r*r)/b,2*r/b,q)


def difference_squared(p,q):
    """Represent (sqrt(p)-sqrt(q))² as a rational or a radical expression."""
    p,q=medial(p),medial(q)
    if p<=q:
        raise ValueError("larger squared area must strictly exceed the smaller")
    t=root(p*q)
    return p+q-2*t if t is not None else WidthSquare(p+q,F(-2),p*q)
