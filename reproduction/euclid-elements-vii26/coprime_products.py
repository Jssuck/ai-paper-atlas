"""Exact teaching reconstruction of Euclid VII.26."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Step:
    factors: tuple[int,int]
    against: int
    product: int


def vii24(x,y,z):
    if any(type(t) is not int or t <= 1 for t in (x,y,z)):
        raise ValueError("given numbers must be integers greater than one")
    if gcd(x,z) != 1 or gcd(y,z) != 1:
        raise ValueError("a cross-group pair is not coprime")
    p = sum(x for _ in range(y))
    if gcd(p,z) != 1:
        raise ArithmeticError("VII.24 result failed")
    return Step((x,y),z,p)


def prove(a,b,c,d):
    against_c = vii24(a,b,c)
    against_d = vii24(a,b,d)
    e = against_c.product
    if against_d.product != e:
        raise ArithmeticError("the same two factors yielded different products")
    against_e = vii24(c,d,e)
    return against_c, against_d, against_e


if __name__ == "__main__":
    print(prove(45,75,26,77))
