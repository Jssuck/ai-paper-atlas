"""Exact integer teaching certificate for Euclid VIII.25."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class CubeTrace:
    primitive: tuple
    scale: int
    means: tuple
    roots: tuple


def exact_cuberoot(n):
    low, high = 0, 1 << ((n.bit_length()+2)//3)
    while low+1 < high:
        middle = (low+high)//2
        if middle**3 <= n:
            low = middle
        else:
            high = middle
    if low**3 != n:
        raise ValueError("A, C and D must be cubes")
    return low


def transfer_cube(a, b, c, d):
    """Given A:B=C:D and cube A,C,D, construct and verify a cube root of B."""
    if any(type(n) is not int or n < 1 for n in (a,b,c,d)):
        raise ValueError("expected four positive integers")
    s,u,v = map(exact_cuberoot,(a,c,d))
    if a*d != b*c:
        raise ValueError("the two oriented ratios must agree")
    z = gcd(u,v)
    p,q = u//z,v//z
    primitive = (p**3,p*p*q,p*q*q,q**3)
    scale, rem = divmod(a,primitive[0])
    if rem or scale*primitive[3] != b:
        raise ArithmeticError("least ratio did not measure both target terms")
    first, second = scale*primitive[1],scale*primitive[2]
    t, rem = divmod(first,s*s)
    if rem or t**3 != b or s*t*t != second:
        raise ArithmeticError("cube-root transfer invariant failed")
    return CubeTrace(primitive,scale,(first,second),(s,t))
