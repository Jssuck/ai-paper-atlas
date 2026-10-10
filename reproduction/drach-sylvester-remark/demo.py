"""Modern exact-arithmetic teaching examples for the Drach/Sylvester remark.

This is an illustration of elementary algebra, not a historical experiment.
Only Python's standard library is used; floats are deliberately rejected.
"""

from dataclasses import dataclass
from fractions import Fraction
import json


def rational(value):
    """Accept an exact integer, rational string, or Fraction, never a float."""
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError("Use int, rational string, or Fraction; not float.")
    return Fraction(value)


@dataclass(frozen=True)
class Pair:
    """Represent r + s*i by the exact rational pair (r, s)."""

    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, "real", rational(self.real))
        object.__setattr__(self, "imag", rational(self.imag))

    def __add__(self, other):
        return Pair(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Pair(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Pair(self.real * other.real - self.imag * other.imag,
                    self.real * other.imag + self.imag * other.real)

    @property
    def is_real(self):
        return self.imag == 0

    def as_json(self):
        return {"real": str(self.real), "imag": str(self.imag)}


def remark(a, b, f, c):
    """a + b*i + f - c*i, with a,b,f,c restricted to real rationals."""
    return Pair(a, b) + Pair(f, -rational(c))


def unrestricted_remark(a, b, f, c):
    """Allow complex a/f, retaining real-rational b/c for the caveat."""
    return a + Pair(0, b) + f - Pair(0, c)


def build_results():
    differences = [
        {"left": str(x), "right": str(y), "difference": str(rational(x) - rational(y))}
        for x, y in [(5, 3), (3, 5), (3, 3)]
    ]
    cases = []
    for b, c in [(5, 3), (3, 5), (3, 3)]:
        value = remark(2, b, 3, c)
        cases.append({"a": "2", "b": str(b), "f": "3", "c": str(c),
                      "value": value.as_json(), "is_real": value.is_real,
                      "b_equals_c": b == c})

    decompositions = []
    for a, b, f, c in [(2, 5, 3, 3), (1, 9, 4, 7)]:
        decompositions.append({"a": str(a), "b": str(b), "f": str(f), "c": str(c),
                               "value": remark(a, b, f, c).as_json()})

    # Both summands are nonreal; their sum is real.
    left, right = Pair(2, 3), Pair(3, -3)
    u, v = Pair(1, 1), Pair(1, -1)
    roots = [Fraction(1), Fraction(-4)]
    caveats = []
    for a, b, f, c in [(Pair(0, 1), 1, Pair(), 1),
                       (Pair(0, -1), 2, Pair(), 1)]:
        value = unrestricted_remark(a, b, f, c)
        caveats.append({"a": a.as_json(), "b": str(b), "f": f.as_json(),
                        "c": str(c), "value": value.as_json(),
                        "b_equals_c": b == c, "is_real": value.is_real})

    return {
        "scope": "Modern teaching examples; not an experiment reported in 1852.",
        "arithmetic": "Exact rational complex pairs; JSON rationals are strings.",
        "real_coefficient_identity": "a + b*i + f - c*i = (a+f) + (b-c)*i",
        "signed_real_differences": differences,
        "imaginary_difference_cases": cases,
        "nonunique_decompositions": decompositions,
        "nonreal_intermediates_real_result": {
            "sum_operands": [left.as_json(), right.as_json()],
            "sum": (left + right).as_json(),
            "product_operands": [u.as_json(), v.as_json()],
            "product": (u * v).as_json(),
        },
        "positive_length_constraint": {
            "equation": "x^2 + 3*x = 4",
            "factorization": "(x-1)*(x+4) = 0",
            "real_roots": [str(x) for x in roots],
            "residuals": [str(x*x + 3*x - 4) for x in roots],
            "admissibility_assumption": "x is an ordinary length, so x > 0",
            "admissible_roots": [str(x) for x in roots if x > 0],
            "excluded_real_roots": [str(x) for x in roots if x <= 0],
            "interpretation": "A real algebraic root may violate a geometric domain constraint.",
        },
        "complex_a_f_caveat": caveats,
    }


if __name__ == "__main__":
    print(json.dumps(build_results(), ensure_ascii=False, indent=2))
