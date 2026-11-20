"""Euclid V.9 as exact equimultiple probes on positive rational magnitudes."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __post_init__(self):
        if type(self.value) not in (int, Fraction) or self.value <= 0:
            raise ValueError("expected positive int or Fraction")
        if not isinstance(self.kind, str) or not self.kind:
            raise ValueError("expected nonempty kind")
        object.__setattr__(self, "value", Fraction(self.value))


def _values(a, b, c):
    if len({a.kind, b.kind, c.kind}) != 1:
        raise ValueError("shared reference requires three homogeneous magnitudes")
    return a.value, b.value, c.value


def _positive_int(n):
    if type(n) is not int or n < 1:
        raise ValueError("expected a positive integer")


def _sign(x):
    return (x > 0) - (x < 0)


def probe(a, b, c, m, n):
    """Return comparisons for (a:c,b:c) and (c:a,c:b) at swapped multipliers."""
    a, b, c = _values(a, b, c)
    _positive_int(m)
    _positive_int(n)
    forward = _sign(m*a - n*c), _sign(m*b - n*c)
    return forward, tuple(-x for x in forward)


@dataclass(frozen=True)
class Countercertificate:
    larger: str
    m: int
    n: int
    forward: tuple
    reverse: tuple


def distinguish(a, b, c):
    """Use the V.8 construction when unequal; None means direct input equality."""
    av, bv, cv = _values(a, b, c)
    if av == bv:
        return None
    hi, lo = max(av, bv), min(av, bv)
    gap = hi - lo
    m = cv // min(lo, gap) + 1
    n = (m * max(lo, gap)) // cv + 1
    fw, rev = probe(a, b, c, m, n)
    return Countercertificate("a" if av > bv else "b", m, n, fw, rev)


def bounded_mismatch(a, b, c, bound):
    """Return first mismatch in the window or None; not a ratio verdict."""
    _values(a, b, c)
    _positive_int(bound)
    for m in range(1, bound+1):
        for n in range(1, bound+1):
            fw, _ = probe(a, b, c, m, n)
            if fw[0] != fw[1]:
                return m, n
    return None


if __name__ == "__main__":
    a, b, c = map(Magnitude, (102, 101, 100))
    print("unequal, window 20:", bounded_mismatch(a, b, c, 20))
    print("V.8 countercertificate:", distinguish(a, b, c))
    print("swapped a/b:", distinguish(b, a, c))
    print("equal, equality probe:", probe(c, c, c, 1, 1))
