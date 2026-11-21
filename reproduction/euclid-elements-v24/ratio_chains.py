"""Exact modern rational trace of Euclid V.24, with an auxiliary lex model."""
from fractions import Fraction


def positive(value):
    if type(value) not in (int, Fraction):
        raise TypeError("expected an int or Fraction")
    if value <= 0:
        raise ValueError("expected a positive magnitude")
    return Fraction(value)


def addition_trace(u, v, w, x, y, z):
    """Input order u,v,w,x,y,z for u:v~w:x and y:v~z:x."""
    u, v, w, x, y, z = map(positive, (u, v, w, x, y, z))
    if u * x != w * v:
        raise ValueError("first premise fails: u:v vs w:x")
    if y * x != z * v:
        raise ValueError("second premise fails: y:v vs z:x")
    return {
        "V.7 cor.": (v / y, x / z),
        "V.22 first": (u / y, w / z),
        "V.18": ((u + y) / y, (w + z) / z),
        "V.22 second": ((u + y) / v, (w + z) / x),
    }


def lex_probe(m, n):
    """Sign pairs for two hypotheses and conclusion, as a non-Archimedean model."""
    if type(m) is not int or type(n) is not int:
        raise TypeError("expected integer multipliers")
    if min(m, n) <= 0:
        raise ValueError("expected positive multipliers")
    u, v, w, x, y, z = (1, 1), (1, 0), (1, 2), (1, 0), (1, -1), (1, -1)

    def cmp(a, b):
        ma, nb = (m * a[0], m * a[1]), (n * b[0], n * b[1])
        return (ma > nb) - (ma < nb)

    return (
        (cmp(u, v), cmp(w, x)),
        (cmp(y, v), cmp(z, x)),
        (cmp((2, 0), v), cmp((2, 1), x)),
    )


def grid_evidence(limit):
    """Enumerate every positive integer sextuple of entries <= limit."""
    from itertools import product
    from math import gcd

    scanned = admissible = 0
    for u, v, w, x, y, z in product(range(1, limit + 1), repeat=6):
        scanned += 1
        # Independent admissibility filter: primitive pair scaling as integers.

        g = gcd(v, x)
        a, b = v // g, x // g
        valid = (u % a == w % b == y % a == z % b == 0
                 and u // a == w // b and y // a == z // b)
        try:
            trace = addition_trace(u, v, w, x, y, z)
        except ValueError:
            if valid:
                raise
            continue
        if not valid:
            raise AssertionError("false acceptance")
        admissible += 1
        for left, right in trace.values():
            if left != right:
                raise AssertionError("a restated ratio differs")
        l, r = trace["V.22 second"]
        if (l.numerator * v != (u + y) * l.denominator or
                r.numerator * x != (w + z) * r.denominator or
                (u + y) * x != (w + z) * v):
            raise AssertionError("conclusion does not match integer oracle")
    return scanned, admissible
