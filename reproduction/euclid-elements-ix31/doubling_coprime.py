"""Exact bounded teaching model of Euclid IX.31."""


def common_divisors(a, b):
    """Direct enumeration of nonunit common divisors of positive integers."""
    if any(type(x) is not int or x < 1 for x in (a, b)):
        raise ValueError("expected positive integers")
    return tuple(d for d in range(2, min(a,b)+1) if a%d == b%d == 0)


def transfer_double_measure(a,b,d):
    """Given a common nonunit divisor of odd A and 2B, return its quotient in B."""
    if any(type(x) is not int for x in (a,b,d)) or a<3 or b<2 or d<2 or a%2!=1:
        raise ValueError("expected odd A >= 3, B >= 2, and nonunit divisor")
    twice,remainder=divmod(2*b,d)
    if remainder or a%d:
        raise ValueError("candidate must divide A and twice B")
    half,odd=divmod(twice,2)
    if d%2!=1 or odd or d*half!=b:
        raise ArithmeticError("odd-divisor transfer invariant failed")
    return half


def doubled_coprime(a,b):
    """Check original coprime premises, then reject any possible doubled common divisor."""
    if any(type(x) is not int for x in (a,b)) or a<3 or b<2 or a%2!=1:
        raise ValueError("expected odd A >= 3 and B >= 2")
    if common_divisors(a,b):
        raise ValueError("A and B must be coprime")
    for d in common_divisors(a,2*b):
        transfer_double_measure(a,b,d)
        raise ArithmeticError("contradictory common divisor")
    return 2*b
