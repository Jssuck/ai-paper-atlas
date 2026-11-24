"""Exact teaching reconstruction of Euclid VII.35."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    quotient: int
    remainder: int
    remainder_counts: tuple[int,int]


def close_difference(a,b,step,target):
    if any(type(x) is not int or x <= 0 for x in (a,b,step,target)):
        raise ValueError("expected positive integers")
    if any(n%d for n in (step,target) for d in (a,b)):
        raise ValueError("step and target must both be common multiples")
    q,r = divmod(target,step)
    counts = tuple(target//d - q*(step//d) for d in (a,b))
    if any(k*d != r for k,d in zip(counts,(a,b))):
        raise ArithmeticError("remainder did not inherit both measures")
    return Trace(q,r,counts)


def verify_least_divides(a,b,target):
    if any(type(x) is not int or x <= 0 for x in (a,b,target)):
        raise ValueError("expected positive integers")
    least = (a//gcd(a,b))*b
    t = close_difference(a,b,least,target)
    if t.remainder:
        raise ArithmeticError("positive common remainder contradicts minimality")
    return t
