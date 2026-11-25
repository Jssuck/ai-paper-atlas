"""Exact integer teaching reconstruction of Euclid IX.5."""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuotientTrace:
    source: tuple
    target: tuple
    root: int
    modern_unit: bool


def _cube_root(n):
    lo, hi = 0, 1 << ((n.bit_length()+2)//3)
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    if lo**3 != n:
        raise ValueError("A and C must both be cubes")
    return lo


def cube_quotient(a, c):
    """Construct the cube witness of B=C/A when A and C are positive cubes."""
    if any(type(n) is not int or n < 1 for n in (a,c)):
        raise ValueError("expected two positive integers")
    x,z = _cube_root(a),_cube_root(c)
    b, rem = divmod(c,a)
    if rem:
        raise ValueError("A must divide C exactly")
    d = x*x
    source = (a*a,d*d*z,d*z*z,c)
    divisions = tuple(divmod(term,a) for term in source)
    target = tuple(q for q,_ in divisions)
    root, root_rem = divmod(z,x)
    if any(r for _,r in divisions) or root_rem or target != (a,x*x*root,x*root*root,b) or root**3 != b:
        raise ArithmeticError("cube transfer invariant failed")
    return QuotientTrace(source,target,root,1 in (a,b,c))
