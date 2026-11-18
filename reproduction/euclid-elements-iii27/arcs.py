"""Exact modern model for selected counterclockwise arcs (units: turns)."""
from dataclasses import dataclass
from fractions import Fraction as Q

@dataclass(frozen=True)
class Arc:
    radius: Q
    start: Q
    end: Q

    def __post_init__(self):
        if any(not isinstance(x, Q) for x in (self.radius, self.start, self.end)):
            raise TypeError("use exact Fraction inputs")
        if self.radius <= 0 or self.start % 1 == self.end % 1:
            raise ValueError("positive radius and distinct endpoints required")

    @property
    def sweep(self):
        return (self.end - self.start) % 1

    @property
    def length_over_tau(self):
        return self.radius * self.sweep

    @property
    def inscribed(self):
        return self.sweep / 2  # III.20 in modern selected-arc form

    def contains_interior(self, direction):
        return 0 < (direction - self.start) % 1 < self.sweep

def copy_smaller(smaller, larger):
    """Return the proper initial subarc representing the copied angle."""
    if smaller.radius != larger.radius or not smaller.sweep < larger.sweep:
        raise ValueError("requires equal radii and strictly ordered sweeps")
    copy = Arc(larger.radius, larger.start, larger.start + smaller.sweep)
    if not larger.contains_interior(copy.end):
        raise RuntimeError("not a proper initial subarc")
    return copy

def inspect(a, b):
    """Check premises and conclusions; optionally construct the proof witness."""
    if a.radius != b.radius:
        return {"premises": False, "reason": "radius"}
    if a.sweep == b.sweep:
        return {"premises": a.length_over_tau == b.length_over_tau,
                "central": True, "inscribed": a.inscribed == b.inscribed}
    small, large = sorted((a, b), key=lambda arc: arc.sweep)
    copy = copy_smaller(small, large)
    return {"premises": a.length_over_tau == b.length_over_tau,
            "central": False, "inscribed": a.inscribed == b.inscribed,
            "copy_matches_small": copy.length_over_tau == small.length_over_tau,
            "copy_shorter_than_large": copy.length_over_tau < large.length_over_tau}
