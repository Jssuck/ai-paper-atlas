"""Exact teaching witness for Euclid IX.35."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Witness:
    adjacent_differences: tuple
    endpoint_difference: int
    subtraction_ratio: Fraction
    prefix_sum: int


def geometric_prefix_sum(terms):
    """Construct the sum of all but the final term using the difference ratio."""
    terms=tuple(terms)
    if len(terms)<3 or any(type(x) is not int or x<1 for x in terms):
        raise ValueError("expected at least three positive integer terms")
    a,b=terms[:2]
    if b<=a or any(a*y!=b*x for x,y in zip(terms,terms[1:])):
        raise ValueError("expected an increasing geometric chain")
    differences=tuple(y-x for x,y in zip(terms,terms[1:]))
    terminal=terms[-1]-a
    if any(a*d!=differences[0]*x for x,d in zip(terms[:-1],differences)):
        raise ArithmeticError("adjacent differences do not have the common scale")
    ratio=Fraction(terminal,differences[0])
    result=ratio*a
    if result.denominator!=1:
        raise ArithmeticError("prefix must be an integer sum")
    return Witness(differences,terminal,ratio,int(result))
