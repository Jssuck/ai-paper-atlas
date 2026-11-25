"""Exact teaching reconstruction of Euclid IX.6."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CubeTrace:
    source: tuple
    target: tuple
    root: int
    modern_unit: bool


def cube_from_square(a):
    """Assuming A² is a cube, construct a positive integer cube root of A."""
    if type(a) is not int or a < 1:
        raise ValueError("A must be a positive integer")
    squared = a*a
    lo, hi = 0, 1 << ((squared.bit_length()+2)//3)
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**3 <= squared:
            lo = mid
        else:
            hi = mid
    b = lo
    if b**3 != squared:
        raise ValueError("A squared must be a cube")
    source = (b**3,b*b*a,b*squared,a**3)
    divisions = [divmod(n,a) for n in source]
    target = tuple(q for q,_ in divisions)
    # The four exact quotients use b³=A², not the sought root of A.
    if any(r for _,r in divisions) or target != (a,b*b,b*a,squared):
        raise ArithmeticError("chain division invariant failed")
    root, rem = divmod(a,b)
    if rem or root**3 != a:
        raise ArithmeticError("cube root transfer invariant failed")
    return CubeTrace(source,target,root,a==1)
