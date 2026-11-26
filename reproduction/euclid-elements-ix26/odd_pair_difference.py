"""Equal-halves certificate for Euclid IX.26."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Witness:
    even_residuals: tuple
    even_halves: tuple
    half: int
    difference: int


def odd_pair_difference(a,b):
    """Given odd integers A > B >= 3, remove one from both terms."""
    if any(type(x) is not int for x in (a,b)) or not a>b>=3 or a%2!=1 or b%2!=1:
        raise ValueError("expected odd integers A > B >= 3")
    left,right=a-1,b-1
    h1,h2=left//2,right//2
    half=h1-h2
    difference=left-right
    if difference!=a-b or difference!=half+half:
        raise ArithmeticError("even-difference certificate failed")
    return Witness((left,right),(h1,h2),half,difference)
