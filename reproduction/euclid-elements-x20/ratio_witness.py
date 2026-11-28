"""X.20: apply an exact rational area along a reference-relative base."""
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Witness:
    breadth_per_base: F
    breadth_squared: F
    counts: tuple[int,int]  # breadth, base
    measure_per_base: F


def apply_area(base_squared,area):
    """Use squared base and rectangle area, both relative to reference square."""
    if any(type(x) not in (int,F) or x<=0 for x in (base_squared,area)):
        raise ValueError("expected positive exact rational inputs")
    a,r = F(base_squared),F(area)
    k = r/a
    return Witness(k,r*r/a,(k.numerator,k.denominator),F(1,k.denominator))
