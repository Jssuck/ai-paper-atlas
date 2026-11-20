"""Exact teaching model for Elements V.12; no floating point or dependencies."""
from fractions import Fraction
from itertools import product


def _sign(a, b):
    return (a > b) - (a < b)


def _positive_int(value):
    if type(value) is not int or value < 1:
        raise ValueError("positive integer required")


def _pairs(pairs):
    pairs = tuple(pairs)
    if not pairs:
        raise ValueError("nonempty family required")
    heads, tails = set(), set()
    rows = []
    for a, b, head_unit, tail_unit in pairs:
        if head_unit != tail_unit:
            raise ValueError("each ratio must use a common unit")
        heads.add(head_unit)
        tails.add(tail_unit)
        if type(a) not in (int, Fraction) or type(b) not in (int, Fraction):
            raise TypeError("use exact int or Fraction inputs")
        if min(a, b) <= 0:
            raise ValueError("positive magnitudes required")
        rows.append((Fraction(a), Fraction(b)))
    if len(heads) != 1 or len(tails) != 1:
        raise ValueError("summands must use common units")
    return tuple(rows)


def _probe(rows, m, n):
    a_sum, b_sum = map(sum, zip(*rows))
    return tuple(_sign(m*a, n*b) for a, b in rows), _sign(m*a_sum, n*b_sum)


def probe_sum(pairs, m, n):
    """Component signs and aggregate sign for one shared probe."""
    _positive_int(m)
    _positive_int(n)
    return _probe(_pairs(pairs), m, n)


def exact_sum(pairs):
    """Component ratios, aggregate ratio, and whether all components match."""
    rows = _pairs(pairs)
    first_a, first_b = rows[0]
    a_sum, b_sum = map(sum, zip(*rows))
    common = all(a*first_b == b*first_a for a, b in rows)
    return tuple(a/b for a, b in rows), a_sum/b_sum, common


def bounded_component_mismatch(pairs, limit):
    """First (m,n,component signs,aggregate sign), or None in this window."""
    _positive_int(limit)
    rows = _pairs(pairs)
    for m, n in product(range(1, limit+1), repeat=2):
        signs, aggregate = _probe(rows, m, n)
        if len(set(signs)) != 1:
            return m, n, signs, aggregate
    return None


def same_unit(*pairs):
    return tuple((a, b, "length", "length") for a, b in pairs)


COMMON = same_unit((2, 3), (4, 6), (6, 9))
MIXED = same_unit((1, 2), (3, 3), (6, 5))
CLOSE = same_unit((101, 100), (102, 100), (103, 100))


def main():
    components, aggregate, common = exact_sum(COMMON)
    print("common:", tuple(map(str, components)), str(aggregate), common)
    for m, n in ((1, 1), (3, 2), (2, 1)):
        print("probe:", (m, n), probe_sum(COMMON, m, n))
    components, aggregate, common = exact_sum(MIXED)
    print("unequal:", tuple(map(str, components)), str(aggregate), common)
    print("unweighted mean:", sum(components)/len(components))
    print("masked at (1, 1):", probe_sum(MIXED, 1, 1))
    for limit in (20, 40):
        print("first mismatch:", limit, bounded_component_mismatch(CLOSE, limit))


if __name__ == "__main__":
    main()
