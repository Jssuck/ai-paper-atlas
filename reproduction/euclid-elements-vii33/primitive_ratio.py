"""Exact finite teaching implementation of Euclid VII.33."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Trace:
    least: tuple[int, ...]
    scale: int
    prefix_measures: tuple[int, ...]


def primitive(numbers):
    numbers = tuple(numbers)
    if len(numbers) < 2 or any(type(x) is not int or x <= 1 for x in numbers):
        raise ValueError("need at least two given integers greater than one")
    measures = []
    current = 0
    for x in numbers:
        current = gcd(current,x)
        measures.append(current)
    least = tuple(x//current for x in numbers)
    return Trace(least,current,tuple(measures))


def matching_scale(numbers, candidate):
    """If candidate matches the ratio of numbers, certify its scale from least."""
    t = primitive(numbers)
    candidate = tuple(candidate)
    if len(candidate) != len(t.least) or any(type(x) is not int or x < 1 for x in candidate):
        raise ValueError("candidate must be a matching-length positive integer tuple")
    count, remainder = divmod(candidate[0],t.least[0])
    if remainder or tuple(x*count for x in t.least) != candidate:
        raise ValueError("candidate does not have the ordered ratio")
    return count


if __name__ == "__main__":
    print(primitive((18,30,45)))
