"""Compare sqrt(a_squared)/B with m/n without extracting a root."""
from fractions import Fraction
from dataclasses import dataclass


@dataclass(frozen=True)
class Comparison:
    gap: Fraction
    sign: int


def compare_ratio(a_squared,b,m,n):
    """Positive quantities A and B, with A represented by A squared."""
    if any(type(x) not in (int,Fraction) or x<=0 for x in (a_squared,b)):
        raise ValueError("expected positive exact squared magnitude and reference")
    if any(type(x) is not int or x<1 for x in (m,n)):
        raise ValueError("ratio counts must be positive integers")
    gap=Fraction(a_squared)*n*n-(Fraction(b)*m)**2
    return Comparison(gap,(gap>0)-(gap<0))
