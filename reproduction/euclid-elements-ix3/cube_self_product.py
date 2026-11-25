"""Exact integer teaching trace for Euclid IX.3."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CubeSquareTrace:
    unit_chain: tuple
    scaled_chain: tuple
    root: int
    modern_unit: bool


def cube_self_product(a: int) -> CubeSquareTrace:
    """Given a positive cube A, return the chain and a cube root of A²."""
    if type(a) is not int or a < 1:
        raise ValueError("expected a positive integer")
    lo, hi = 0, 1 << ((a.bit_length()+2)//3)
    while hi-lo > 1:
        mid = (lo+hi)//2
        if mid**3 <= a:
            lo = mid
        else:
            hi = mid
    c = lo
    if c**3 != a:
        raise ValueError("A must be a cube")
    unit_chain = (1,c,c*c,a)
    scaled_chain = tuple(a*x for x in unit_chain)
    root, rem = divmod(scaled_chain[1],c*c)
    if rem or root**3 != scaled_chain[-1]:
        raise ArithmeticError("exact cube root transfer failed")
    return CubeSquareTrace(unit_chain,scaled_chain,root,a==1)
