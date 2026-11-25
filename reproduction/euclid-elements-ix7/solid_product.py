"""Exact integer teaching reconstruction of Euclid IX.7."""
from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class SolidTrace:
    factors: tuple
    product: int
    cube: bool


def solid_product(a, b):
    """Find a proper divisor of composite A and construct the three factors."""
    if any(type(n) is not int or n < 2 for n in (a,b)):
        raise ValueError("A and B must be integers greater than one")
    for d in range(2,isqrt(a)+1):
        e, rem = divmod(a,d)
        if rem == 0:
            c = d*e*b
            lo, hi = 0, 1 << ((c.bit_length()+2)//3)
            while lo+1 < hi:
                mid = (lo+hi)//2
                if mid**3 <= c:
                    lo = mid
                else:
                    hi = mid
            return SolidTrace((d,e,b),c,lo**3==c)
    raise ValueError("the first factor A must be composite")
