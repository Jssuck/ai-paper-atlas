"""Teaching arithmetic for Euclid VII.34."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    branch: str
    measure: int
    least_ratio: tuple[int,int]
    multiple: int


def construct(a,b):
    if any(type(x) is not int or x <= 1 for x in (a,b)):
        raise ValueError("supply two integers greater than one")
    g = gcd(a,b)
    x,y = a//g,b//g
    if a*y != b*x:
        raise ArithmeticError("crossed products disagree")
    return Trace("coprime" if g == 1 else "noncoprime",g,(x,y),a*y)


def multiple_witness(a,b,c):
    """Claimed common multiple yields counts and a scale from the least ratio."""
    t = construct(a,b)
    if type(c) is not int or c <= 0:
        raise ValueError("claimed multiple must be a positive integer")
    m,r = divmod(c,b)
    n,s = divmod(c,a)
    if r or s:
        raise ValueError("number is not a common multiple")
    k,q = divmod(m,t.least_ratio[0])
    if q or k < 1 or n != k*t.least_ratio[1] or c != k*t.multiple:
        raise ArithmeticError("VII.20 scale check failed")
    return (m,n),k


if __name__ == "__main__":
    for a,b in ((12,18),(8,15)):
        print(a,b,construct(a,b))
