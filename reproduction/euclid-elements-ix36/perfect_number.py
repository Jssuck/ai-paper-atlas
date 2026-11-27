"""Bounded integer teaching model of Euclid IX.36."""
from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class Witness:
    chain: tuple
    mersenne: int
    number: int
    pure_powers: tuple
    mixed_powers: tuple


def perfect_number(p):
    """Construct the witness for 2 <= p <= 20 when the chain sum is prime."""
    if type(p) is not int or not 2 <= p <= 20:
        raise ValueError("expected integer exponent in 2..20")
    chain=tuple(1<<i for i in range(p))
    m=sum(chain)
    if any(m%d==0 for d in range(2,isqrt(m)+1)):
        raise ValueError("the geometric sum must be prime")
    n=m*chain[-1]
    pure=chain
    mixed=tuple(m*x for x in chain[:-1])
    if sum(pure)+sum(mixed)!=n:
        raise ArithmeticError("proper-divisor sum invariant failed")
    return Witness(chain,m,n,pure,mixed)
