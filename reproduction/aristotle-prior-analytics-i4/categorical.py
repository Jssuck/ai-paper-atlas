"""Modern, finite-support teaching model for Prior Analytics I.4.

This is a reconstruction, not an algorithm attributed to Aristotle.
A form XYZ means X(M,P), Y(S,M) entails Z(S,P).
Membership types use P=4, M=2, S=1; the universe is always nonempty.
"""
from dataclasses import dataclass
from itertools import combinations, product

KINDS = "AEIO"
MODES = ("empty-allowed", "all-nonempty")
TERM_BITS = {"P": 4, "M": 2, "S": 1}
ORIGINAL_ROUTES = {"AA": "A", "EA": "E", "AI": "I", "EI": "O"}


def _choice(value, choices, label):
    if type(value) is not str:
        raise TypeError(f"{label} must be a string")
    if value not in choices:
        raise ValueError(f"invalid {label}: {value!r}")


def _kind(kind):
    # Tuple membership prevents accepting substrings such as '' or 'AE'.
    _choice(kind, tuple(KINDS), "kind")


def _bool(value, label):
    if type(value) is not bool:
        raise TypeError(f"{label} must be a bool")


@dataclass(frozen=True)
class Model:
    """One individual per occupied type. Use an ascending, distinct int tuple."""
    support: tuple[int, ...]

    def __post_init__(self):
        if type(self.support) is not tuple:
            raise TypeError("support must be a tuple")
        if not self.support:
            raise ValueError("the universe must be nonempty")
        for value in self.support:
            if type(value) is not int:
                raise TypeError("membership types must be integers, not bools")
            if not 0 <= value <= 7:
                raise ValueError("membership types must lie in 0..7")
        if self.support != tuple(sorted(set(self.support))):
            raise ValueError("support must be ascending and contain no duplicates")

    @classmethod
    def from_mask(cls, mask: int):
        """Decode an occupied-types bit mask, strictly in 1..255."""
        if type(mask) is not int:
            raise TypeError("mask must be an integer, not a bool")
        if not 1 <= mask <= 255:
            raise ValueError("mask must lie in 1..255")
        return cls(tuple(t for t in range(8) if mask & (1 << t)))

    @property
    def mask(self):
        return sum(1 << t for t in self.support)

    def extension(self, term: str):
        _choice(term, tuple(TERM_BITS), "term")
        return frozenset(t for t in self.support if t & TERM_BITS[term])

    def holds(self, kind: str, subject: str, predicate: str):
        """A: subset; E: disjoint; I: nonempty overlap; O: nonempty difference."""
        _kind(kind)
        x, y = self.extension(subject), self.extension(predicate)
        if kind == "A":
            return x <= y
        if kind == "E":
            return x.isdisjoint(y)
        if kind == "I":
            return bool(x & y)
        return bool(x - y)

    def admitted(self, mode: str):
        _choice(mode, MODES, "mode")
        return mode == "empty-allowed" or all(self.extension(t) for t in TERM_BITS)

    def as_dict(self):
        return {
            "support": list(self.support),
            "type_bits_PMS": [f"{t:03b}" for t in self.support],
            "cardinality": len(self.support),
            "mask": self.mask,
            "U": list(self.support),
            **{term: sorted(self.extension(term)) for term in TERM_BITS},
        }


def models(mode="empty-allowed"):
    """All canonical supports, ordered by size then lexicographically.

    Thus a first countermodel has minimum cardinality, with deterministic ties.
    This enumeration is justified by the support-compression proof in the docs.
    """
    _choice(mode, MODES, "mode")
    return tuple(
        model
        for size in range(1, 9)
        for support in combinations(range(8), size)
        if (model := Model(support)).admitted(mode)
    )


def premises_hold(model: Model, major: str, minor: str):
    if type(model) is not Model:
        raise TypeError("model must be a Model")
    _kind(major)
    _kind(minor)
    return model.holds(major, "M", "P") and model.holds(minor, "S", "M")


def conclusion_holds(model: Model, conclusion: str, *, reverse=False):
    if type(model) is not Model:
        raise TypeError("model must be a Model")
    _kind(conclusion)
    _bool(reverse, "reverse")
    subject, predicate = ("P", "S") if reverse else ("S", "P")
    return model.holds(conclusion, subject, predicate)


@dataclass(frozen=True)
class FormResult:
    form: str
    mode: str
    reverse: bool
    premise_model_count: int
    countermodel: Model | None

    @property
    def valid(self):
        return self.countermodel is None

    def as_dict(self):
        return {
            "form": self.form,
            "mode": self.mode,
            "direction": "P->S" if self.reverse else "S->P",
            "valid": self.valid,
            "premise_model_count": self.premise_model_count,
            "minimal_countermodel": None if self.valid else self.countermodel.as_dict(),
        }


def analyze_form(major, minor, conclusion, *, mode="empty-allowed", reverse=False):
    """Check a form over every canonical support; return its first countermodel."""
    for kind in (major, minor, conclusion):
        _kind(kind)
    _bool(reverse, "reverse")
    candidates = models(mode)
    count, countermodel = 0, None
    for model in candidates:
        if premises_hold(model, major, minor):
            count += 1
            if not conclusion_holds(model, conclusion, reverse=reverse):
                if countermodel is None:
                    countermodel = model
    return FormResult(major + minor + conclusion, mode, reverse, count, countermodel)


def all_forms(*, mode="empty-allowed", reverse=False):
    """64 results in explicit AEIO-major/minor/conclusion order."""
    _choice(mode, MODES, "mode")
    _bool(reverse, "reverse")
    return tuple(analyze_form(*form, mode=mode, reverse=reverse)
                 for form in product(KINDS, repeat=3))


def universal_witness(major, minor, conclusion, *, mode="all-nonempty"):
    """Smallest model of the premises AND A(S,P) or E(S,P), with S nonempty.

    The explicit S condition prevents a vacuous A/E witness when empty terms
    are allowed. Returns None only when no such witness exists.
    """
    for kind in (major, minor):
        _kind(kind)
    _choice(conclusion, ("A", "E"), "universal conclusion")
    for model in models(mode):
        if (model.extension("S") and premises_hold(model, major, minor)
                and conclusion_holds(model, conclusion)):
            return model
    return None


def nonproductive_witnesses(*, mode="all-nonempty"):
    """The twelve premise pairs outside the four I.4 productive routes."""
    _choice(mode, MODES, "mode")
    rows = []
    for major, minor in product(KINDS, repeat=2):
        pair = major + minor
        if pair in ORIGINAL_ROUTES:
            continue
        positive = universal_witness(major, minor, "A", mode=mode)
        negative = universal_witness(major, minor, "E", mode=mode)
        rows.append({
            "pair": pair,
            "mode": mode,
            "A_SP_witness": None if positive is None else positive.as_dict(),
            "E_SP_witness": None if negative is None else negative.as_dict(),
        })
    return rows
