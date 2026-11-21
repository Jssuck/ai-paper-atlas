"""Exact rational demonstration of Euclid V.25; not a general magnitude solver."""
from dataclasses import dataclass
from fractions import Fraction


def positive(value):
    if type(value) not in (int, Fraction):
        raise TypeError("use an int or Fraction, not a boolean or floating-point value")
    value = Fraction(value)
    if value <= 0:
        raise ValueError("magnitudes and parameters must be positive")
    return value


@dataclass(frozen=True)
class Trace:
    copied_parts: tuple[Fraction, Fraction]
    remainders: tuple[Fraction, Fraction]
    common_ratio: Fraction
    equal_addends: tuple[Fraction, Fraction]
    sums: tuple[Fraction, Fraction]
    gap: Fraction


def v25(a, b, c, d):
    """a:b ~ c:d, a uniquely largest, d uniquely smallest; b=c is allowed."""
    a, b, c, d = map(positive, (a, b, c, d))
    if a * d != b * c:
        raise ValueError("expected a:b ~ c:d")
    if not (a > max(b, c) and d < min(b, c)):
        raise ValueError("strict extrema required; the middle terms may be equal")
    # The copied parts AG and CH are c and d.
    u, v = a - c, b - d
    ratio = a / b
    # V.19 and V.Def.5 at unit multiples, checked numerically.
    if u / v != ratio or not u > v:
        raise ArithmeticError("remainder checkpoint failed")
    addends = (c + d, d + c)
    sums = (u + addends[0], v + addends[1])
    gap = sums[0] - sums[1]
    if sums != (a + d, b + c) or gap <= 0:
        raise ArithmeticError("add-back checkpoint failed")
    return Trace((c, d), (u, v), ratio, addends, sums, gap)


def parameterized(d, r, s):
    """Independent product parameterization: d, r=a/b=c/d, s=b/d."""
    d, r, s = map(positive, (d, r, s))
    if r <= 1 or s <= 1:
        raise ValueError("r and s must both exceed one")
    return (r * s * d, s * d, r * d, d), (r - 1) * (s - 1) * d


def lex_sign(a, b, m, n):
    """Compare m*a and n*b in the lexicographically ordered integer pairs."""
    if type(m) is not int or type(n) is not int or min(m, n) < 1:
        raise ValueError("multipliers must be positive integers")
    left, right = tuple(m * x for x in a), tuple(n * x for x in b)
    return (left > right) - (left < right)


def joyce_signs(m, n):
    """Return the two premise signs, then the proposed sum comparison sign."""
    a, b, c, d = ((1, offset) for offset in (5, 2, 4, 0))
    return (lex_sign(a, b, m, n), lex_sign(c, d, m, n),
            lex_sign((2, 5), (2, 6), m, n))
