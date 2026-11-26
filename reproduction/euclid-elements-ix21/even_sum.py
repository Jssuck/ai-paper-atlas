"""Construct the two equal halves in Euclid IX.21."""
from dataclasses import dataclass


@dataclass(frozen=True)
class EvenSum:
    term_halves: tuple
    half_total: int
    total: int


def even_sum(terms):
    """Certify a finite nonempty list of positive even integers."""
    terms=tuple(terms)
    if not terms:
        raise ValueError("expected a nonempty list")
    halves=[]
    for n in terms:
        if type(n) is not int or n<2:
            raise ValueError("every term must be a positive even integer")
        q,r=divmod(n,2)
        if r:
            raise ValueError("every term must be a positive even integer")
        halves.append(q)
    half=sum(halves)
    total=sum(terms)
    if half+half!=total:
        raise ArithmeticError("reconstructed halves must sum to the original total")
    return EvenSum(tuple(halves),half,total)
