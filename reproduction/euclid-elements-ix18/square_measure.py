"""Exact certificate for the integer continuation in Euclid IX.18."""
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional


@dataclass(frozen=True)
class Measure:
    square: int
    quotient: int
    remainder: int
    witness: Optional[int]
    modern_unit: bool


def square_measure(a,b):
    """Modern positive-integer decision; modern_unit marks unit inputs only."""
    if any(type(x) is not int or x<1 for x in (a,b)):
        raise ValueError("expected positive integer terms")
    square=b*b
    quotient,remainder=divmod(square,a)
    return Measure(square,quotient,remainder,quotient if remainder==0 else None,1 in (a,b))


def extend_nonunit(a,b):
    """Restrict inputs to nonunits; a unit output is allowed as a modern boundary."""
    out=square_measure(a,b)
    if out.modern_unit or out.witness is None:
        raise ValueError("expected nonunit terms with A measuring B squared")
    if Fraction(a,b)!=Fraction(b,out.witness):
        raise ArithmeticError("proportional witness invariant failed")
    return out.witness
