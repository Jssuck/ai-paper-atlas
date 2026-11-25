"""Exact integer endpoint certificate for Euclid VIII.22."""
from math import isqrt


def square_endpoint_roots(a: int, b: int, c: int) -> tuple:
    """Return positive roots of first and third terms, given the hypotheses."""
    if any(type(x) is not int or x < 1 for x in (a, b, c)):
        raise ValueError("expected three positive integers")
    if a*c != b*b:
        raise ValueError("the three terms must be in continued proportion")
    s = isqrt(a)
    if s*s != a:
        raise ValueError("the first term must be a square")
    t, remainder = divmod(b, s)
    if remainder or t*t != c:
        raise ArithmeticError("exact root-transfer invariant failed")
    return s, t
