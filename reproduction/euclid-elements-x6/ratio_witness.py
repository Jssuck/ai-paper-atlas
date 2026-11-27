"""Exact construction for Euclid X.6 and its porism."""
from fractions import Fraction
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    part: Fraction
    constructed: Fraction
    mean_squared: Fraction


def construct(a,m,n):
    """Construct C=A/m and F=nC, and store the mean's square."""
    if type(a) not in (int,Fraction) or a<=0:
        raise ValueError("expected positive exact A")
    if any(type(k) is not int or k<1 for k in (m,n)):
        raise ValueError("expected positive integer ratio counts")
    c=Fraction(a)/m
    f=n*c
    return Witness(c,f,a*f)


def ratio_witness(a,b,m,n):
    if type(b) not in (int,Fraction) or b<=0:
        raise ValueError("expected positive exact B")
    w=construct(a,m,n)
    if w.constructed!=b:
        raise ValueError("constructed F does not equal supplied B")
    return w
