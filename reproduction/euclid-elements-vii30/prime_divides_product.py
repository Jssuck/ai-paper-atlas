"""Exact arithmetic teaching model of Euclid VII.30."""
from dataclasses import dataclass
from math import gcd, isqrt
from typing import Optional


@dataclass(frozen=True)
class Witness:
    ratio: tuple[int,int]
    compared: tuple[int,int]
    scale: int


@dataclass(frozen=True)
class Trace:
    product: int
    product_quotient: int
    divides: tuple[bool,bool]
    witness: Optional[Witness]


def least_transfer(p, a, b, e):
    """If P and A are coprime and P*E=A*B, transfer the common scale."""
    if gcd(p,a) != 1 or p*e != a*b:
        raise ValueError("need a coprime pair with matching cross products")
    s,r = divmod(b,p)
    t,u = divmod(e,a)
    if r or u or s != t or s < 1:
        raise ArithmeticError("least-ratio counts were not equal")
    return Witness((p,a),(b,e),s)


def prove(p,a,b):
    if any(type(x) is not int or x <= 1 for x in (p,a,b)):
        raise ValueError("given numbers must be integers greater than one")
    if any(p%d == 0 for d in range(2,isqrt(p)+1)):
        raise ValueError("P must be prime")
    c = a*b
    e,r = divmod(c,p)
    if r:
        raise ValueError("P must measure the product")
    left = a%p == 0
    right = b%p == 0
    if not left:
        witness = least_transfer(p,a,b,e)
    elif not right:
        witness = least_transfer(p,b,a,e)
    else:
        witness = None
    return Trace(c,e,(left,right),witness)


if __name__ == "__main__":
    for args in ((7,15,14),(7,14,15),(7,14,21)):
        print(args,prove(*args))
