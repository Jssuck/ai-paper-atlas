"""Finite observational identifiability: a modern, stipulated teaching model."""
from dataclasses import dataclass
from typing import Hashable, Mapping


@dataclass(frozen=True)
class Answer:
    """inconsistent / identified / ambiguous; no vacuous identification."""
    status: str
    candidates: tuple[str, ...]
    values: tuple[Hashable, ...]


@dataclass(frozen=True)
class FiniteModel:
    columns: tuple[str, ...]
    states: tuple[str, ...]
    signatures: tuple[tuple[int, ...], ...]
    labels: tuple[str, ...]

    def __post_init__(self):
        if not all(isinstance(x, tuple) for x in
                   (self.columns, self.states, self.signatures, self.labels)):
            raise TypeError("model data must be immutable tuples")
        if not all(isinstance(x, str) and x for x in self.columns + self.states):
            raise ValueError("column and state identifiers must be nonempty strings")
        if len(set(self.columns)) != len(self.columns):
            raise ValueError("duplicate observation column")
        if len(set(self.states)) != len(self.states):
            raise ValueError("duplicate state identifier")
        if not len(self.states) == len(self.signatures) == len(self.labels):
            raise ValueError("state, signature and label lengths must agree")
        if not all(isinstance(x, str) for x in self.labels):
            raise TypeError("labels must be strings")
        for row in self.signatures:
            self._check_signature(row)

    @classmethod
    def from_rows(cls, columns: tuple[str, ...], rows: Mapping[str, tuple[int, ...]]):
        return cls(columns, tuple(rows), tuple(rows.values()), tuple(rows))

    def _check_signature(self, row):
        if not isinstance(row, tuple) or len(row) != len(self.columns):
            raise ValueError("signature must be a tuple with one entry per column")
        if any(type(value) is not int for value in row):
            raise TypeError("observation values must be exact integers")

    def _check_domain(self, mapping):
        if set(mapping) != set(self.states):
            raise ValueError("mapping domain must equal the model state set")

    def fibers(self) -> tuple[tuple[str, ...], ...]:
        groups = {}
        for state, signature in zip(self.states, self.signatures):
            groups.setdefault(signature, []).append(state)
        return tuple(tuple(group) for group in groups.values())

    def candidates(self, observed: tuple[int, ...]) -> tuple[str, ...]:
        self._check_signature(observed)
        return tuple(state for state, signature in zip(self.states, self.signatures)
                     if signature == observed)

    def answer(self, observed: tuple[int, ...], query: Mapping[str, Hashable]) -> Answer:
        self._check_domain(query)
        if any(not isinstance(value, Hashable) for value in query.values()):
            raise TypeError("query values must be hashable")
        candidates = self.candidates(observed)
        if not candidates:
            return Answer("inconsistent", (), ())
        values = tuple(dict.fromkeys(query[state] for state in candidates))
        status = "identified" if len(values) == 1 else "ambiguous"
        return Answer(status, candidates, values)

    def globally_identifiable(self, query: Mapping[str, Hashable]) -> bool:
        """A global property; vacuously true on an empty model, unlike answer()."""
        self._check_domain(query)
        return all(self.answer(row, query).status == "identified"
                   for row in dict.fromkeys(self.signatures))

    def with_labels(self, labels: Mapping[str, str]):
        """Change linguistic metadata, never measurement values."""
        self._check_domain(labels)
        return FiniteModel(self.columns, self.states, self.signatures,
                           tuple(labels[state] for state in self.states))

    def append_observation(self, name: str, values: Mapping[str, int]):
        self._check_domain(values)
        if name in self.columns:
            raise ValueError("new observation name must be distinct")
        rows = tuple(row + (values[state],)
                     for state, row in zip(self.states, self.signatures))
        return FiniteModel(self.columns + (name,), self.states, rows, self.labels)

    def restrict(self, allowed):
        """An assumption filters H; it does not supply another observation."""
        allowed = frozenset(allowed)
        if not allowed <= set(self.states):
            raise ValueError("unknown state in assumption")
        selected = [i for i, state in enumerate(self.states) if state in allowed]
        return FiniteModel(self.columns, tuple(self.states[i] for i in selected),
                           tuple(self.signatures[i] for i in selected),
                           tuple(self.labels[i] for i in selected))

    def refines(self, other) -> bool:
        """Compare information on the same state domain, ignoring row order."""
        if set(self.states) != set(other.states):
            raise ValueError("refinement requires the same state domain")
        old = dict(zip(other.states, other.signatures))
        return all(len({old[state] for state in fiber}) == 1
                   for fiber in self.fibers())
