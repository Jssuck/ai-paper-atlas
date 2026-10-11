"""Exact toy response y = gain * coefficient * input; NOT a historical law."""
from dataclasses import dataclass
from fractions import Fraction


def exact(value) -> Fraction:
    if type(value) is int or isinstance(value, Fraction):
        return Fraction(value)
    raise TypeError("use int or Fraction, never float; e.g. Fraction(1, 10)")


def positive(value) -> Fraction:
    value = exact(value)
    if value <= 0:
        raise ValueError("gain and coefficient must be strictly positive")
    return value


def response(inputs, coefficient, gain=1) -> tuple[Fraction, ...]:
    coefficient, gain = positive(coefficient), positive(gain)
    return tuple(gain * coefficient * exact(u) for u in inputs)


@dataclass(frozen=True)
class ProductInference:
    status: str  # identified / uninformative / inconsistent
    product: Fraction | None


def infer_product(inputs, outputs) -> ProductInference:
    inputs, outputs = tuple(map(exact, inputs)), tuple(map(exact, outputs))
    if not inputs or len(inputs) != len(outputs):
        raise ValueError("need equally sized, nonempty input and output sequences")
    ratios = set()
    for u, y in zip(inputs, outputs):
        if u == 0:
            if y != 0:
                return ProductInference("inconsistent", None)
        else:
            ratios.add(y / u)
    if not ratios:
        return ProductInference("uninformative", None)
    if len(ratios) != 1 or next(iter(ratios)) <= 0:
        return ProductInference("inconsistent", None)
    return ProductInference("identified", next(iter(ratios)))


def calibrated_coefficient(inputs, outputs, known_gain) -> Fraction:
    gain = positive(known_gain)
    result = infer_product(inputs, outputs)
    if result.status != "identified":
        raise ValueError("data do not identify a positive response product")
    return result.product / gain


def equivalent_parameters(coefficient, gain, scale) -> tuple[Fraction, Fraction]:
    """Return (k*c, g/c): every input has the same output."""
    coefficient, gain, scale = map(positive, (coefficient, gain, scale))
    return coefficient * scale, gain / scale


def relative_coefficient(inputs, outputs_a, outputs_b) -> Fraction:
    """Identify k_a/k_b ONLY under the stated common-gain assumption."""
    inputs = tuple(inputs)
    a, b = infer_product(inputs, outputs_a), infer_product(inputs, outputs_b)
    if a.status != "identified" or b.status != "identified":
        raise ValueError("both response products must be identified")
    return a.product / b.product
