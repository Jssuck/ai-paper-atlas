"""A small modern model checker for Euler CII's four categorical forms.

No claim of historical reconstruction is made.  The universe is nonempty;
term extensions may be empty unless NONEMPTY_TERMS is selected.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Iterable, Iterator


FORMS = ("A", "E", "I", "O")
# Bit 0 is S∩P, bit 1 is S\P, bit 2 is P\S, bit 3 is U\(S∪P).
ATOM_NAMES = ("both", "s_only", "p_only", "outside")


class Mode(str, Enum):
    ALLOW_EMPTY_TERMS = "allow_empty_terms"
    NONEMPTY_TERMS = "nonempty_terms"


@dataclass(frozen=True)
class Model:
    """Finite extensional interpretation; labels are arbitrary integers."""

    universe: frozenset[int]
    subject: frozenset[int]
    predicate: frozenset[int]

    def __post_init__(self) -> None:
        # Freeze mutable set inputs as well; keep a genuinely immutable value.
        for name in ("universe", "subject", "predicate"):
            object.__setattr__(self, name, frozenset(getattr(self, name)))
        if not self.universe:
            raise ValueError("The universe must be nonempty.")
        if not (self.subject <= self.universe and self.predicate <= self.universe):
            raise ValueError("Both term extensions must be subsets of the universe.")

    def truth(self) -> dict[str, bool]:
        """A: all S are P; E: no S are P; I: some S are P; O: some S are not P."""
        intersection = self.subject & self.predicate
        difference = self.subject - self.predicate
        return {
            "A": self.subject <= self.predicate,  # includes equality and empty S
            "E": not intersection,
            "I": bool(intersection),  # at least one, not some-but-not-all
            "O": bool(difference),
        }

    def atoms(self) -> tuple[frozenset[int], ...]:
        return (
            self.subject & self.predicate,
            self.subject - self.predicate,
            self.predicate - self.subject,
            self.universe - (self.subject | self.predicate),
        )

    def occupancy(self) -> int:
        """Forget multiplicities; retain only which of the four atoms are nonempty."""
        return sum(1 << index for index, atom in enumerate(self.atoms()) if atom)

    def admitted(self, mode: Mode | str) -> bool:
        selected = Mode(mode)  # reject misspelled modes instead of silently defaulting
        return selected is Mode.ALLOW_EMPTY_TERMS or bool(self.subject and self.predicate)

    def as_dict(self) -> dict:
        return {
            "U": sorted(self.universe),
            "S": sorted(self.subject),
            "P": sorted(self.predicate),
            "occupancy_mask": self.occupancy(),
            "atoms_nonempty": dict(zip(ATOM_NAMES, map(bool, self.atoms()))),
            "truth": self.truth(),
        }


def canonical_model(mask: int) -> Model:
    """One witness per occupied atom.  Valid masks are 1..15, not empty U."""
    if type(mask) is not int or not 1 <= mask < 16:
        raise ValueError("An occupancy mask must be an integer from 1 through 15.")
    universe = frozenset(index for index in range(4) if mask & (1 << index))
    return Model(universe, universe & {0, 1}, universe & {0, 2})


def representatives(mode: Mode | str) -> tuple[Model, ...]:
    """Exhaust all admitted occupancy patterns; order by size, then mask."""
    selected = Mode(mode)
    models = (canonical_model(mask) for mask in range(1, 16))
    return tuple(sorted(
        (model for model in models if model.admitted(selected)),
        key=lambda model: (len(model.universe), model.occupancy()),
    ))


def counterexample(
    premises: Iterable[str], conclusion: str, mode: Mode | str
) -> Model | None:
    """Smallest canonical model satisfying all premises and falsifying conclusion.

    None means valid in this restricted two-term semantics.  An empty list of
    premises is allowed.  Forms refer to the same ordered pair (S, P).
    """
    premises = tuple(premises)
    if conclusion not in FORMS or any(form not in FORMS for form in premises):
        raise ValueError("Only A, E, I, and O over the same S and P are supported.")
    for model in representatives(mode):
        values = model.truth()
        if all(values[form] for form in premises) and not values[conclusion]:
            return model
    return None


def labeled_models(size: int) -> Iterator[Model]:
    """All 4**size assignments over the labeled universe {0,...,size-1}."""
    if type(size) is not int or size < 1:
        raise ValueError("The universe size must be a positive integer.")
    universe = frozenset(range(size))
    for assignments in product(range(4), repeat=size):
        subject = frozenset(i for i, atom in enumerate(assignments) if atom in (0, 1))
        predicate = frozenset(i for i, atom in enumerate(assignments) if atom in (0, 2))
        yield Model(universe, subject, predicate)
