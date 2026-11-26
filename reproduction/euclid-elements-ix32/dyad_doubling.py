"""Strict nonunit factor-pair model for Euclid IX.32."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Classification:
    doublings: int
    odd_core: int
    even_pairs: tuple
    odd_factor_pairs: tuple


def odd_core(n):
    if type(n) is not int or n<2:
        raise ValueError("expected an integer >= 2")
    e=0
    while n%2==0:
        e+=1
        n//=2
    return n,e


def classify(n):
    """Return unordered nonunit pairs, excluding endpoints 1 and n."""
    core,e=odd_core(n)
    even,mixed=[],[]
    d=2
    while d*d<=n:
        quotient,remainder=divmod(n,d)
        if not remainder:
            (even if d%2==quotient%2==0 else mixed).append((d,quotient))
        d+=1
    return Classification(max(0,e-1),core,tuple(even),tuple(mixed))


def doubled_dyad(steps):
    """Construct the term after at least one doubling of 2."""
    if type(steps) is not int or steps<1:
        raise ValueError("expected at least one doubling after the dyad")
    n=2
    for _ in range(steps):
        n+=n
    return n
