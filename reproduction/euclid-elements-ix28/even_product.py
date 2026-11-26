"""Equal-halves certificate for Euclid IX.28."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    copies: int
    term: int
    half_total: int
    total: int


def odd_times_even(a,b):
    """Take even B exactly odd A times, in the historical nonunit input model."""
    if any(type(n) is not int for n in (a,b)) or a<3 or b<2 or a%2!=1 or b%2:
        raise ValueError("expected an odd count A >= 3 and even term B >= 2")
    half_total=total=0
    half=b//2
    for _ in range(a):
        half_total+=half
        total+=b
        if half_total+half_total!=total:
            raise ArithmeticError("running half-sum invariant failed")
    return Witness(a,b,half_total,total)
