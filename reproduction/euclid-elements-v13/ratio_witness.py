"""Exact rational teaching model for Euclid V.13, not a general magnitude solver."""
from fractions import Fraction
from itertools import product


def magnitude(x):
    if type(x) not in (int, Fraction) or x <= 0:
        raise ValueError("use positive int or Fraction")
    return Fraction(x)


def natural(x):
    if type(x) is not int or x <= 0:
        raise ValueError("use positive integer")
    return x


def quotient(pair):
    a, b = map(magnitude, pair)
    return a / b


def compare(pair, probe):
    a, b = map(magnitude, pair)
    m, n = map(natural, probe)
    left, right = m * a, n * b
    return (left > right) - (left < right)


def is_witness(high, low, probe):
    return compare(high, probe) == 1 and compare(low, probe) <= 0


def find_witness(high, low, cap):
    """First lexicographic probe in the square, or None (not an order verdict)."""
    quotient(high), quotient(low)
    indices = range(1, natural(cap) + 1)
    return next((p for p in product(indices, repeat=2)
                 if is_witness(high, low, p)), None)


def exact_witness(high, low):
    """In this rational model, choose the weaker quotient itself as the threshold."""
    hi, lo = quotient(high), quotient(low)
    if hi <= lo:
        return None
    return lo.denominator, lo.numerator


def transport(first, middle, last, probe):
    """Guard prerequisites, then return the first/middle/last signs at one probe."""
    if quotient(first) != quotient(middle):
        raise ValueError("first and middle ratios must be exactly equal")
    if not is_witness(middle, last, probe):
        raise ValueError("probe must witness middle strictly above last")
    return tuple(compare(pair, probe) for pair in (first, middle, last))


def demo():
    first, middle, last = (3, 2), (6, 4), (2, 2)
    for p in [(1, 1), (4, 5)]:
        print("transport:", p, transport(first, middle, last, p))
    p = (2, 3)
    print("equality at the high endpoint is not a witness:", is_witness(middle, last, p))
    print("reverse direction at (1, 1):", is_witness(last, middle, (1, 1)))
    close_high, close_low = (102, 100), (101, 100)
    print("bounded close witness (cap 20):", find_witness(close_high, close_low, 20))
    print("bounded close witness (cap 60):", find_witness(close_high, close_low, 60))
    p = exact_witness(close_high, close_low)
    print("exact close witness:", p, tuple(compare(x, p) for x in (close_high, close_low)))


if __name__ == "__main__":
    demo()
