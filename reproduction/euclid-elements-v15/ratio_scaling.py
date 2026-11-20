"""Exact rational teaching model for Euclid V.15; no dependencies."""
from fractions import Fraction


def positive(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("magnitude must be int or Fraction")
    if value <= 0:
        raise ValueError("magnitude must be positive")
    return Fraction(value)


def multiplier(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("multiplier must be an integer")
    if value <= 0:
        raise ValueError("multiplier must be positive")
    return value


def signature(a, b, m, n):
    """The V.Def.5 comparison at one independent multiplier pair."""
    left, right = multiplier(m) * positive(a), multiplier(n) * positive(b)
    return (left > right) - (left < right)


def partition_trace(c, f, k, m, n):
    """Report the ordered equal parts and the independent probe on their totals."""
    c, f, k = positive(c), positive(f), multiplier(k)
    parts = ((c, f),) * k
    total_c = sum((a for a, _ in parts), Fraction(0))
    total_f = sum((b for _, b in parts), Fraction(0))
    return {
        "parts": parts,
        "part_ratio": c / f,
        "total": (total_c, total_f),
        "total_ratio": total_c / total_f,
        "part_signs": tuple(signature(a, b, m, n) for a, b in parts),
        "total_sign": signature(total_c, total_f, m, n),
    }


def demo():
    for m, n in ((1, 1), (3, 2), (2, 1)):
        trace = partition_trace(2, 3, 4, m, n)
        print(f"probe={(m,n)} parts={trace['part_signs']} total_sign={trace['total_sign']}")
    print(f"uniform ratio: {trace['part_ratio']} -> {trace['total_ratio']}")
    print(f"unequal scales: {Fraction(2,3)} -> {Fraction(4,9)}; "
          f"probe (3,2): {signature(2,3,3,2)} -> {signature(4,9,3,2)}")


if __name__ == "__main__":
    demo()
