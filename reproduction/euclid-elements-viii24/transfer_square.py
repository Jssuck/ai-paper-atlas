"""Integer certificates for the square-ratio transfer of Euclid VIII.24."""
from dataclasses import dataclass
from math import gcd, isqrt


@dataclass(frozen=True)
class SquareTrace:
    primitive: tuple
    scale: int
    middle: int
    roots: tuple


def transfer_square(a, b, c, d):
    """Given A:B=C:D and square A,C,D, return a square witness for B."""
    if any(type(n) is not int or n < 1 for n in (a,b,c,d)):
        raise ValueError("expected four positive integers")
    s, u, v = map(isqrt, (a,c,d))
    if (s*s,u*u,v*v) != (a,c,d):
        raise ValueError("A, C and D must be squares")
    if a*d != b*c:
        raise ValueError("the two ordered ratios must agree")
    z = gcd(u,v)
    p,q = u//z,v//z
    primitive = (p*p,p*q,q*q)
    scale, r = divmod(a,primitive[0])
    if r or b != scale*primitive[2]:
        raise ArithmeticError("primitive chain did not measure both target terms")
    middle = scale*primitive[1]
    t, r = divmod(middle,s)
    if r or t*t != b:
        raise ArithmeticError("root transfer failed")
    return SquareTrace(primitive,scale,middle,(s,t))
