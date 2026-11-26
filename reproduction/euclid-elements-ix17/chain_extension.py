"""Exact teaching model of Euclid IX.17."""
from fractions import Fraction
from math import gcd


def continuation(terms):
    """Modern rational continuation of a positive integer geometric chain."""
    terms=tuple(terms)
    if len(terms)<2 or any(type(n) is not int or n<1 for n in terms):
        raise ValueError("expected at least two positive integer terms")
    a,b=terms[:2]
    if any(a*y != b*x for x,y in zip(terms,terms[1:])):
        raise ValueError("successive ratios must agree")
    return Fraction(terms[-1]*b,a)


def coprime_endpoint_obstruction(terms):
    """Return the unique noninteger candidate under the IX.17 premises."""
    terms=tuple(terms)
    result=continuation(terms)
    if min(terms[0],terms[-1])<2 or gcd(terms[0],terms[-1])!=1:
        raise ValueError("the endpoints must be coprime nonunit integers")
    a=terms[0]//gcd(*terms[:2])
    if result.denominator!=a or a<2:
        raise ArithmeticError("coprime-endpoint obstruction failed")
    return result
