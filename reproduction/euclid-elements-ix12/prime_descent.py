"""Descending prime-divisor certificates for Euclid IX.12."""
from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class Stage:
    exponent: int
    power: int
    quotient: int


def descend_prime(q, k, p):
    """Verify prime p divides q**k, then trace actual quotients down to q."""
    if any(type(n) is not int for n in (q,k,p)) or q < 2 or k < 1 or p < 2:
        raise ValueError("expected q,p >= 2 and k >= 1 as integers")
    if any(p%d==0 for d in range(2,isqrt(p)+1)):
        raise ValueError("candidate must be prime")
    value=q**k
    if value%p:
        raise ValueError("candidate does not divide the given term")
    result=[]
    for e in range(k,0,-1):
        quotient,rem=divmod(value,p)
        if rem:
            raise ArithmeticError("prime descent invariant failed")
        result.append(Stage(e,value,quotient))
        value//=q
    return tuple(result)
