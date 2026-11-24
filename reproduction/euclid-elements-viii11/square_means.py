"""Exact integer teaching model for Euclid VIII.11; no floating point."""
from fractions import Fraction
from math import isqrt


def positive_integer(*values):
    for value in values:
        if type(value) is not int or value < 1:
            raise ValueError("expected a positive Python integer")


def from_sides(c, d):
    """Return endpoint-middle-endpoint in input order, and the two ratios."""
    positive_integer(c, d)
    a, e, b = c*c, c*d, d*d
    return (a, e, b), Fraction(c, d), Fraction(a, b)


def integer_mean(a, b):
    """Modern extension: return the unique positive integer mean, or None."""
    positive_integer(a, b)
    product = a*b
    root = isqrt(product)
    return root if root*root == product else None


def is_mean(a, e, b):
    """Verify a proposed middle by cross multiplication."""
    positive_integer(a, e, b)
    return a*b == e*e
