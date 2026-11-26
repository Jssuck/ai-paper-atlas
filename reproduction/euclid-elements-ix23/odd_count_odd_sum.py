"""Construct the odd-sum witness of Euclid IX.23."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    prefix_half: int
    last_half: int
    total_half_without_unit: int
    total: int


def odd_count_odd_sum(terms):
    """An odd list of at least three nonunit positive odd integers."""
    terms=tuple(terms)
    if len(terms)<3 or len(terms)%2==0:
        raise ValueError("expected an odd count of at least three terms")
    if any(type(n) is not int or n<3 or n%2==0 for n in terms):
        raise ValueError("expected odd integer terms at least 3")
    prefix=terms[:-1]
    prefix_half=sum((n-1)//2 for n in prefix)+len(prefix)//2
    last_half=(terms[-1]-1)//2
    half=prefix_half+last_half
    total=sum(terms)
    if half+half+1 != total:
        raise ArithmeticError("odd sum witness did not reconstruct total")
    return Witness(prefix_half,last_half,half,total)
