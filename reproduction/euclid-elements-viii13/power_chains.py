"""Exact stitched power chains for Euclid VIII.13."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class PowerChain:
    local: tuple[tuple[int,...],...]
    stitched: tuple[int,...]
    extracted: tuple[int,...]


def construct(xs,power,*,modern=False):
    xs = tuple(xs)
    if len(xs)<3 or any(type(x) is not int or x < (1 if modern else 2) for x in xs):
        raise ValueError("need at least three positive integer terms (nonunits by default)")
    if type(power) is not int or power not in (2,3):
        raise ValueError("power must be 2 or 3")
    a,b = xs[:2]
    if any(a*y != b*x for x,y in zip(xs,xs[1:])):
        raise ValueError("adjacent ratios differ")
    if a == b and not modern:
        raise ValueError("constant chains require modern=True")
    local = tuple(tuple(x**(power-k)*y**k for k in range(power+1))
                  for x,y in zip(xs,xs[1:]))
    stitched = local[0] + tuple(t for row in local[1:] for t in row[1:])
    extract = stitched[::power]
    step = Fraction(b,a)
    if (any(Fraction(y,x)!=step for x,y in zip(stitched,stitched[1:]))
            or any(Fraction(y,x)!=step**power for x,y in zip(extract,extract[1:]))):
        raise ArithmeticError("continued ratio certificate failed")
    return PowerChain(local,stitched,extract)


if __name__ == "__main__":
    for k in (2,3):
        print(k,construct((4,6,9),k))
