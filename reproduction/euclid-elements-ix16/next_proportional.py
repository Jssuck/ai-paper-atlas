"""Exact continuation and premise checks for Euclid IX.16."""
from fractions import Fraction
from math import gcd


def next_proportional(a,b):
    """Modern positive-integer domain, returning the unique rational continuation."""
    if any(type(n) is not int or n<1 for n in (a,b)):
        raise ValueError("expected two positive integer terms")
    return b*Fraction(b,a)


def no_integer_continuation(a,b):
    """Certificate: reduced denominator equals a for coprime nonunit terms."""
    candidate=next_proportional(a,b)
    if min(a,b)<2 or gcd(a,b)!=1:
        raise ValueError("expected two coprime nonunit terms")
    if candidate.denominator!=a:
        raise ArithmeticError("denominator certificate failed")
    return candidate
