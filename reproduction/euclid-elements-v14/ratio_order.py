"""Euclid V.14 in a positive rational teaching model, not a general proof."""

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Magnitude:
    value: int | Fraction
    kind: str = "length"

    def __post_init__(self):
        if type(self.value) not in (int, Fraction) or self.value <= 0:
            raise ValueError("magnitude requires an exact positive int or Fraction")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("kind requires a nonempty label")


def sign(x, y):
    return (x > y) - (x < y)


def same_kind(*magnitudes):
    if not all(isinstance(x, Magnitude) for x in magnitudes):
        raise ValueError("expected Magnitude")
    if len({x.kind for x in magnitudes}) != 1:
        raise ValueError("these comparisons need one common kind and unit")


def proportion(a, b, c, d):
    """Exact quotient equality; allows separately same-kind pairs."""
    same_kind(a, b)
    same_kind(c, d)
    return a.value * d.value == b.value * c.value


def local_probe(a, b, m, n):
    same_kind(a, b)
    if type(m) is not int or type(n) is not int or min(m, n) < 1:
        raise ValueError("probe multipliers must be positive integers")
    return sign(m * a.value, n * b.value)


def bounded_difference(a, b, c, d, cap):
    """Find a signature discrepancy in a square window, or return None."""
    same_kind(a, b)
    same_kind(c, d)
    if type(cap) is not int or cap < 1:
        raise ValueError("cap must be a positive integer")
    for m in range(1, cap + 1):
        for n in range(1, cap + 1):
            lhs, rhs = local_probe(a, b, m, n), local_probe(c, d, m, n)
            if lhs != rhs:
                return (m, n), (lhs, rhs)
    return None


def strict_trace(a, b, c, d):
    """A>C oriented branch, with one probe aligned through V.8, V.13, V.10."""
    same_kind(a, b, c, d)
    if not proportion(a, b, c, d) or a.value <= c.value:
        raise ValueError("strict oriented branch requires proportion and A>C")
    threshold = Fraction(c.value) / Fraction(b.value)
    m, n = threshold.denominator, threshold.numerator
    signs = (local_probe(a, b, m, n), local_probe(c, b, m, n),
             local_probe(c, d, m, n))
    if signs != (1, 0, 1) or not n * d.value < m * c.value <= n * b.value:
        raise ArithmeticError("the witness did not transport")
    return (m, n), signs, (n * d.value, m * c.value, n * b.value)


def order_transport(a, b, c, d):
    """Return signs (A vs C, B vs D) and oriented strict trace if needed."""
    same_kind(a, b, c, d)
    if not proportion(a, b, c, d):
        raise ValueError("V.14 requires exact proportion")
    first = sign(a.value, c.value)
    if first == 0:
        # From A=C>0 and AD=BC, cancel A to obtain D=B.
        second = sign(b.value, d.value)
        if second != 0:
            raise ArithmeticError("positive cancellation failed")
        return (0, 0), None
    oriented = (a, b, c, d) if first == 1 else (c, d, a, b)
    return (first, first), strict_trace(*oriented)


def mags(*values):
    return tuple(Magnitude(value) for value in values)


def main():
    for values in ((9, 6, 6, 4), (6, 4, 9, 6), (6, 4, 6, 4)):
        print("order:", values, order_transport(*mags(*values)))
    near = mags(51, 50, 52, 50)
    print("near exact proportion:", proportion(*near))
    print("near discrepancy cap 20:", bounded_difference(*near, 20))
    print("near discrepancy cap 26:", bounded_difference(*near, 26))
    print("near raw order:", (sign(51, 52), sign(50, 50)))


if __name__ == "__main__":
    main()
