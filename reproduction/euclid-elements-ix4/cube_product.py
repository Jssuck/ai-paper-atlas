"""Exact integer teaching reconstruction of Euclid IX.4."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CubeProduct:
    chain: tuple
    lifted: tuple
    root: int
    modern_unit: bool


def _root(n):
    low, high = 0, 1 << ((n.bit_length()+2)//3)
    while low+1 < high:
        mid = (low+high)//2
        if mid**3 <= n:
            low = mid
        else:
            high = mid
    if low**3 != n:
        raise ValueError("both factors must be cubes")
    return low


def cube_product(a, b):
    """Given positive cubes A,B, construct and check the cube root of AB."""
    if any(type(x) is not int or x < 1 for x in (a,b)):
        raise ValueError("expected two positive integers")
    x,y = _root(a),_root(b)
    chain = (a,x*x*y,x*y*y,b)
    lifted = tuple(a*n for n in chain)
    root, rem = divmod(lifted[1],x**4)
    if rem or root**3 != lifted[-1] or lifted[2] != x*x*root**2:
        raise ArithmeticError("cube-root transfer invariant failed")
    return CubeProduct(chain,lifted,root,min(a,b)==1)
