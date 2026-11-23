"""Exact finite reconstruction of Euclid VII.29."""
from dataclasses import dataclass
from math import gcd, isqrt


def given(*xs):
    if any(type(x) is not int or x < 2 for x in xs):
        raise ValueError("given numbers must be integers greater than one")


def prime(p):
    given(p)
    return all(p % d for d in range(2,isqrt(p)+1))


@dataclass(frozen=True)
class Trace:
    common_measure: int
    remainder: int
    coprime: bool


def inspect(p, n):
    given(p,n)
    d = gcd(p,n)
    return Trace(d,n%p,d==1)


def common_witness(p, n, d):
    """A nonunit common measure of a prime must equal that prime."""
    given(p,n,d)
    if not prime(p):
        raise ValueError("P must be prime")
    if p%d or n%d:
        raise ValueError("D does not measure both numbers")
    if d != p:
        raise ArithmeticError("prime admitted a proper nonunit measure")
    return divmod(n,d)[0]


def prove(p,n):
    given(p,n)
    if not prime(p):
        raise ValueError("P must be prime")
    if n%p == 0:
        raise ValueError("P must not measure N")
    t = inspect(p,n)
    if t.common_measure > 1:
        count = common_witness(p,n,t.common_measure)
        raise ArithmeticError(f"a common measure would imply P measures N {count} times")
    return t


if __name__ == "__main__":
    print(prove(7,15))
