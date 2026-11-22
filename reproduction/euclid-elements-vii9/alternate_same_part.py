"""Exact teaching reconstruction of Euclid VII.9, on positive integers."""
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class PairedRows:
    n: int
    kind: str
    m: int
    k: int
    local_measure: int
    pooled_measure: int


def paired_rows(a: int, bc: int, d: int, ef: int) -> PairedRows:
    """Check the historical direction A<D and the common proper unit part.

    Encode the n identical aligned rows (A,D) without allocating a list.
    The symbols m,k are the exact counts of a common measure in one row.
    """
    if any(type(x) is not int or x <= 1 for x in (a, bc, d, ef)):
        raise ValueError("given numbers must be integers greater than one")
    if a >= d:
        raise ValueError("the historical part/parts comparison requires A<D")
    n, r_a = divmod(bc, a)
    n_d, r_d = divmod(ef, d)
    if r_a or r_d or n < 2 or n_d != n:
        raise ValueError("both smaller numbers must be the same proper unit part")
    g = gcd(a, d)
    m, k = a // g, d // g
    # Each row has m and k copies of g. Merge the i-th copy across all n rows:
    # the pooled quantities consist of m and k copies of the merged measure.
    merged = n * g
    if (m * merged, k * merged) != (bc, ef) or gcd(bc, ef) != merged:
        raise ArithmeticError("paired-row pooling failed")
    return PairedRows(n, "part" if m == 1 else "parts", m, k, g, merged)


def demo():
    for values in ((4, 12, 12, 36), (6, 18, 10, 30)):
        print(values, paired_rows(*values))


if __name__ == "__main__":
    demo()
