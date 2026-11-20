"""Euclid V.18: two distinct replays in a typed positive-rational model."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Magnitude:
    value: Fraction
    kind: str = "length"

    def __post_init__(self):
        if type(self.value) not in (int, Fraction):
            raise TypeError("use integers or exact Fractions")
        if self.value <= 0:
            raise ValueError("expected a positive magnitude")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("expected a nonempty kind")
        object.__setattr__(self, "value", Fraction(self.value))

    def __add__(self, other):
        same_kind(self, other)
        return Magnitude(self.value + other.value, self.kind)

    def __sub__(self, other):
        same_kind(self, other)
        return Magnitude(self.value - other.value, self.kind)

    def scale(self, k):
        if type(k) is not int or k <= 0:
            raise ValueError("expected a positive integer probe")
        return Magnitude(self.value * k, self.kind)


def same_kind(a, b):
    if a.kind != b.kind:
        raise ValueError("magnitude kinds differ within a pair")


def sgn(a, b):
    return (a > b) - (a < b)


def compare(a, b):
    same_kind(a, b)
    return sgn(a.value, b.value)


def ratio(a, b):
    same_kind(a, b)
    return a.value / b.value


@dataclass(frozen=True)
class CandidateTrace:
    total: Magnitude
    candidate: Magnitude
    remainder: Magnitude
    denominator_sign: int
    remainder_sign: int
    actual_separated_ratio: Fraction
    separated_hypothesis: bool


def candidate_trace(a, b, c, d):
    """Inspect the fourth proportional; both disagreements are negative inputs.

    Fraction division supplies a witness in this model, not in arbitrary types
    of magnitudes. Cross-group comparisons only compare dimensionless ratios.
    """
    whole_left, whole_right = a + b, c + d
    joint = ratio(whole_left, b)
    g = Magnitude(whole_right.value / joint, whole_right.kind)
    if compare(g, whole_right) >= 0 or ratio(whole_right, g) != joint:
        raise ArithmeticError("invalid fourth proportional")
    rest = whole_right - g
    sep = ratio(a, b)
    if ratio(rest, g) != sep:
        raise ArithmeticError("separation replay mismatch")
    denom_sign, rest_sign = compare(g, d), compare(rest, c)
    if denom_sign != -rest_sign:
        raise ArithmeticError("complement failed to reverse order")
    right_sep = ratio(c, d)
    premise = sep == right_sep
    # With the premise, V.14 would demand rest_sign == denom_sign;
    # only the equality branch is compatible with both sign conditions.
    if premise != (denom_sign == 0):
        raise ArithmeticError("contrast between premise and branch failed")
    return CandidateTrace(whole_right, g, rest, denom_sign, rest_sign,
                          right_sep, premise)


def replay(a, b, c, d):
    trace = candidate_trace(a, b, c, d)
    if not trace.separated_hypothesis:
        raise ValueError("separated-ratio premise fails")
    return trace


@dataclass(frozen=True)
class ProbeTrace:
    joint_signs: tuple
    separated_signs: tuple | None


def direct_probe(a, b, c, d, m, k):
    """Independent modern probe argument, with no fourth proportional."""
    if ratio(a, b) != ratio(c, d):
        raise ValueError("separated-ratio premise fails")
    pairs = ((a, b), (c, d))
    signs = tuple(compare((x + y).scale(m), y.scale(k)) for x, y in pairs)
    if k <= m:
        # Do not construct a zero or negative multiple.
        if signs != (1, 1):
            raise ArithmeticError("positive remainder must dominate")
        return ProbeTrace(signs, None)
    separated = tuple(compare(x.scale(m), y.scale(k - m)) for x, y in pairs)
    if separated[0] != separated[1] or signs != separated:
        raise ArithmeticError("translating the comparison changed the sign")
    return ProbeTrace(signs, separated)


def demo():
    a, b = map(Magnitude, (2, 3))
    for c, d in ((4, 6), (3, 7), (5, 5)):
        c, d = Magnitude(c, "area"), Magnitude(d, "area")
        t = candidate_trace(a, b, c, d)
        print(f"c={c.value} d={d.value}: candidate={t.candidate.value} "
              f"remainder={t.remainder.value} signs(g-d,rest-c)="
              f"{(t.denominator_sign,t.remainder_sign)} premise={t.separated_hypothesis}")
    c, d = Magnitude(4, "area"), Magnitude(6, "area")
    for m, k in ((3, 2), (3, 3), (3, 4), (3, 5), (3, 6)):
        print(f"m={m} k={k}: {direct_probe(a,b,c,d,m,k)}")


if __name__ == "__main__":
    demo()
