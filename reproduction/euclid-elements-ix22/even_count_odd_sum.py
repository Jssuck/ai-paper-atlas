"""Construct a parity witness for Euclid IX.22."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    residual_halves: tuple
    unit_pairs: int
    total_half: int
    total: int


def even_count_odd_sum(terms):
    """Return an equal-halves witness for an even number of odd terms >= 3."""
    terms = tuple(terms)
    if len(terms) < 2 or len(terms) % 2:
        raise ValueError("expected an even count of at least two terms")
    halves = []
    for term in terms:
        if type(term) is not int or term < 3 or term % 2 == 0:
            raise ValueError("expected odd integer terms at least 3")
        halves.append((term-1)//2)
    pairs = len(terms)//2
    half = sum(halves) + pairs
    total = sum(terms)
    if half+half != total:
        raise ArithmeticError("halves do not reconstruct total")
    return Witness(tuple(halves), pairs, half, total)
