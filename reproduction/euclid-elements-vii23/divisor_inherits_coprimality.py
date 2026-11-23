"""Exact teaching checks for Euclid VII.23."""
from dataclasses import dataclass
from math import gcd


def valid(*xs):
    if any(type(x) is not int or x <= 1 for x in xs):
        raise ValueError("given numbers must be integers greater than one")


@dataclass(frozen=True)
class Transfer:
    divisions: tuple[int, int, int]
    a_over_d: int


def transfer(a,b,c,d):
    """Transport a hypothesized common measure D of C and B to A and B."""
    valid(a,b,c,d)
    u, r = divmod(a,c)
    v, s = divmod(c,d)
    w, t = divmod(b,d)
    if r or s or t:
        raise ValueError("require D | C | A and D | B")
    q = u*v
    if divmod(a,d) != (q,0):
        raise ArithmeticError("composed division failed")
    return Transfer((u,v,w),q)


def inherit(a,b,c):
    valid(a,b,c)
    u,r = divmod(a,c)
    if r:
        raise ValueError("C must divide A")
    if gcd(a,b) != 1:
        raise ValueError("A and B must be coprime")
    d = gcd(c,b)
    if d > 1:
        certificate = transfer(a,b,c,d)
        raise ArithmeticError(f"would give common nonunit measure of A and B: {certificate}")
    return u,d


if __name__ == "__main__":
    print(inherit(35,12,5))
    print(transfer(12,9,6,3))
