"""Exact positive-integer construction for Euclid VIII.4."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Step:
    bridge: int
    prefix_scale: int
    pair_scale: int
    prefix: tuple[int,...]


@dataclass(frozen=True)
class Trace:
    terms: tuple[int,...]
    steps: tuple[Step,...]


def construct(ratios, *, modern=False):
    ratios = tuple(ratios)
    if not ratios:
        raise ValueError("need at least one ordered ratio")
    reduced = []
    low = 1 if modern else 2
    for a,b in ratios:
        if any(type(x) is not int or x < low for x in (a,b)):
            raise ValueError("positive integer ratio terms required")
        g = gcd(a,b)
        if min(a//g,b//g) < low:
            raise ValueError("reduced unit or equal ratio needs modern=True")
        reduced.append((a//g,b//g))
    prefix = reduced[0]
    steps = []
    for a,b in reduced[1:]:
        last = prefix[-1]
        bridge = (last//gcd(last,a))*a
        prefix_scale,pair_scale = bridge//last,bridge//a
        prefix = tuple(x*prefix_scale for x in prefix)+(b*pair_scale,)
        steps.append(Step(bridge,prefix_scale,pair_scale,prefix))
    if any(b*x != a*y for (a,b),x,y in zip(reduced,prefix,prefix[1:])):
        raise ArithmeticError("adjacent ratio certificate failed")
    return Trace(prefix,tuple(steps))


if __name__ == "__main__":
    for ds in (((2,3),(5,7),(3,4)),((2,3),(5,7),(4,5))):
        print(construct(ds))
