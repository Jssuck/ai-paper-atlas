"""Exact finite teaching reconstruction of Euclid VII.25."""
from dataclasses import dataclass
from math import gcd


def given(*values):
    if any(type(x) is not int or x <= 1 for x in values):
        raise ValueError("given numbers must be integers greater than one")


def product_lemma(a, d, b):
    """VII.24 certificate: both factors, not each other, are coprime to B."""
    given(a,d,b)
    if gcd(a,b) != 1 or gcd(d,b) != 1:
        raise ValueError("each factor must be coprime to B")
    product = sum(a for _ in range(d))
    if gcd(product,b) != 1:
        raise ArithmeticError("VII.24 conclusion failed")
    return product


@dataclass(frozen=True)
class Trace:
    factor_slots: tuple[int,int]
    reference: int
    square: int


def square(a,b):
    given(a,b)
    d = a
    return Trace((a,d),b,product_lemma(a,d,b))


if __name__ == "__main__":
    print(square(8,15))
