"""Exact arithmetic teaching model for Euclid VII.36."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    pair_multiple: int
    result: int
    branch: str


def pair(a, b):
    return (a // gcd(a, b)) * b


def construct(a, b, c, *, modern=False):
    lower = 1 if modern else 2
    if any(type(x) is not int or x < lower for x in (a,b,c)):
        raise ValueError("inputs must be positive integers, nonunits by default")
    m = pair(a,b)
    if m%c == 0:
        return Trace(m,m,"already measured")
    return Trace(m,pair(m,c),"second construction")


def transfer(a, b, c, target, *, modern=False):
    t = construct(a,b,c,modern=modern)
    if type(target) is not int or target <= 0 or any(target%x for x in (a,b,c)):
        raise ValueError("target must be a positive common multiple")
    if target%t.pair_multiple or target%t.result:
        raise ArithmeticError("VII.35 divisibility did not transfer")
    return target//t.pair_multiple,target//t.result


if __name__ == "__main__":
    for values in ((12,18,9),(6,10,14)):
        print(values,construct(*values))
