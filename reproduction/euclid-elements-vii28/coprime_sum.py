"""Exact common-measure transport for Euclid VII.28."""
from math import gcd


def given(*values):
    if any(type(x) is not int or x < 2 for x in values):
        raise ValueError("given numbers must be integers greater than one")


def quotient(x, d):
    q, r = divmod(x, d)
    if r:
        raise ValueError("not a common measure")
    return q


def to_sum(a, b, d):
    given(a, b, d)
    i, j = quotient(a, d), quotient(b, d)
    if d*(i+j) != a+b:
        raise ArithmeticError("addition transport failed")
    return i+j


def from_sum(a, b, d):
    """D measures A and A+B; recover its count in B by subtraction."""
    given(a, b, d)
    i, j = quotient(a, d), quotient(a+b, d)
    if not j > i or d*(j-i) != b:
        raise ArithmeticError("subtraction transport failed")
    return j-i


def check(a, b):
    given(a, b)
    return gcd(a,b), gcd(a,a+b), gcd(b,a+b)


if __name__ == "__main__":
    for a,b in ((8,15),(5,7),(6,9)):
        print((a,b), a+b, check(a,b))
