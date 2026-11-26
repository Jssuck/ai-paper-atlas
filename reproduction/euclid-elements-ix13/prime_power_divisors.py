"""Exact divisor extraction for the positive-integer model of Euclid IX.13."""
from math import isqrt


def _validate(p, n):
    if type(p) is not int or type(n) is not int or p < 2 or n < 1:
        raise ValueError("expected integer base >= 2 and exponent >= 1")
    if any(p % d == 0 for d in range(2, isqrt(p)+1)):
        raise ValueError("base must be prime")


def proper_nonunit_divisors(p, n):
    """Generate the earlier nonunit entries, excluding the target itself."""
    _validate(p,n)
    return tuple(p**e for e in range(1,n))


def extraction_trace(p, n, divisor):
    """Verify a proper nonunit divisor and extract its copies of p."""
    _validate(p,n)
    value = p**n
    if type(divisor) is not int or not 1 < divisor < value or value % divisor:
        raise ValueError("expected a proper nonunit divisor of p**n")
    residue = [divisor]
    while residue[-1] % p == 0:
        residue.append(residue[-1]//p)
    exponent = len(residue)-1
    if residue[-1] != 1 or not 1 <= exponent < n:
        raise ArithmeticError("prime-power divisor invariant failed")
    return exponent, tuple(residue)
