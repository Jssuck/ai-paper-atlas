"""Exact nonunit measurement witness for Euclid VII.37."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Part:
    divisor: int
    quotient: int
    reversed_count: int


def extract(a, b, *, modern=False):
    lower = 1 if modern else 2
    if any(type(x) is not int or x < lower for x in (a,b)):
        raise ValueError("positive integers required, nonunits by default")
    c,r = divmod(a,b)
    if r or c < lower:
        raise ValueError("need exact measurement with a nonunit count by default")
    # VII.15 transfers equal measure counts; here we express it by swapping factors.
    if sum(c for _ in range(b)) != a:
        raise ArithmeticError("reversed measurement failed")
    return Part(b,c,b)


if __name__ == "__main__":
    print(extract(12,3))
