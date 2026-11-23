"""Exact arithmetic witness chain for Euclid VII.27."""
from dataclasses import dataclass
from math import gcd


def binary_gcd(a, b):
    if min(a, b) <= 0:
        raise ValueError("positive integers needed for this binary gcd")
    shift = 0
    while a % 2 == b % 2 == 0:
        a //= 2
        b //= 2
        shift += 1
    while a % 2 == 0:
        a //= 2
    while b:
        while b % 2 == 0:
            b //= 2
        if a > b:
            a, b = b, a
        b -= a
    return a << shift


def vii25(squared_base, reference):
    if gcd(squared_base, reference) != 1:
        raise ValueError("square step needs a coprime base and reference")
    square = squared_base * squared_base
    if gcd(square, reference) != 1:
        raise ArithmeticError("square step failed")
    return square, reference


@dataclass(frozen=True)
class Trace:
    square_steps: tuple
    cross_pairs: tuple
    cubes: tuple[int, int]


def prove(a, b):
    if any(type(x) is not int or x <= 1 for x in (a, b)):
        raise ValueError("given numbers must be greater than one")
    gamma, _ = vii25(a, b)
    epsilon, _ = vii25(b, gamma)
    epsilon_again, _ = vii25(b, a)
    if epsilon != epsilon_again:
        raise ArithmeticError("inconsistent second square")
    cross = ((a,b), (a,epsilon), (gamma,b), (gamma,epsilon))
    if any(gcd(x,y) != 1 for x,y in cross):
        raise ArithmeticError("VII.26 cross conditions failed")
    cubes = a*gamma, b*epsilon
    if gcd(*cubes) != 1:
        raise ArithmeticError("VII.26 result failed")
    return Trace(((gamma,b),(gamma,epsilon),(a,epsilon)),cross,cubes)


if __name__ == "__main__":
    print(prove(8,15))
