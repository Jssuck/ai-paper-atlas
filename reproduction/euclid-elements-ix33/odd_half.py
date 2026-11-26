"""Exact witness for Euclid IX.33, in measurement order."""
from dataclasses import dataclass


@dataclass(frozen=True)
class OddHalf:
    odd_divisor: int
    even_count: int


def odd_half_witness(n):
    """Return the odd half as divisor and 2 as count."""
    if type(n) is not int or n<3:
        raise ValueError("expected a nonunit even input with nonunit odd half")
    half,remainder=divmod(n,2)
    if remainder or half%2==0:
        raise ValueError("the whole must be even and its half odd")
    return OddHalf(half,2)


def even_factor_counts(n):
    """Modern diagnostics: (odd divisor/even count, even divisor/even count)."""
    if type(n) is not int or n<2:
        raise ValueError("expected integer n >= 2")
    mixed,even=[],[]
    for divisor in range(2,n//2+1):
        count,remainder=divmod(n,divisor)
        if not remainder and count%2==0:
            (mixed if divisor%2 else even).append((divisor,count))
    return tuple(mixed),tuple(even)
