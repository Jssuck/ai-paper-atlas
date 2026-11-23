"""Exact repeated-addition reconstruction of Euclid VII.16."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Trace:
    a: int
    b: int
    ab: int
    ba: int
    first_measure_count: int
    transferred_measure_count: int
    second_measure_count: int


def added_copies(count, summand):
    total = 0
    for _ in range(count):
        total += summand
    return total


def exact_measure(measure, whole, expected):
    count, remainder = divmod(whole, measure)
    if remainder or count != expected:
        raise ValueError("not the claimed exact measure count")
    return count


def commute(a, b):
    if any(type(t) is not int or t < 2 for t in (a,b)):
        raise ValueError("given numbers must be integers greater than one")
    ab = added_copies(a,b)  # Def.15, A times B.
    ba = added_copies(b,a)  # Def.15, B times A.
    first = exact_measure(b,ab,a)
    # VII.15 transfers the measurement: A measures AB as 1 measures B.
    transferred = exact_measure(a,ab,b)
    second = exact_measure(a,ba,b)
    if ab != ba:
        raise ArithmeticError("same measure and count must give the same total")
    return Trace(a,b,ab,ba,first,transferred,second)


def modern(a,b):
    """Separate extension: addition allows a unit and empty sums."""
    if any(type(t) is not int or t < 0 for t in (a,b)):
        raise ValueError("modern model requires nonnegative integers")
    return added_copies(a,b), added_copies(b,a)


if __name__ == "__main__":
    print(commute(3,4))
