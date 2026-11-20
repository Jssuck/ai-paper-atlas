"""Euclid V.11: compose exact or probe-local equality of ratio comparisons."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Ratio:
    first: Fraction
    second: Fraction
    kind: str = "length"

    def __post_init__(self):
        if not isinstance(self.kind, str) or not self.kind:
            raise ValueError("expected one nonempty kind shared by both terms")
        for field in ("first", "second"):
            value = getattr(self, field)
            if type(value) not in (int, Fraction) or value <= 0:
                raise ValueError("expected positive exact quantities")
            object.__setattr__(self, field, Fraction(value))

    @classmethod
    def from_typed(cls, first, first_kind, second, second_kind):
        if first_kind != second_kind:
            raise ValueError("ratio terms must have the same kind")
        return cls(first, second, first_kind)

    def sign(self, m, n):
        _integer(m)
        _integer(n)
        delta = m*self.first - n*self.second
        return (delta > 0) - (delta < 0)


def _integer(n):
    if type(n) is not int or n < 1:
        raise ValueError("expected a positive integer")


def same_exact(left, right):
    """Separate positive rational oracle, not the historical proof."""
    return left.first*right.second == right.first*left.second


def exact_chain(left, middle, right):
    """Return whether both premises are valid in the rational model."""
    return same_exact(left, middle) and same_exact(middle, right)


def probe_chain(left, middle, right, m, n):
    """Three signs at one common pair of multipliers."""
    return tuple(x.sign(m,n) for x in (left,middle,right))


def bounded_mismatch(left, middle, right, bound):
    """Return first violated premise probe, or None (not exact equality)."""
    _integer(bound)
    for m in range(1,bound+1):
        for n in range(1,bound+1):
            signs = probe_chain(left,middle,right,m,n)
            if len(set(signs)) != 1:
                return (m,n,signs)
    return None


if __name__ == "__main__":
    equal = Ratio(2,3), Ratio(4,6,"area"), Ratio(6,9,"mass")
    for m,n in ((1,1),(3,2),(2,1)):
        print((m,n),probe_chain(*equal,m,n))
    near = Ratio(101,100), Ratio(102,100), Ratio(103,100)
    print("window 20:", bounded_mismatch(*near,20))
    print("window 40:", bounded_mismatch(*near,40))
    print("exact premises:", exact_chain(*near))
