"""Exact reconstruction of the square bridge and two cube means."""
from dataclasses import dataclass
from math import gcd


def cube_root(n):
    low, high = 0, 1 << ((n.bit_length()+2)//3)
    while low+1 < high:
        mid = (low+high)//2
        if mid**3 <= n:
            low = mid
        else:
            high = mid
    return low


@dataclass(frozen=True)
class Trace:
    sides: tuple[int,int]
    squares: tuple[int,int,int]
    scale: int
    chain: tuple[int,int,int,int]


def _construct(c,d,scale):
    e,f,g = c*c,c*d,d*d
    a,h,k,b = (scale*x for x in (c*e,c*f,d*f,d*g))
    if h*h != a*k or k*k != h*b or a*d**3 != b*c**3:
        raise ArithmeticError("continued ratio certificate failed")
    return Trace((c,d),(e,f,g),scale,(a,h,k,b))


def from_sides(c,d):
    if any(type(x) is not int or x < 2 for x in (c,d)) or c == d:
        raise ValueError("need distinct nonunit positive integer sides")
    return _construct(c,d,1)


def between(a,b):
    """Modern positive integer extension, or None if no two integer means."""
    if any(type(x) is not int or x < 1 for x in (a,b)):
        raise ValueError("endpoints must be positive integers")
    g = gcd(a,b)
    u,v = a//g,b//g
    c,d = cube_root(u),cube_root(v)
    return _construct(c,d,g) if (c**3,d**3) == (u,v) else None


if __name__ == "__main__":
    print(from_sides(2,3))
    print(between(16,54))
