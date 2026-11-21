"""Exact positive-rational model of Elements V.23; not general magnitude arithmetic."""
from fractions import Fraction


def magnitude(x):
    if type(x) not in (int, Fraction):
        raise TypeError("magnitudes must be int or Fraction, not bool or float")
    if x <= 0:
        raise ValueError("magnitudes must be positive")
    return Fraction(x)


def multiplier(n):
    if type(n) is not int:
        raise TypeError("multipliers must be integers, not bool")
    if n <= 0:
        raise ValueError("multipliers must be positive")
    return n


def compare(x, y):
    return (x > y) - (x < y)


def probe(left, right, p, q):
    """Evaluate one multiplier pair. Signs -1/0/1 mean less/equal/greater."""
    a, b, c = map(magnitude, left)
    d, e, f = map(magnitude, right)
    p, q = multiplier(p), multiplier(q)
    if a / b != e / f or b / c != d / e:
        raise ValueError("the perturbed proportion premises must both hold")
    g, h, k, l, m, n = p*a, p*b, p*d, q*c, q*e, q*f

    # Original, treated as one common kind. Each pair records the two ratios.
    original = (
        (g/h, a/b), (e/f, m/n), (g/h, m/n),
        (b/d, c/e), (h/k, b/d), (c/e, l/m), (h/k, l/m), (h/l, k/m),
    )
    # Teaching alternative: V.4 on B:C ~ D:E with p on antecedents and q on consequents.
    # The unchanged first-pair proof works whether or not both groups share a kind.
    alternative = ((g/h, a/b), (e/f, m/n), (g/h, m/n), (h/l, k/m))
    signs = compare(g, l), compare(k, n)
    return {"scaled": (g, h, k, l, m, n), "original": original,
            "alternative": alternative, "signs": signs}


def first_mismatch(left_ratio, right_ratio, limit):
    """Bounded Definition 5 search: None means no mismatch in this box only."""
    a, c = map(magnitude, left_ratio)
    d, f = map(magnitude, right_ratio)
    limit = multiplier(limit)
    for p in range(1, limit + 1):
        for q in range(1, limit + 1):
            if compare(p*a, q*c) != compare(p*d, q*f):
                return p, q
    return None
