"""Exact positive-integer model of Euclid IX.14."""
from math import isqrt, prod


def prime(n):
    return type(n) is int and n >= 2 and all(n%d for d in range(2,isqrt(n)+1))


def _unique(members):
    values=tuple(members)
    if not values or not all(prime(p) for p in values):
        raise ValueError("supply a nonempty list of primes")
    return tuple(sorted(set(values)))


def prime_lcm(members):
    """Construct the least common multiple from distinct prescribed primes."""
    return prod(_unique(members))


def strip_foreign_prime(members, candidate, p):
    """Verify a forbidden extra prime witness and remove one copy."""
    values=_unique(members)
    if not prime(p) or p in values:
        raise ValueError("p must be a prime outside the prescribed set")
    if type(candidate) is not int or candidate<1 or any(candidate%x for x in values):
        raise ValueError("candidate must be a positive common multiple")
    reduced,rem=divmod(candidate,p)
    if rem:
        raise ValueError("p does not divide the candidate")
    if not 0<reduced<candidate or any(reduced%x for x in values):
        raise ArithmeticError("foreign prime removal must preserve common multiplicity")
    return reduced
