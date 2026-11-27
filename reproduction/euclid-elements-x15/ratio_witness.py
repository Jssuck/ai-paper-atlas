"""Exact common-measure witnesses for part, remainder, and whole (X.15)."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Witness:
    unit: Fraction
    counts: tuple[int, int, int]  # part, remainder, whole

    @property
    def lengths(self):
        return tuple(self.unit*n for n in self.counts)


def _validate(unit, x, y):
    if type(unit) not in (int, Fraction) or unit <= 0:
        raise ValueError("unit must be a positive exact rational number")
    if any(type(n) is not int or n <= 0 for n in (x,y)):
        raise ValueError("counts must be positive integers")
    return Fraction(unit)


def from_parts(unit, part, remainder):
    """A measure of the two parts also measures their whole."""
    return Witness(_validate(unit,part,remainder),(part,remainder,part+remainder))


def from_whole(unit, whole, part):
    """A measure of the whole and a proper part also measures the remainder."""
    unit = _validate(unit,whole,part)
    if whole <= part:
        raise ValueError("part must be strictly smaller than the whole")
    return Witness(unit,(part,whole-part,whole))
