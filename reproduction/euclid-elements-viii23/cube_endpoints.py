"""Exact integer endpoint certificate for Euclid VIII.23."""


def floor_cuberoot(n: int) -> int:
    """Return the greatest integer r >= 0 with r**3 <= n."""
    if type(n) is not int or n < 0:
        raise ValueError("expected a nonnegative integer")
    low, high = 0, 1 << ((n.bit_length()+2)//3)
    while low+1 < high:
        mid = (low+high)//2
        if mid**3 <= n:
            low = mid
        else:
            high = mid
    return low


def cube_endpoint_roots(a: int, b: int, c: int, d: int) -> tuple:
    """Given four terms in continued proportion starting with a cube, return both endpoint roots."""
    if any(type(x) is not int or x < 1 for x in (a,b,c,d)):
        raise ValueError("expected four positive integers")
    if a*c != b*b or b*d != c*c:
        raise ValueError("the four terms must be in continued proportion")
    s = floor_cuberoot(a)
    if s**3 != a:
        raise ValueError("the first term must be a cube")
    t, remainder = divmod(b,s*s)
    if remainder or t**3 != d:
        raise ArithmeticError("exact cube-root transfer invariant failed")
    return s,t
