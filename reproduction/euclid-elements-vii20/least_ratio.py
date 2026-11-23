"""Exact integer-count teaching reconstruction of Euclid VII.20."""
from dataclasses import dataclass
from math import gcd
from typing import Optional


def check_pair(a,b,minimum):
    if any(type(x) is not int or x < minimum for x in (a,b)):
        raise ValueError("pair terms are below the domain minimum")


def least(a,b):
    """Modern extension, including the unit, without a proper-part restriction."""
    check_pair(a,b,1)
    g = gcd(a,b)
    return (a//g,b//g),g


@dataclass(frozen=True)
class Trace:
    block: tuple[int,int]
    scales: tuple[int,int]
    prefixes: tuple[tuple[int,int],...]
    is_least: bool
    fraction_counts: tuple[int,int]
    historical_block: Optional[tuple[int,int]]


def candidate(a,b,c,d):
    """Test whether the proposed lower pair (c,d) is least in the restricted model."""
    check_pair(a,b,2)
    check_pair(c,d,2)
    (m,n),full_scale = least(a,b)
    reduced,small_scale = least(c,d)
    if not (1 < m < n) or not (c < a and d < b) or (m,n) != reduced:
        raise ValueError("requires a smaller proportional pair with proper nonunit blocks")
    # Alternate: c:a=d:b=small_scale:full_scale. Pool a pair
    # per step; each has the same count of primitive blocks on both sides.
    if c*full_scale != a*small_scale or d*full_scale != b*small_scale:
        raise ArithmeticError("candidate scaling disagrees")
    prefixes = tuple((i*m,i*n) for i in range(1,small_scale+1))
    if prefixes[-1] != (c,d):
        raise ArithmeticError("candidate was not reconstructed")
    divisor = gcd(small_scale,full_scale)
    fraction = small_scale//divisor,full_scale//divisor
    # A proper single part is a distinct historical branch, even if its
    # corresponding candidate is nonminimal by the modern primitive test.
    historical_block = (m*divisor,n*divisor) if fraction[0] > 1 else None
    return Trace((m,n),(small_scale,full_scale),prefixes,small_scale==1,
                 fraction,historical_block)
