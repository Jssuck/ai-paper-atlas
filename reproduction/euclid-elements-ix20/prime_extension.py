"""Construct a new prime for a supplied finite nonempty prime set."""
from dataclasses import dataclass
from math import isqrt,prod


def least_divisor(n):
    """Least divisor > 1 of integer n >= 2, including n if prime."""
    if type(n) is not int or n < 2:
        raise ValueError("expected an integer at least 2")
    for d in range(2,isqrt(n)+1):
        if n%d==0:
            return d
    return n


@dataclass(frozen=True)
class Extension:
    given: tuple
    multiple: int
    next_number: int
    new_prime: int
    cofactor: int


def extend_primes(members):
    supplied=tuple(members)
    if not supplied or any(least_divisor(p)!=p for p in supplied):
        raise ValueError("expected a nonempty collection of primes")
    given=tuple(sorted(set(supplied)))
    multiple=prod(given)
    n=multiple+1
    p=least_divisor(n)
    if p in given:
        raise ArithmeticError("new prime was in the given collection")
    return Extension(given,multiple,n,p,n//p)
