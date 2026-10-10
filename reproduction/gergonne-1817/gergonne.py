"""Finite extensional teaching reconstruction of Gergonne (1817), §§5–66.

Python 3.10+ standard library only. This is new code, not historical software.
The principal semantics requires P, M, G all nonempty. See PROOF.md for why
the seven occupied-membership atoms cover arbitrary, including infinite, sets.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from itertools import product
from typing import Iterable

TERMS = ("P", "M", "G")
LETTERS = "ANan"  # Gergonne's proposition kinds, not modern A/E/I/O.
RELATIONS = "HXICD"  # D is our ASCII alias for the original reversed C.
REVERSE_RELATION = dict(zip(RELATIONS, "HXIDC"))
FIGURES = {
    1: (("M", "G"), ("P", "M")),
    2: (("G", "M"), ("M", "P")),
    3: (("G", "M"), ("P", "M")),
    4: (("M", "G"), ("M", "P")),
}
MODERN_FIGURE = {1: 1, 2: 4, 3: 2, 4: 3}
CONTRADICTORY = {"A": "n", "n": "A", "N": "a", "a": "N"}
SIMPLE_CONVERSION = frozenset("Na")


@dataclass(frozen=True, order=True)
class Model:
    """One representative per occupied atom; bits P=1, M=2, G=4.

    mask bit (atom-1) marks occupancy of atom in 1..7. The atom number is
    also the representative's identity, not a cardinality. Objects outside
    P union M union G never affect this fragment and are omitted.
    """

    mask: int

    def __post_init__(self) -> None:
        if type(self.mask) is not int or not 0 <= self.mask < 128:
            raise ValueError("mask must be an integer in 0..127")

    @property
    def atoms(self) -> tuple[int, ...]:
        return tuple(a for a in range(1, 8) if self.mask & (1 << (a - 1)))

    @cache
    def term(self, name: str) -> frozenset[int]:
        try:
            bit = 1 << TERMS.index(name)
        except ValueError as exc:
            raise ValueError(f"unknown term: {name}") from exc
        return frozenset(a for a in self.atoms if a & bit)

    @property
    def all_terms_nonempty(self) -> bool:
        return all(self.term(t) for t in TERMS)

    def as_dict(self) -> dict:
        return {
            "mask": self.mask,
            "occupied_atoms": list(self.atoms),
            "size": len(self.atoms),
            "terms": {t: sorted(self.term(t)) for t in TERMS},
        }


@cache
def models(nonempty: bool = True) -> tuple[Model, ...]:
    """Canonical patterns, ordered by witness size then mask."""
    return tuple(
        sorted(
            (Model(m) for m in range(128) if not nonempty or Model(m).all_terms_nonempty),
            key=lambda m: (len(m.atoms), m.mask),
        )
    )


def proposition(kind: str, first: frozenset, second: frozenset) -> bool:
    """A: subset; N: disjoint; a: intersects; n: first-minus-second exists.

    Nonemptiness is a model restriction, not silently added to universals.
    This same evaluator supports the explicitly separate empty-term study.
    """
    if kind == "A":
        return first <= second
    if kind == "N":
        return first.isdisjoint(second)
    if kind == "a":
        return bool(first & second)
    if kind == "n":
        return bool(first - second)
    raise ValueError(f"unknown proposition kind: {kind}")


def relation(first: frozenset, second: frozenset) -> str:
    """The five mutually exclusive/exhaustive cases, for nonempty terms."""
    if not first or not second:
        raise ValueError("Gergonne's five-way partition requires both terms nonempty")
    if first.isdisjoint(second):
        return "H"
    if first == second:
        return "I"
    if first < second:
        return "C"
    if second < first:
        return "D"
    return "X"


def relation_triple(model: Model) -> tuple[str, str, str]:
    """Fixed direction: (M,G), (P,M), (P,G), regardless of figure."""
    return tuple(relation(model.term(a), model.term(b))
                 for a, b in (("M", "G"), ("P", "M"), ("P", "G")))


@dataclass(frozen=True, order=True)
class Literal:
    kind: str
    subject: str
    predicate: str

    def __post_init__(self) -> None:
        if self.kind not in LETTERS or len(self.kind) != 1:
            raise ValueError("unknown proposition kind")
        if self.subject not in TERMS or self.predicate not in TERMS:
            raise ValueError("unknown term")

    def holds(self, model: Model) -> bool:
        return proposition(self.kind, model.term(self.subject), model.term(self.predicate))

    def reverse(self) -> Literal:
        return Literal(self.kind, self.predicate, self.subject)

    def contradict(self) -> Literal:
        return Literal(CONTRADICTORY[self.kind], self.subject, self.predicate)

    def text(self) -> str:
        return f"{self.kind}({self.subject},{self.predicate})"


@dataclass(frozen=True, order=True)
class Mood:
    figure: int
    major: str
    minor: str
    conclusion: str

    def __post_init__(self) -> None:
        if self.figure not in FIGURES:
            raise ValueError("original figure must be in 1..4")
        if any(k not in LETTERS or len(k) != 1 for k in self.kinds):
            raise ValueError("mood letters must each be A, N, a or n")

    @property
    def kinds(self) -> tuple[str, str, str]:
        return self.major, self.minor, self.conclusion

    @property
    def id(self) -> str:
        return f"{self.figure}:{''.join(self.kinds)}"

    @property
    def original_ascii(self) -> str:
        """r marks a rotated original character; r and D are modern aliases."""
        first_reversed = self.figure in (2, 3)
        second_reversed = self.figure in (2, 4)
        return " ".join((
            ("r" if first_reversed else "") + self.major,
            ("r" if second_reversed else "") + self.minor,
            self.conclusion,
        ))

    def literals(self) -> tuple[Literal, Literal, Literal]:
        (s1, p1), (s2, p2) = FIGURES[self.figure]
        return (Literal(self.major, s1, p1), Literal(self.minor, s2, p2),
                Literal(self.conclusion, "P", "G"))

    def premises_hold(self, model: Model) -> bool:
        major, minor, _ = self.literals()
        return major.holds(model) and minor.holds(model)

    def is_countermodel(self, model: Model) -> bool:
        return self.premises_hold(model) and not self.literals()[2].holds(model)


def candidates() -> tuple[Mood, ...]:
    return tuple(Mood(f, *kinds) for f in FIGURES for kinds in product(LETTERS, repeat=3))


def countermodel(mood: Mood, nonempty: bool = True) -> Model | None:
    return next((m for m in models(nonempty) if mood.is_countermodel(m)), None)


@cache
def valid_moods(nonempty: bool = True) -> tuple[Mood, ...]:
    return tuple(m for m in candidates() if countermodel(m, nonempty) is None)


def rule59_violations(mood: Mood) -> tuple[str, ...]:
    """Independent, literal implementation of §59's eight printed rules.

    The common-language 'one premise may be ...' means at most one.
    This classifier does not call the semantic model checker.
    """
    f, a, b, c = mood.figure, *mood.kinds
    negative = lambda k: k in "Nn"
    particular = lambda k: k in "an"
    neg_count = int(negative(a)) + int(negative(b))
    par_count = int(particular(a)) + int(particular(b))
    broken = []
    if neg_count > 1 or (neg_count == 1 and not negative(c)):
        broken.append("I")
    if par_count > 1 or (par_count == 1 and not particular(c)):
        broken.append("II")
    if particular(a) and negative(b):
        broken.append("III")
    if neg_count == 0 and negative(c):
        broken.append("IV")
    if f == 1 and (particular(a) or negative(b)):
        broken.append("V")
    if f == 2 and ((not negative(a) and particular(b))
                   or (neg_count > 0 and particular(a))
                   or (not negative(b) and not particular(c))):
        broken.append("VI")
    if f == 3 and (neg_count != 1 or particular(a)):
        broken.append("VII")
    if f == 4 and (negative(b) or not particular(c)):
        broken.append("VIII")
    return tuple(broken)


def conversion_targets(kind: str, nonempty: bool = True) -> tuple[str, ...]:
    """All kinds k for which kind(P,G) entails k(G,P)."""
    return tuple(k for k in LETTERS
                 if all(not Literal(kind, "P", "G").holds(m)
                        or Literal(k, "G", "P").holds(m) for m in models(nonempty)))


def reverse_premise(mood: Mood, index: int) -> Mood:
    if index not in (0, 1):
        raise ValueError("premise index must be 0 or 1")
    if mood.kinds[index] not in SIMPLE_CONVERSION:
        raise ValueError("only N and a have a simple converse")
    directions = list(FIGURES[mood.figure])
    directions[index] = directions[index][::-1]
    figure = next(f for f, d in FIGURES.items() if d == tuple(directions))
    return Mood(figure, *mood.kinds)


def reverse_conclusion(mood: Mood) -> Mood:
    """§62(2): reverse conclusion, rename P/G, and exchange premises."""
    if mood.conclusion not in SIMPLE_CONVERSION:
        raise ValueError("only N and a have a simple converse")
    rename = {"P": "G", "G": "P", "M": "M"}
    directions = tuple(tuple(rename[t] for t in d) for d in FIGURES[mood.figure][::-1])
    figure = next(f for f, d in FIGURES.items() if d == directions)
    return Mood(figure, mood.minor, mood.major, mood.conclusion)


def equivalent_neighbors(mood: Mood, conclusions: bool = False) -> tuple[Mood, ...]:
    result = [reverse_premise(mood, i) for i in (0, 1)
              if mood.kinds[i] in SIMPLE_CONVERSION]
    if conclusions and mood.conclusion in SIMPLE_CONVERSION:
        result.append(reverse_conclusion(mood))
    return tuple(result)


def equivalence_classes(conclusions: bool = False) -> tuple[tuple[Mood, ...], ...]:
    unseen = set(valid_moods())
    groups = []
    while unseen:
        seed = min(unseen)
        found, agenda = {seed}, [seed]
        for current in agenda:
            for neighbor in equivalent_neighbors(current, conclusions):
                if neighbor not in found:
                    found.add(neighbor)
                    agenda.append(neighbor)
        if not found <= unseen:
            raise AssertionError("conversion graph is not a partition")
        unseen -= found
        groups.append(tuple(sorted(found)))
    return tuple(groups)


def weakened_neighbors(mood: Mood) -> tuple[Mood, ...]:
    """§62(3–4): weaken conclusion or strengthen one premise.

    Direction is from a sufficient base inference to an inference it entails.
    The word 'weakened' refers to inference strength, not to premise strength.
    """
    result = []
    if mood.conclusion in "AN":
        result.append(Mood(mood.figure, mood.major, mood.minor, mood.conclusion.lower()))
    for i in (0, 1):
        if mood.kinds[i] in "an":
            kinds = list(mood.kinds)
            kinds[i] = kinds[i].upper()
            result.append(Mood(mood.figure, *kinds))
    return tuple(result)


def reduction_closure(seeds: Iterable[Mood]) -> frozenset[Mood]:
    found = set(seeds)
    agenda = list(found)
    for mood in agenda:
        for child in equivalent_neighbors(mood, True) + weakened_neighbors(mood):
            if child not in found:
                found.add(child)
                agenda.append(child)
    return frozenset(found)


# Original §63–64 representatives, with unrotated A/N/a/n plus figure index.
# The representatives are source anchors; the computed class counts are not
# supplied by these lists. §66 reduces the last four of SIX to the first two.
FOURTEEN = tuple(Mood(f, *word) for f, word in (
    (1, "Nan"), (3, "ANN"), (3, "ANn"), (1, "NAN"), (4, "Aaa"),
    (1, "NAn"), (2, "aAa"), (4, "NAn"), (1, "AAA"), (1, "AAa"),
    (3, "Ann"), (4, "AAa"), (4, "nAn"), (2, "AAa"),
))
ELEVEN = tuple(m for m in FOURTEEN if m not in
               {Mood(2, *"aAa"), Mood(2, *"AAa"), Mood(3, *"ANN")})
SIX = tuple(Mood(f, *word) for f, word in (
    (1, "AAA"), (1, "NAN"), (4, "Aaa"), (1, "Nan"), (3, "Ann"), (4, "nAn"),
))


def base_inference(major: Literal, minor: Literal) -> Literal:
    """Apply only the two final bases: AAA or NAN in the first figure."""
    if major.kind not in "AN" or minor.kind != "A" or major.subject != minor.predicate:
        raise ValueError("not an instance of the AAA/NAN bases")
    return Literal(major.kind, minor.subject, major.predicate)


def reductio_certificates() -> list[dict]:
    """Explicit §66 certificates; no search-based implication oracle used."""
    certificates = []
    for target in SIX[2:]:
        major, minor, conclusion = target.literals()
        denied = conclusion.contradict()
        if target == Mood(4, *"Aaa"):
            used_major, used_minor, contradicted = denied.reverse(), major, minor
            conversion = denied.text() + " -> " + denied.reverse().text()
        elif target == Mood(1, *"Nan"):
            used_major, used_minor, contradicted = major.reverse(), denied, minor
            conversion = major.text() + " -> " + major.reverse().text()
        elif target == Mood(3, *"Ann"):
            used_major, used_minor, contradicted = major, denied, minor
            conversion = None
        else:
            used_major, used_minor, contradicted = denied, minor, major
            conversion = None
        derived = base_inference(used_major, used_minor)
        if derived != contradicted.contradict():
            raise AssertionError("invalid reductio certificate")
        certificates.append({
            "target": target.id,
            "original_ascii": target.original_ascii,
            "target_literals": [x.text() for x in target.literals()],
            "deny_conclusion": denied.text(),
            "simple_conversion": conversion,
            "base": "AAA" if used_major.kind == "A" else "NAN",
            "base_premises": [used_major.text(), used_minor.text()],
            "derived": derived.text(),
            "contradicts_original_premise": contradicted.text(),
        })
    return certificates
