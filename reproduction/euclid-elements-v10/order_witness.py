"""Euclid V.10: verify an oriented V.Def.7 witness in a rational model."""
from dataclasses import dataclass
from fractions import Fraction

SHARED_DENOMINATOR = "shared-denominator"
SHARED_NUMERATOR = "shared-numerator"


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


def _int(n):
    if type(n) is not int or n < 1:
        raise ValueError("expected a positive integer")


def _validate(a,b,c,orientation):
    if len({a.kind,b.kind,c.kind}) != 1:
        raise ValueError("a shared term requires three homogeneous magnitudes")
    if orientation not in (SHARED_DENOMINATOR, SHARED_NUMERATOR):
        raise ValueError("unknown orientation")


def scaled_terms(a,b,c,m,n,orientation):
    """A:C ≻ B:C, or C:B ≻ C:A; m scales antecedents, n consequents."""
    _validate(a,b,c,orientation)
    _int(m)
    _int(n)
    av,bv,cv = a.value,b.value,c.value
    if orientation == SHARED_DENOMINATOR:
        return (m*av,n*cv), (m*bv,n*cv)
    return (m*cv,n*bv), (m*cv,n*av)


@dataclass(frozen=True)
class Certificate:
    orientation: str
    m: int
    n: int
    first: tuple
    second: tuple
    conclusion: str = "A>B"


def infer_order(a,b,c,m,n,orientation):
    """Infer A>B (equivalently B<A) only if both supplied comparisons pass."""
    first, second = scaled_terms(a,b,c,m,n,orientation)
    if first[0] > first[1] and second[0] <= second[1]:
        return Certificate(orientation,m,n,first,second)
    return None


def bounded_search(a,b,c,bound,orientation):
    """Return a verified certificate or None; None is not a comparison result."""
    _validate(a,b,c,orientation)
    _int(bound)
    for m in range(1,bound+1):
        for n in range(1,bound+1):
            cert = infer_order(a,b,c,m,n,orientation)
            if cert is not None:
                return cert
    return None


if __name__ == "__main__":
    a,b,c = map(Magnitude,(3,2,2))
    for orientation,m,n in ((SHARED_DENOMINATOR,1,1),
                             (SHARED_NUMERATOR,1,1),(SHARED_NUMERATOR,3,2)):
        print(orientation, f"({m},{n}):", infer_order(a,b,c,m,n,orientation))
    a,b,c = map(Magnitude,(102,101,100))
    for orientation in (SHARED_DENOMINATOR,SHARED_NUMERATOR):
        print(orientation,"window 20:",bounded_search(a,b,c,20,orientation))
        print(orientation,"window 52:",bounded_search(a,b,c,52,orientation))
