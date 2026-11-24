"""Exact reconstruction of Euclid VII.39 on three named unit parts."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    whole: int
    parts: tuple[int,int,int]


def validate(ds,modern):
    if len(ds) != 3 or any(type(x) is not int or x < (1 if modern else 2) for x in ds):
        raise ValueError("three positive integral denominators required, nonunits by default")


def check(whole,*ds,modern=False):
    validate(ds,modern)
    if type(whole) is not int or whole <= 0:
        raise ValueError("whole must be a positive integer")
    parts = []
    for d in ds:
        q,r = divmod(whole,d)
        if r:
            raise ValueError(f"missing named part with denominator {d}")
        parts.append(q)
    return Trace(whole,tuple(parts))


def construct(*ds,modern=False):
    validate(ds,modern)
    whole = 1
    for d in ds:
        whole = (whole // gcd(whole,d))*d
    return check(whole,*ds,modern=modern)


if __name__ == "__main__":
    print(construct(4,6,10))
