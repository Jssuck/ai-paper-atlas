"""Exact teaching model of Euclid VIII.19, with ordered integer factors."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class SolidTrace:
    kml: tuple
    anob: tuple
    step: Fraction


def solid_chain(left, right):
    """Construct K,M,L and A,N,O,B; reject nonproportional ordered factors."""
    c, d, e = left
    f, g, h = right
    if any(type(x) is not int or x < 1 for x in (c, d, e, f, g, h)):
        raise ValueError("each factor must be a positive integer")
    if c*g != d*f or d*h != e*g:
        raise ValueError("corresponding factors must be proportional")
    k, m, l = c*d, d*f, f*g
    return SolidTrace((k, m, l), (e*k, e*m, h*m, h*l), Fraction(f, c))
