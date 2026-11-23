"""Exact integer certificates for the two directions of Euclid VII.19."""
from dataclasses import dataclass
from math import gcd


def reduced(x, y):
    g = gcd(x, y)
    return x // g, y // g


@dataclass(frozen=True)
class Trace:
    g: int
    e: int
    f: int
    first: tuple[int, int]
    second: tuple[int, int]
    ratios_equal: bool
    products_equal: bool


def check(a, b, c, d):
    if any(type(x) is not int or x <= 1 for x in (a,b,c,d)):
        raise ValueError("given numbers must be integers greater than one")
    g, e, f = (sum(term for _ in range(copies))
               for copies,term in ((a,c),(a,d),(b,c)))
    first, second = reduced(a,b), reduced(c,d)
    gf, ge = reduced(g,f), reduced(g,e)
    if first != gf or second != ge:
        raise ArithmeticError("VII.17 or VII.18 certificate failed")
    # Forward: equal reduced forms with the same fixed positive numerator
    # imply identical gcd scaling factors, hence identical denominators.
    ratios_equal = first == second
    if ratios_equal:
        common_numerator = gf[0]
        scale = g // common_numerator
        if f != gf[1]*scale or e != gf[1]*scale:
            raise ArithmeticError("fixed positive numerator was not injective")
    # Reverse: E=F makes G:E and G:F the identical ordered pair.
    products_equal = e == f
    if products_equal and not (gf == ge == first == second):
        raise ArithmeticError("substitution into the two ratio certificates failed")
    return Trace(g,e,f,first,second,ratios_equal,products_equal)


if __name__ == "__main__":
    print(check(4,6,10,15))
    print(check(4,6,10,16))
