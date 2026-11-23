"""An integer-count teaching version of Euclid VII.12."""
from dataclasses import dataclass
from math import gcd


def counts(a, b):
    g = gcd(a, b)
    return a // g, b // g


@dataclass(frozen=True)
class Trace:
    ratio_counts: tuple[int, int]
    branch: str
    prefixes: tuple[tuple[int, int], ...]
    total: tuple[int, int]


def pool(pairs):
    pairs = tuple(pairs)
    if len(pairs) < 2:
        raise ValueError("need at least two paired comparisons")
    for a, b in pairs:
        if type(a) is not int or type(b) is not int or not 1 < a < b:
            raise ValueError("each pair must be integers with 1 < a < b")
    common = counts(*pairs[0])
    if any(counts(a, b) != common for a, b in pairs):
        raise ValueError("original pairs must all have the same reduced counts")
    total_a = total_b = 0
    prefixes = []
    for a, b in pairs:
        total_a += a
        total_b += b
        if counts(total_a, total_b) != common:
            raise ArithmeticError("prefix aggregation failed")
        prefixes.append((total_a, total_b))
    return Trace(common, "VII.5" if common[0] == 1 else "VII.6",
                 tuple(prefixes), prefixes[-1])


def demo():
    for pairs in (((4,12),(5,15),(7,21)), ((2,3),(6,9),(8,12))):
        print(pairs, pool(pairs))


if __name__ == "__main__":
    demo()
