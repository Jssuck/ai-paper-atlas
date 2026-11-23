"""Integer-count reconstruction of Euclid VII.14."""
from dataclasses import dataclass
from math import gcd


def ratio(a, b):
    g = gcd(a, b)
    return a // g, b // g


@dataclass(frozen=True)
class Trace:
    adjacent: tuple
    vertical: tuple
    shared: tuple
    endpoints: tuple


def ex_aequali(left, right):
    left, right = tuple(left), tuple(right)
    if len(left) != len(right) or len(left) < 3:
        raise ValueError("need two equally long sequences of at least three terms")
    if any(type(x) is not int or x <= 1 for x in left + right):
        raise ValueError("given numbers must be integers greater than one")
    if (any(a >= b for a, b in zip(left, left[1:]))
            or any(a >= b for a, b in zip(right, right[1:]))
            or any(a >= b for a, b in zip(left, right))):
        raise ValueError("this direct teaching model requires proper directions")
    adjacent = []
    vertical = [ratio(left[0], right[0])]
    shared = vertical[0]
    for i in range(1, len(left)):
        local = ratio(left[i-1], left[i])
        if local != ratio(right[i-1], right[i]):
            raise ValueError(f"adjacent ratios disagree at step {i}")
        adjacent.append(local)
        # Alternate this adjacent quartet, then extend the shared column ratio.
        current = ratio(left[i], right[i])
        if current != vertical[-1] or current != shared:
            raise ArithmeticError("alternation or transitivity failed")
        vertical.append(current)
    # Alternate back on the first and last columns.
    endpoints = ratio(left[0], left[-1])
    if endpoints != ratio(right[0], right[-1]):
        raise ArithmeticError("endpoint alternation failed")
    return Trace(tuple(adjacent), tuple(vertical), shared, endpoints)


def demo():
    for left, right in (((4,6,10),(10,15,25)), ((4,6,10,14),(10,15,25,35))):
        print(left, right, ex_aequali(left, right))


if __name__ == "__main__":
    demo()
