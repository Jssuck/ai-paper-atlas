"""Exact teaching model for Euclid IX.34."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    halving_chain: tuple
    even_pair: tuple
    odd_divisor_pair: tuple
    reversed_mixed_pair: tuple


def mixed_even_types(n):
    """Return both measurement types when the half is even and n is not dyadic."""
    if type(n) is not int or n<2 or n%4:
        raise ValueError("expected an even integer whose half is even")
    chain=[n]
    while chain[-1]%2==0:
        chain.append(chain[-1]//2)
    odd=chain[-1]
    if odd==1:
        raise ValueError("powers of two have no nonunit odd divisor")
    count=2**(len(chain)-1)
    return Witness(tuple(chain),(n//2,2),(odd,count),(count,odd))
