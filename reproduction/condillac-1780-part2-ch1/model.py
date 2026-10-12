"""Original, finite teaching models prompted by Condillac, La Logique II.I.

This is a modern construction, not historical code or psychological validation.
All public inputs are finite iterables of nonempty string labels. A bare string
is not accepted as a collection. Functions are pure; snapshots are immutable.
"""
from dataclasses import dataclass
from typing import Iterable, Literal


def _symbols(values: Iterable[str], label: str) -> frozenset[str]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{label} must be a finite iterable, not one string")
    result = frozenset(values)
    if any(not isinstance(value, str) or not value for value in result):
        raise ValueError(f"{label} must contain nonempty strings")
    return result


def _subset(values: Iterable[str], universe: frozenset[str], label: str) -> frozenset[str]:
    result = _symbols(values, label)
    if not result <= universe:
        raise ValueError(f"{label} contains labels outside the universe")
    return result


def filter_evidence(
    hypotheses: Iterable[str],
    observations: Iterable[Iterable[str]],
    initial: Iterable[str] | None = None,
) -> tuple[frozenset[str], ...]:
    """Return C0, C1, ..., Cn with Ci = Ci-1 intersect Ei.

    Each Ei is a caller-supplied compatibility set, not raw sensory data.
    Even after the candidate set becomes empty, later input is validated.
    This function neither creates new hypotheses nor repairs wrong evidence.
    """
    universe = _symbols(hypotheses, "hypotheses")
    current = universe if initial is None else _subset(initial, universe, "initial")
    if isinstance(observations, (str, bytes)):
        raise TypeError("observations must be an iterable of compatibility sets")
    trace = [current]
    for index, observation in enumerate(observations):
        compatible = _subset(observation, universe, f"observation {index}")
        current = current & compatible
        trace.append(current)
    return tuple(trace)


@dataclass(frozen=True)
class Rule:
    """A positive Horn rule body -> head; facts belong in anchors instead."""
    body: frozenset[str]
    head: str

    def __post_init__(self) -> None:
        body = _symbols(self.body, "rule body")
        if not body:
            raise ValueError("empty rule bodies are not allowed; use an explicit anchor")
        if not isinstance(self.head, str) or not self.head:
            raise ValueError("rule head must be a nonempty string")
        object.__setattr__(self, "body", body)


@dataclass(frozen=True)
class FixedPoint:
    """Trace includes the initial state, but not a duplicate stable state."""
    kind: Literal["least", "greatest"]
    states: tuple[frozenset[str], ...]

    def __post_init__(self) -> None:
        if self.kind not in ("least", "greatest"):
            raise ValueError("kind must be 'least' or 'greatest'")
        if isinstance(self.states, (str, bytes)):
            raise TypeError("states must be an iterable of state collections")
        states = tuple(_symbols(state, "trace state") for state in self.states)
        if not states:
            raise ValueError("a fixed-point record needs at least one state")
        object.__setattr__(self, "states", states)

    @property
    def result(self) -> frozenset[str]:
        return self.states[-1]

    @property
    def changes(self) -> int:
        return len(self.states) - 1


@dataclass(frozen=True)
class HornSystem:
    """Finite positive rules; rules encode claimed support, not verified truth."""
    claims: frozenset[str]
    rules: tuple[Rule, ...]

    def __post_init__(self) -> None:
        claims = _symbols(self.claims, "claims")
        rules = tuple(self.rules)
        if any(not isinstance(rule, Rule) for rule in rules):
            raise TypeError("rules must contain Rule objects")
        for rule in rules:
            if not rule.body <= claims or rule.head not in claims:
                raise ValueError("all rule labels must belong to claims")
        object.__setattr__(self, "claims", claims)
        object.__setattr__(self, "rules", rules)

    def _context(self, anchors, withdrawn):
        anchors = _subset(anchors, self.claims, "anchors")
        withdrawn = _subset(withdrawn, self.claims, "withdrawn")
        return anchors, withdrawn

    def _step(self, state, anchors, withdrawn):
        derived = {rule.head for rule in self.rules if rule.body <= state}
        return (anchors | derived) - withdrawn

    def immediate(
        self, state: Iterable[str], anchors: Iterable[str] = (), withdrawn: Iterable[str] = ()
    ) -> frozenset[str]:
        """T(S) on U = V minus W; W overrides anchors and rule heads alike.

        W is externally stipulated exclusion, not automatically inferred negation.
        """
        anchors, withdrawn = self._context(anchors, withdrawn)
        state = _subset(state, self.claims - withdrawn, "state")
        return self._step(state, anchors, withdrawn)

    def fixed_point(
        self,
        kind: Literal["least", "greatest"],
        anchors: Iterable[str] = (),
        withdrawn: Iterable[str] = (),
    ) -> FixedPoint:
        """Iterate T from empty (least) or U (greatest); at most |U| changes."""
        if kind not in ("least", "greatest"):
            raise ValueError("kind must be 'least' or 'greatest'")
        anchors, withdrawn = self._context(anchors, withdrawn)
        current = frozenset() if kind == "least" else self.claims - withdrawn
        states = [current]
        while True:
            following = self._step(current, anchors, withdrawn)
            if following == current:
                return FixedPoint(kind, tuple(states))
            states.append(following)
            current = following
