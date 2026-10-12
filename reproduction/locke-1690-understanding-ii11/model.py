"""Finite teaching models prompted by Locke, Essay II.XI; not a model of a mind.

Only Python's standard library is used. Validation is explicit and survives -O.
The finite universe is always supplied; an unused representation label is not
silently added to a quotient's domain.
"""

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Mapping, Sequence


def _names(values: Iterable[str], label: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{label} must be an iterable of names, not one string")
    result = tuple(values)
    if any(not isinstance(value, str) or not value for value in result):
        raise ValueError(f"{label} must contain nonempty strings")
    if len(set(result)) != len(result):
        raise ValueError(f"{label} must not contain duplicates")
    return result


def _natural(value: int, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{label} must be a nonnegative integer, excluding bool")
    return value


def _representation(domain: Sequence[str], representation: Mapping[str, str]):
    objects = _names(domain, "domain")
    if set(representation) != set(objects):
        raise ValueError("representation must have exactly the domain's keys")
    fibers: dict[str, list[str]] = {}
    for item in objects:
        label = representation[item]
        if not isinstance(label, str) or not label:
            raise ValueError("representation labels must be nonempty strings")
        fibers.setdefault(label, []).append(item)
    return objects, fibers


@dataclass(frozen=True)
class PairConflict:
    """Two ordered pairs in the same fiber rectangle with different values."""

    representation_pair: tuple[str, str]
    true_pair: tuple[str, str]
    false_pair: tuple[str, str]


@dataclass(frozen=True)
class RelationDescent:
    quotient: dict[tuple[str, str], bool] | None
    conflicts: tuple[PairConflict, ...]

    @property
    def descends(self) -> bool:
        return self.quotient is not None


def descend_relation(
    domain: Sequence[str],
    representation: Mapping[str, str],
    relation: Mapping[tuple[str, str], bool],
) -> RelationDescent:
    """Return the unique quotient on the image, or one witness per bad block.

    Each nonempty Cartesian product of two fibers is checked in supplied domain
    order. Ordered pairs are not symmetrized. A conflicting relation produces no
    partial quotient: the returned quotient is None.
    """
    objects, fibers = _representation(domain, representation)
    expected = set(product(objects, repeat=2))
    if set(relation) != expected:
        raise ValueError("relation must specify exactly every ordered domain pair")
    if any(type(value) is not bool for value in relation.values()):
        raise ValueError("relation values must be bool, not integer surrogates")
    quotient: dict[tuple[str, str], bool] = {}
    conflicts = []
    for left_label, left_fiber in fibers.items():
        for right_label, right_fiber in fibers.items():
            witnesses: dict[bool, tuple[str, str]] = {}
            for pair in product(left_fiber, right_fiber):
                witnesses.setdefault(relation[pair], pair)
            block = (left_label, right_label)
            if len(witnesses) == 2:
                conflicts.append(PairConflict(block, witnesses[True], witnesses[False]))
            else:
                quotient[block] = next(iter(witnesses))
    return RelationDescent(None if conflicts else quotient, tuple(conflicts))


@dataclass(frozen=True)
class UnaryDescent:
    quotient: dict[str, bool] | None
    # Each triple is (representation label, true object, false object).
    conflicts: tuple[tuple[str, str, str], ...]


def descend_unary(
    domain: Sequence[str], representation: Mapping[str, str], predicate: Mapping[str, bool]
) -> UnaryDescent:
    """Unary analogue used to separate retained features from lost relations."""
    objects, fibers = _representation(domain, representation)
    if set(predicate) != set(objects):
        raise ValueError("predicate must have exactly the domain's keys")
    if any(type(value) is not bool for value in predicate.values()):
        raise ValueError("predicate values must be bool")
    quotient = {}
    conflicts = []
    for label, fiber in fibers.items():
        witnesses: dict[bool, str] = {}
        for item in fiber:
            witnesses.setdefault(predicate[item], item)
        if len(witnesses) == 2:
            conflicts.append((label, witnesses[True], witnesses[False]))
        else:
            quotient[label] = next(iter(witnesses))
    return UnaryDescent(None if conflicts else quotient, tuple(conflicts))


@dataclass(frozen=True)
class Multiset:
    """A finite-alphabet count vector, with a canonical sorted alphabet.

    Direct construction must already be canonical. Use from_pairs for ordinary
    input: repeated entries add, zero entries disappear from support, and every
    input count must itself be nonnegative.
    """

    alphabet: tuple[str, ...]
    counts: tuple[int, ...]

    def __post_init__(self):
        if type(self.alphabet) is not tuple or type(self.counts) is not tuple:
            raise ValueError("alphabet and counts must be tuples")
        names = _names(self.alphabet, "alphabet")
        if names != tuple(sorted(names)):
            raise ValueError("direct construction requires a sorted alphabet")
        if len(names) != len(self.counts):
            raise ValueError("one count is required for each alphabet atom")
        for count in self.counts:
            _natural(count, "count")

    @classmethod
    def from_pairs(cls, alphabet: Iterable[str], pairs: Iterable[tuple[str, int]] = ()):
        names = tuple(sorted(_names(alphabet, "alphabet")))
        values = dict.fromkeys(names, 0)
        for atom, count in pairs:
            if atom not in values:
                raise ValueError(f"unknown atom: {atom!r}")
            values[atom] += _natural(count, "count")
        return cls(names, tuple(values[atom] for atom in names))

    @property
    def total(self) -> int:
        return sum(self.counts)

    @property
    def support(self) -> tuple[str, ...]:
        return tuple(atom for atom, count in zip(self.alphabet, self.counts) if count)

    def as_dict(self) -> dict[str, int]:
        return {atom: count for atom, count in zip(self.alphabet, self.counts) if count}

    def add(self, other: "Multiset") -> "Multiset":
        if not isinstance(other, Multiset) or self.alphabet != other.alphabet:
            raise ValueError("addition requires the same atom alphabet")
        return Multiset(self.alphabet, tuple(a + b for a, b in zip(self.counts, other.counts)))

    def scale(self, factor: int) -> "Multiset":
        factor = _natural(factor, "factor")
        return Multiset(self.alphabet, tuple(factor * count for count in self.counts))

    def project(self, kept_atoms: Iterable[str]) -> "Multiset":
        kept = tuple(sorted(_names(kept_atoms, "kept atoms")))
        if not set(kept).issubset(self.alphabet):
            raise ValueError("projection may keep only known atoms")
        values = dict(zip(self.alphabet, self.counts))
        return Multiset(kept, tuple(values[atom] for atom in kept))

    def rename(self, target_alphabet: Iterable[str], mapping: Mapping[str, str]) -> "Multiset":
        target = tuple(sorted(_names(target_alphabet, "target alphabet")))
        if set(mapping) != set(self.alphabet):
            raise ValueError("renaming must specify exactly every source atom")
        if any(value not in target for value in mapping.values()):
            raise ValueError("renaming images must belong to the target alphabet")
        return Multiset.from_pairs(target, ((mapping[a], c) for a, c in zip(self.alphabet, self.counts)))


@dataclass(frozen=True)
class DeterministicPolicy:
    """A total extensional table; a table does not reveal an internal mechanism."""

    name: str
    stimuli: tuple[str, ...]
    responses: tuple[str, ...]

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("policy name must be nonempty")
        if type(self.stimuli) is not tuple or type(self.responses) is not tuple:
            raise ValueError("stimuli and responses must be tuples")
        _names(self.stimuli, "stimuli")
        if len(self.responses) != len(self.stimuli):
            raise ValueError("policy must specify exactly one response per stimulus")
        if any(not isinstance(response, str) or not response for response in self.responses):
            raise ValueError("responses must be nonempty strings")

    def response(self, stimulus: str) -> str:
        if stimulus not in self.stimuli:
            raise ValueError(f"unknown stimulus: {stimulus!r}")
        return self.responses[self.stimuli.index(stimulus)]


def enumerate_policies(stimuli: Iterable[str], actions: Iterable[str]) -> tuple[DeterministicPolicy, ...]:
    domain = _names(stimuli, "stimuli")
    labels = _names(actions, "actions")
    if not labels:
        raise ValueError("at least one admissible action is required")
    return tuple(DeterministicPolicy(f"table_{i}", domain, outputs)
                 for i, outputs in enumerate(product(labels, repeat=len(domain))))


@dataclass(frozen=True)
class VersionSpace:
    stimuli: tuple[str, ...]
    survivors: tuple[DeterministicPolicy, ...]

    def possible_actions(self, stimulus: str) -> tuple[str, ...]:
        if stimulus not in self.stimuli:
            raise ValueError(f"unknown stimulus: {stimulus!r}")
        return tuple(sorted({policy.response(stimulus) for policy in self.survivors}))

    def unanimous(self, stimulus: str) -> str | None:
        possibilities = self.possible_actions(stimulus)
        return possibilities[0] if len(possibilities) == 1 else None

    def status(self, stimulus: str) -> str:
        possibilities = self.possible_actions(stimulus)
        return ("empty_version_space" if not possibilities else
                "unanimous" if len(possibilities) == 1 else "underdetermined")


def version_space(
    stimuli: Iterable[str], actions: Iterable[str],
    admissible: Iterable[DeterministicPolicy], observations: Iterable[tuple[str, str]],
) -> VersionSpace:
    """Filter an explicitly chosen hypothesis class; do not infer capacity.

    Repeated identical observations are harmless. Conflicting observations are
    invalid for this deterministic model. A coherent observation can still leave
    no admissible policy, which is reported as empty rather than as unanimity.
    """
    domain = _names(stimuli, "stimuli")
    labels = _names(actions, "actions")
    if not labels:
        raise ValueError("at least one admissible action is required")
    policies = tuple(admissible)
    if any(not isinstance(policy, DeterministicPolicy) for policy in policies):
        raise ValueError("admissible entries must be DeterministicPolicy instances")
    _names((policy.name for policy in policies), "policy names")
    for policy in policies:
        if policy.stimuli != domain or any(response not in labels for response in policy.responses):
            raise ValueError("admissible policies must use this ordered domain and action set")
    observed: dict[str, str] = {}
    for stimulus, response in observations:
        if stimulus not in domain or response not in labels:
            raise ValueError("observation outside the stimulus/action domain")
        if stimulus in observed and observed[stimulus] != response:
            raise ValueError("conflicting observations violate deterministic assumptions")
        observed[stimulus] = response
    survivors = tuple(policy for policy in policies
                      if all(policy.response(s) == a for s, a in observed.items()))
    return VersionSpace(domain, survivors)
