"""Exact integer-count teaching model of VII.11."""
from dataclasses import dataclass
from math import gcd


def reduced(x: int, y: int) -> tuple[int, int]:
    measure = gcd(x, y)
    return x // measure, y // measure


@dataclass(frozen=True)
class Trace:
    counts: tuple[int, int]
    removal: tuple[int, int]
    remainders: tuple[int, int]
    remainder_counts: tuple[int, int]
    subtraction: str


def subtract(ab: int, cd: int, ae: int, cf: int) -> Trace:
    if any(type(x) is not int or x <= 1 for x in (ab, cd, ae, cf)):
        raise ValueError("given numbers must be integers greater than one")
    if not (ab < cd and ae < ab and cf < cd):
        raise ValueError("require AB<CD and proper removals")
    counts = reduced(ab, cd)
    if counts != reduced(ae, cf):
        raise ValueError("original and removed pairs must have the same part(s)")
    removal = reduced(ae, ab)
    if removal != reduced(cf, cd):
        raise ArithmeticError("alternation to internal removal failed")
    remainders = ab - ae, cd - cf
    remainder_counts = reduced(*remainders)
    # Def.20 in the modern counting reconstruction: same reduced part(s)
    # in the original and remainder comparisons is the same ratio.
    if remainder_counts != counts:
        raise ArithmeticError("remainders did not preserve reduced counts")
    return Trace(counts, removal, remainders, remainder_counts,
                 "VII.7" if counts[0] == 1 else "VII.8")


def demo():
    for args in ((12,36,4,12), (18,30,6,10), (3,6,2,4)):
        print(args, subtract(*args))


if __name__ == "__main__":
    demo()
