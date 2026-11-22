"""VII.6: match the same proper multiple-part ratio exactly."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Witness:
    m: int
    n: int
    first_unit: int
    second_unit: int
    partial_pairs: tuple
    whole_pairs: tuple


def _validate(a,b,c,d):
    if any(type(x) is not int for x in (a,b,c,d)) or not (0<a<b and 0<c<d):
        raise ValueError("two proper ordered pairs of positive integers required")


def construct(a,b,c,d):
    """Show all m selected pairs and n whole pairs in the reduced representation."""
    _validate(a,b,c,d)
    g,h=gcd(a,b),gcd(c,d)
    m,n=a//g,b//g
    if m==1 or (c//h,d//h)!=(m,n):
        raise ValueError("the same reduced m/n with 1 < m < n is required")
    part=tuple(zip((g,)*m,(h,)*m))
    whole=tuple(zip((g,)*n,(h,)*n))
    return Witness(m,n,g,h,part,whole)


def ratios(a,b,c,d):
    _validate(a,b,c,d)
    return Fraction(a,b),Fraction(c,d),Fraction(a+c,b+d)


def paired_totals(pairs):
    return tuple(map(sum,zip(*pairs)))+(sum(sum(pair) for pair in pairs),)
