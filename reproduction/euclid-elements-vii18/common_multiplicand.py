"""Exact arithmetic teaching reconstruction of Euclid VII.18."""
from dataclasses import dataclass
from math import gcd


def reduced(x, y):
    g = gcd(x, y)
    return x // g, y // g


@dataclass(frozen=True)
class Trace:
    products: tuple[int, int]
    swapped: tuple[int, int]
    measure_counts: tuple[int, int]
    internal: tuple[int, int]
    ratio: tuple[int, int]


def construct(a, b, c):
    if any(type(x) is not int or x <= 1 for x in (a,b,c)):
        raise ValueError("numbers must be integers greater than one")
    return sum(c for _ in range(a)), sum(c for _ in range(b))


def check_products(a, b, c, d, e):
    if any(type(x) is not int or x <= 1 for x in (d,e)):
        raise ValueError("products must be integers greater than one")
    if (d,e) != construct(a,b,c):
        raise ValueError("products do not have the specified common multiplicand")
    swapped = sum(a for _ in range(c)), sum(b for _ in range(c))
    if swapped != (d,e):
        raise ArithmeticError("VII.16 transport failed")
    measures = divmod(swapped[0],a), divmod(swapped[1],b)
    if measures != ((c,0),(c,0)):
        raise ArithmeticError("VII.17 common count failed")
    internal = reduced(a,d)
    crossed = reduced(a,b)
    if internal != reduced(b,e) or crossed != reduced(d,e):
        raise ArithmeticError("VII.17 ratio check failed")
    return Trace((d,e), swapped, (measures[0][0],measures[1][0]), internal,crossed)


def transport(a, b, c):
    return check_products(a,b,c,*construct(a,b,c))


if __name__ == "__main__":
    print(transport(4,6,3))
