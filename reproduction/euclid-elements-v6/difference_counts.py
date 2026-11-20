"""Exact teaching reconstruction of Euclid V.6."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Quantity:
    value: Fraction
    kind: str

    def __post_init__(self):
        if type(self.value) is not int and not isinstance(self.value, Fraction):
            raise TypeError("use an exact Fraction or integer")
        object.__setattr__(self, "value", Fraction(self.value))
        if self.value <= 0 or not isinstance(self.kind, str) or not self.kind:
            raise ValueError("positive coordinate and nonempty kind required")


@dataclass(frozen=True)
class Certificate:
    whole_count: int
    cut_count: int
    remainder_count: int
    branch: str
    remainders: tuple
    auxiliaries: tuple
    rebuilt_wholes: tuple


def _strict_count(value, base):
    factor = value / base
    if factor.denominator != 1 or factor < 2:
        raise ValueError("expected strict integer multiple")
    return factor.numerator


def _repeat(base, count):
    return sum((base for _ in range(count)), Fraction(0))


def reconstruct(base, whole, cut):
    """Check matching counts for whole and removed pairs before cancellation."""
    if any(len(pair) != 2 for pair in (base, whole, cut)):
        raise ValueError("each pair needs two columns")
    if any(
        not (b.kind == w.kind == c.kind)
        for b, w, c in zip(base, whole, cut)
    ):
        raise ValueError("base, whole and cut must have same kind within column")
    whole_counts = tuple(_strict_count(w.value, b.value) for b, w in zip(base, whole))
    cut_counts = tuple(_strict_count(c.value, b.value) for b, c in zip(base, cut))
    if whole_counts[0] != whole_counts[1] or cut_counts[0] != cut_counts[1]:
        raise ValueError("counts differ across matched columns")
    m, n = whole_counts[0], cut_counts[0]
    if n >= m:
        raise ValueError("cut must leave a positive remainder")
    k = m - n
    aux = tuple(_repeat(b.value, k) for b in base)
    rebuilt = tuple(c.value + a for c, a in zip(cut, aux))
    remainders = tuple(w.value - c.value for w, c in zip(whole, cut))
    if rebuilt != tuple(w.value for w in whole) or remainders != aux:
        raise ArithmeticError("construction and cancellation disagree")
    tagged = lambda values: tuple(Quantity(v, b.kind) for v, b in zip(values, base))
    return Certificate(m, n, k, "unit" if k == 1 else "strict", tagged(remainders),
                       tagged(aux), tagged(rebuilt))


def make_inputs(a, b, m, n):
    """Build deterministic examples, with different kinds across columns."""
    return ((Quantity(a, "length"), Quantity(b, "area")),
            (Quantity(m*a, "length"), Quantity(m*b, "area")),
            (Quantity(n*a, "length"), Quantity(n*b, "area")))


def finite_grid():
    unit = strict = rejects = 0
    choices = (Fraction(1, 2), Fraction(5, 3), Fraction(7, 4))
    for a in choices:
        for b in choices:
            for m in range(3, 9):
                for n in range(2, m):
                    base, whole, cut = make_inputs(a, b, m, n)
                    result = reconstruct(base, whole, cut)
                    expected = (a*(m-n), b*(m-n))
                    if tuple(x.value for x in result.remainders) != expected:
                        raise ArithmeticError("multiplication baseline disagrees")
                    if result.branch == "unit":
                        unit += 1
                    else:
                        strict += 1
                    # Add one copy to both the right whole and right cut.
                    wrong_whole = (whole[0], Quantity(whole[1].value+b, "area"))
                    wrong_cut = (cut[0], Quantity(cut[1].value+b, "area"))
                    if wrong_whole[1].value-wrong_cut[1].value != expected[1]:
                        raise ArithmeticError("control must preserve remainder")
                    try:
                        reconstruct(base, wrong_whole, wrong_cut)
                    except ValueError as exc:
                        if str(exc) != "counts differ across matched columns":
                            raise
                        rejects += 1
                    else:
                        raise ArithmeticError("accepted matching output with wrong input")
    return unit, strict, rejects


if __name__ == "__main__":
    for m, n in ((4, 3), (7, 3)):
        cert = reconstruct(*make_inputs(Fraction(2, 3), Fraction(5, 4), m, n))
        print(cert.branch, m, n, cert.remainder_count,
              *(q.value for q in cert.remainders))
    print("grid (unit, strict, rejected):", finite_grid())
