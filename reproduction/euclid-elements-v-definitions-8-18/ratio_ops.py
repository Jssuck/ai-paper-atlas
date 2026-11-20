"""Exact rational teaching model for Euclid V, Definitions 8–18."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product


@dataclass(frozen=True)
class Amount:
    value: F
    kind: str

    def __post_init__(self):
        if type(self.value) not in (int, F) or self.value <= 0:
            raise ValueError("amount must be a positive integer or Fraction")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("kind must be a nonempty string")
        object.__setattr__(self, "value", F(self.value))


@dataclass(frozen=True)
class Ratio:
    leading: Amount
    following: Amount

    def __post_init__(self):
        if self.leading.kind != self.following.kind:
            raise ValueError("ratio terms must have the same kind")

    @property
    def value(self):
        return self.leading.value / self.following.value

    def proportional_to(self, other):
        return self.value == other.value


def link_ratios(terms):
    if len(terms) < 2:
        raise ValueError("at least two terms required")
    return tuple(Ratio(a, b) for a, b in zip(terms, terms[1:]))


def power_ratio(terms):
    """Defs. 8–10: a continuous three- or four-term proportion."""
    if len(terms) not in (3, 4):
        raise ValueError("this example implements duplicate and triplicate")
    links = link_ratios(terms)
    if any(not links[0].proportional_to(r) for r in links[1:]):
        raise ValueError("consecutive ratios must agree")
    return Ratio(terms[0], terms[-1])


def corresponding(left, right):
    """Def. 11: ordered pairs of leading and following terms."""
    return ((left.leading, right.leading), (left.following, right.following))


def alternate(left, right):
    """Def. 12 names the two cross-pairs. Require proper ratio domains."""
    return tuple(Ratio(a, b) for a, b in corresponding(left, right))


def transform(r, operation):
    """Defs. 13–16. A difference must be a positive amount."""
    a, b = r.leading, r.following
    if operation == "inverse":
        return Ratio(b, a)
    if operation == "composition":
        return Ratio(Amount(a.value + b.value, a.kind), b)
    if operation not in ("separation", "conversion"):
        raise ValueError("unknown operation")
    excess = Amount(a.value - b.value, a.kind)
    if operation == "separation":
        return Ratio(excess, b)
    return Ratio(a, excess)


def endpoint_ratios(left, right, *, perturbed=False):
    """Defs. 17–18: match the appropriate links before taking endpoints.

    For Def. 18 the right input follows the V.23 endpoint order D,E,F:
    A:B matches E:F and B:C matches D:E.
    """
    if len(left) != len(right):
        raise ValueError("chains must have equal lengths")
    if perturbed and len(left) != 3:
        raise ValueError("perturbed proportions have three terms per chain")
    lhs, rhs = link_ratios(left), link_ratios(right)
    matching_rhs = rhs[::-1] if perturbed else rhs
    if any(not a.proportional_to(b) for a, b in zip(lhs, matching_rhs)):
        raise ValueError("link ratios do not match in the specified order")
    return Ratio(left[0], left[-1]), Ratio(right[0], right[-1])


def terms(*values, kind="length"):
    return tuple(Amount(v, kind) for v in values)


def grid():
    """Aligned and perturbed chains with independent exact endpoint checks."""
    matches = 0
    wrong_order = 0
    for p, q, scale, extra in product(
        (F(1, 2), F(1), F(2), F(3, 2)),
        (F(1, 3), F(1), F(2), F(5, 2)),
        (1, 3),
        (2, 5),
    ):
        lhs = terms(scale * p * q, scale * q, scale)
        aligned = terms(extra * p * q, extra * q, extra, kind="area")
        swapped = terms(extra * p * q, extra * p, extra, kind="area")
        for rhs, perturbed in ((aligned, False), (swapped, True)):
            a, b = endpoint_ratios(lhs, rhs, perturbed=perturbed)
            if a.leading.value * b.following.value != b.leading.value * a.following.value:
                raise ArithmeticError("endpoint cross-products disagree")
            matches += 1
        if p != q:
            try:
                endpoint_ratios(lhs, swapped)
            except ValueError:
                wrong_order += 1
            else:
                raise ArithmeticError("wrong matching accepted")
    return matches, wrong_order


if __name__ == "__main__":
    starts = terms(27, 18, 12, 8)
    base = Ratio(*starts[:2]).value
    print("base / duplicate / triplicate / doubled base:", base,
          power_ratio(starts[:3]).value, power_ratio(starts).value, 2 * base)
    sample = Ratio(*terms(3, 2))
    print("inverse / composition / separation / conversion:",
          *(transform(sample, name).value for name in
            ("inverse", "composition", "separation", "conversion")))
    print("grid (valid joins, order rejections):", grid())
