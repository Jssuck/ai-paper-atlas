"""Exact positive-integer teaching model of Euclid IX.15."""
from dataclasses import dataclass
from math import gcd, isqrt


@dataclass(frozen=True)
class SumCertificate:
    chain: tuple
    sums: tuple
    common_divisors: tuple
    modern_unit: bool


def coprime_sums(a, b):
    """Use coprime roots to check each term against the sum of the others."""
    if any(type(n) is not int or n < 1 for n in (a,b)) or gcd(a,b) != 1:
        raise ValueError("expected positive coprime integer roots")
    chain=(a*a,a*b,b*b)
    sums=tuple(sum(chain)-x for x in chain)
    common=tuple(gcd(x,y) for x,y in zip(chain,sums))
    if common != (1,1,1):
        raise ArithmeticError("coprime sum invariant failed")
    return SumCertificate(chain,sums,common,1 in (a,b))


def normalize_chain(x,y,z):
    """Modern adapter: reduce an ordered integer GP and report discarded scale."""
    if any(type(n) is not int or n < 1 for n in (x,y,z)) or x*z != y*y:
        raise ValueError("expected three positive integers in continued proportion")
    scale=gcd(x,y,z)
    result=coprime_sums(isqrt(x//scale),isqrt(z//scale))
    if tuple(scale*t for t in result.chain)!=(x,y,z):
        raise ArithmeticError("least-chain invariant failed")
    return scale,result
