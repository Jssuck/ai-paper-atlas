"""Original, dependency-free finite-model teaching reconstruction of Letter CIV.

This implements a specified modern semantics, not a transcription of Euler's
proof method. See README.md for the quotient theorem and historical cautions.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations, product
from typing import Iterable

TERMS = "ABC"
MOODS = "AEIO"
TERM_BITS = {"A": 1, "B": 2, "C": 4}
ROMANS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX")


def _validate_term(term: str) -> None:
    if not isinstance(term, str) or term not in TERMS or len(term) != 1:
        raise ValueError("a term must be exactly one of A, B, C")


def normalize_required(required: Iterable[str] = ()) -> tuple[str, ...]:
    """A string such as 'AC' or a finite iterable of term names is accepted."""
    if required is None:
        raise ValueError("required_nonempty must be an iterable of A/B/C names")
    try:
        result = tuple(required)
    except TypeError as exc:
        raise ValueError("required_nonempty must be iterable") from exc
    for term in result:
        _validate_term(term)
    if len(set(result)) != len(result):
        raise ValueError("duplicate nonempty assumptions are not accepted")
    return tuple(sorted(result))


@dataclass(frozen=True)
class Model:
    """Occupancy bit k means the A/B/C membership atom numbered k exists.

    Within an atom number: A = bit 1, B = bit 2, C = bit 4. Atom 0
    therefore lies outside all three sets. At most one witness per atom
    is needed. The universe is nonempty; individual terms may be empty.
    """
    occupancy: int

    def __post_init__(self) -> None:
        if type(self.occupancy) is not int or not 1 <= self.occupancy <= 255:
            raise ValueError("occupancy must be an integer from 1 through 255")

    @property
    def atoms(self) -> tuple[int, ...]:
        return tuple(atom for atom in range(8) if self.occupancy & (1 << atom))

    @property
    def size(self) -> int:
        return self.occupancy.bit_count()

    def members(self, term: str) -> tuple[int, ...]:
        _validate_term(term)
        return tuple(atom for atom in self.atoms if atom & TERM_BITS[term])

    def describe(self) -> dict:
        return {
            "occupancy": self.occupancy,
            "occupied_atoms": list(self.atoms),
            "universe_size": self.size,
            "universe": [f"x{atom}" for atom in self.atoms],
            "sets": {term: [f"x{atom}" for atom in self.members(term)] for term in TERMS},
        }


ALL_MODELS = tuple(sorted((Model(mask) for mask in range(1, 256)),
                          key=lambda m: (m.size, m.occupancy)))


@lru_cache(maxsize=None)
def region_mask(subject: str, predicate: str, region: str) -> int:
    _validate_term(subject)
    _validate_term(predicate)
    if region not in ("intersection", "difference"):
        raise ValueError("region must be intersection or difference")
    return sum(1 << atom for atom in range(8)
               if (atom & TERM_BITS[subject]) and
               (bool(atom & TERM_BITS[predicate]) == (region == "intersection")))


@dataclass(frozen=True, order=True)
class Statement:
    mood: str
    subject: str
    predicate: str

    def __post_init__(self) -> None:
        if not isinstance(self.mood, str) or len(self.mood) != 1 or self.mood not in MOODS:
            raise ValueError("mood must be exactly one of A, E, I, O")
        _validate_term(self.subject)
        _validate_term(self.predicate)
        if self.subject == self.predicate:
            raise ValueError("this teaching language requires two distinct terms")

    @classmethod
    def parse(cls, code: str) -> Statement:
        if not isinstance(code, str) or len(code) != 3:
            raise ValueError("a formula code must contain exactly three characters, e.g. AAB")
        return cls(*code)

    @property
    def code(self) -> str:
        return self.mood + self.subject + self.predicate

    def holds(self, model: Model) -> bool:
        if not isinstance(model, Model):
            raise ValueError("holds expects a Model")
        region = "difference" if self.mood in "AO" else "intersection"
        exists = bool(model.occupancy & region_mask(self.subject, self.predicate, region))
        return not exists if self.mood in "AE" else exists

    def english(self) -> str:
        x, y = self.subject, self.predicate
        return {"A": f"All {x} are {y}", "E": f"No {x} are {y}",
                "I": f"Some {x} are {y}", "O": f"Some {x} are not {y}"}[self.mood]

    def renamed(self, mapping: dict[str, str]) -> Statement:
        if (not isinstance(mapping, dict) or set(mapping) != set(TERMS) or
                any(not isinstance(t, str) for t in mapping.values()) or
                set(mapping.values()) != set(TERMS)):
            raise ValueError("term renaming must be a permutation of A, B, C")
        return Statement(self.mood, mapping[self.subject], mapping[self.predicate])

    def symmetry_normalized(self) -> str:
        if self.mood in "EI":
            return self.mood + "".join(sorted((self.subject, self.predicate)))
        return self.code


@dataclass(frozen=True)
class Argument:
    premises: tuple[Statement, Statement]
    conclusion: Statement

    def __post_init__(self) -> None:
        if (not isinstance(self.premises, tuple) or len(self.premises) != 2 or
                any(not isinstance(p, Statement) for p in self.premises)):
            raise ValueError("premises must be a tuple of exactly two Statements")
        if not isinstance(self.conclusion, Statement):
            raise ValueError("conclusion must be a Statement")

    @classmethod
    def parse(cls, premise1: str, premise2: str, conclusion: str) -> Argument:
        return cls((Statement.parse(premise1), Statement.parse(premise2)),
                   Statement.parse(conclusion))

    @property
    def code(self) -> str:
        return ",".join(p.code for p in self.premises) + "=>" + self.conclusion.code

    def renamed(self, mapping: dict[str, str]) -> Argument:
        return Argument(tuple(p.renamed(mapping) for p in self.premises),
                        self.conclusion.renamed(mapping))

    def as_dict(self) -> dict:
        return {"code": self.code, "premises": [p.code for p in self.premises],
                "conclusion": self.conclusion.code,
                "english": [p.english() for p in self.premises] + [self.conclusion.english()]}


def models_under(required_nonempty: Iterable[str] = ()) -> tuple[Model, ...]:
    return _models_under(normalize_required(required_nonempty))


@lru_cache(maxsize=None)
def _models_under(required: tuple[str, ...]) -> tuple[Model, ...]:
    return tuple(model for model in ALL_MODELS if all(model.members(term) for term in required))


@dataclass(frozen=True)
class Check:
    valid: bool
    models_checked: int
    premise_models: int
    counterexample_count: int
    first_counterexample: Model | None

    def as_dict(self, argument: Argument) -> dict:
        witness = None
        if self.first_counterexample:
            witness = self.first_counterexample.describe()
            witness["premises_true"] = [p.holds(self.first_counterexample) for p in argument.premises]
            witness["conclusion_true"] = argument.conclusion.holds(self.first_counterexample)
        return {"valid": self.valid, "models_checked": self.models_checked,
                "premise_satisfying_models": self.premise_models,
                "counterexample_count": self.counterexample_count,
                "minimal_counterexample": witness}


def check(argument: Argument, required_nonempty: Iterable[str] = ()) -> Check:
    if not isinstance(argument, Argument):
        raise ValueError("check expects an Argument")
    return _check(argument, normalize_required(required_nonempty))


@lru_cache(maxsize=None)
def _check(argument: Argument, required: tuple[str, ...]) -> Check:
    domain = _models_under(required)
    premise_models = [m for m in domain if all(p.holds(m) for p in argument.premises)]
    failures = [m for m in premise_models if not argument.conclusion.holds(m)]
    return Check(not failures, len(domain), len(premise_models), len(failures),
                 failures[0] if failures else None)


def minimal_nonempty_assumptions(argument: Argument) -> tuple[tuple[str, ...], ...]:
    """Inclusion-minimal term-existence sets making the inference valid.

    () within the result means no assumption is needed. An empty result
    means none of these eight assumption sets makes the inference valid.
    """
    valid = []
    for size in range(4):
        for subset in combinations(TERMS, size):
            if check(argument, subset).valid and not any(set(x) <= set(subset) for x in valid):
                valid.append(subset)
    return tuple(valid)


def canonical(argument: Argument, allow_ei_symmetry: bool = True) -> str:
    """Structural quotient: term permutations, premise exchange, E/I symmetry.

    With allow_ei_symmetry=False, even E/I term exchange is excluded.
    This does not allow contraposition, subalternation, conclusions to become
    premises, existential weakening, or arbitrary truth-functional equivalence.
    """
    if not isinstance(argument, Argument):
        raise ValueError("canonical expects an Argument")
    if type(allow_ei_symmetry) is not bool:
        raise ValueError("allow_ei_symmetry must be a bool")
    keys = []
    for names in permutations(TERMS):
        renamed = argument.renamed(dict(zip(TERMS, names)))
        code = (lambda s: s.symmetry_normalized()) if allow_ei_symmetry else (lambda s: s.code)
        premises = sorted(code(p) for p in renamed.premises)
        keys.append(",".join(premises) + "=>" + code(renamed.conclusion))
    return min(keys)


# Directly checked against the recap on printed pp. 116-117 (PDF leaves 137-138).
# XVI's printed conclusion is intentionally preserved here.
PRINTED_CODES = (
    ("AAB", "ACA", "ACB"), ("AAB", "ICA", "ICB"),
    ("AAB", "ECB", "ECA"), ("AAB", "EBC", "ECA"),
    ("AAB", "OCB", "OCA"), ("AAB", "ABC", "ICA"),
    ("EAB", "ACA", "ECB"), ("EAB", "ACB", "ECA"),
    ("EAB", "ICA", "OCB"), ("EAB", "IAC", "OCB"),
    ("EAB", "ICB", "OCA"), ("EAB", "IBC", "OCA"),
    ("IAB", "AAC", "ICB"), ("IAB", "ABC", "ICA"),
    ("OAB", "AAC", "OCB"), ("OAB", "ACB", "OAB"),
    ("AAB", "IAC", "ICB"), ("EAB", "AAC", "OCB"),
    ("EAB", "ABC", "OCA"), ("AAB", "AAC", "ICB"),
)

PRINTED_FORMS = dict(zip(ROMANS, (Argument.parse(*row) for row in PRINTED_CODES)))
REPAIRED_FORMS = {**PRINTED_FORMS, "XVI": Argument.parse("OAB", "ACB", "OAC")}

DERIVATIONS = {
    "I": "Any C-object is an A-object and therefore a B-object.",
    "II": "Take the C-and-A witness from premise 2; premise 1 puts it in B.",
    "III": "An object in C and A would be in B, contradicting C's disjointness from B.",
    "IV": "Disjointness is symmetric, so the reasoning for III applies.",
    "V": "Take the C-outside-B witness. If it were in A, it would be in B.",
    "VI": "Assume A is nonempty. Choose an A-object; it lies in B and hence C.",
    "VII": "Every C-object lies in A, which is disjoint from B.",
    "VIII": "Every C-object lies in B, which is disjoint from A.",
    "IX": "Take a C-and-A witness. Since A and B are disjoint, it is outside B.",
    "X": "The A-and-C witness is also a C-and-A witness; apply IX's reasoning.",
    "XI": "Take a C-and-B witness. Since A and B are disjoint, it is outside A.",
    "XII": "The B-and-C witness is also a C-and-B witness; apply XI's reasoning.",
    "XIII": "The A-and-B witness lies in C because every A is C, giving C-and-B.",
    "XIV": "The A-and-B witness lies in C because every B is C, giving C-and-A.",
    "XV": "The A-outside-B witness lies in C because every A is C.",
    "XVI": "Printed: the conclusion repeats premise 1, so its witness already exists. Repaired: take the A-outside-B witness; it cannot lie in C because C is a subset of B.",
    "XVII": "The A-and-C witness lies in B, so it is also a C-and-B witness.",
    "XVIII": "Assume A is nonempty. An A-object is in C and outside B.",
    "XIX": "Assume B is nonempty. A B-object is in C and outside A.",
    "XX": "Assume A is nonempty. An A-object lies in both B and C.",
}


def standard_candidates() -> tuple[tuple[str, int, Argument], ...]:
    """All 4^3 moods in each of four conventional figures, exactly 256.

    S=C, P=B, M=A; major premise first; conclusion always S-P (C-B).
    """
    figures = {1: ("AB", "CA"), 2: ("BA", "CA"),
               3: ("AB", "AC"), 4: ("BA", "AC")}
    return tuple(("".join(moods), figure, Argument.parse(moods[0] + pairs[0],
                  moods[1] + pairs[1], moods[2] + "CB"))
                 for figure, pairs in figures.items() for moods in product(MOODS, repeat=3))


def euler_style_candidates(first_moods: str = MOODS) -> tuple[Argument, ...]:
    """Fixed larger universe: first pair AB; second AC/CA/BC/CB;
    conclusion is the unused pair, either direction. 4*16*8 = 512.

    first_moods='IO' is the particular-first slice, exactly 256. Each
    argument connects three distinct pairings. A repeated premise-as-
    conclusion such as printed XVI is deliberately outside this universe.
    """
    if (not isinstance(first_moods, str) or not first_moods or
            any(mood not in MOODS for mood in first_moods) or
            len(set(first_moods)) != len(first_moods)):
        raise ValueError("first_moods must be a nonempty, duplicate-free string from AEIO")
    result = []
    for first in first_moods:
        for second_mood in MOODS:
            for pair2, remaining in (("AC", "BC"), ("CA", "BC"),
                                     ("BC", "AC"), ("CB", "AC")):
                for third in MOODS:
                    for pair3 in (remaining, remaining[::-1]):
                        result.append(Argument.parse(first + "AB", second_mood + pair2, third + pair3))
    return tuple(result)


def equivalent_groups(named_arguments: Iterable[tuple[str, Argument]],
                      allow_ei_symmetry: bool = True) -> list[dict]:
    groups: dict[str, list[str]] = {}
    for name, argument in named_arguments:
        groups.setdefault(canonical(argument, allow_ei_symmetry), []).append(name)
    return [{"canonical_key": key, "members": members} for key, members in sorted(groups.items())]
