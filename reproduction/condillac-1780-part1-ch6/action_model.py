"""Finite contextual action tables and explicit normative codes.

All assumptions are modern teaching constructions, not mental or ethical facts.
"""

from dataclasses import dataclass


def _labels(values, name):
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{name} must be a collection, not a scalar str/bytes")
    values = tuple(values)
    if any(not isinstance(v, str) or not v for v in values):
        raise ValueError(f"{name} must contain only nonempty strings")
    if len(set(values)) != len(values):
        raise ValueError(f"{name} must not contain duplicates")
    return values


@dataclass(frozen=True)
class Policy:
    """Rows are intentions, columns are contexts; every entry is an action."""

    contexts: tuple
    intentions: tuple
    actions: tuple
    rows: tuple

    def __post_init__(self):
        for name in ("contexts", "intentions", "actions"):
            object.__setattr__(self, name, _labels(getattr(self, name), name))
        if isinstance(self.rows, (str, bytes)):
            raise TypeError("rows must be a collection, not a scalar str/bytes")
        source_rows = tuple(self.rows)
        if any(isinstance(row, (str, bytes)) for row in source_rows):
            raise TypeError("policy rows must be collections, not scalar str/bytes")
        rows = tuple(tuple(row) for row in source_rows)
        if len(rows) != len(self.intentions):
            raise ValueError("there must be one row for each intention")
        if any(len(row) != len(self.contexts) for row in rows):
            raise ValueError("there must be one entry per context in each row")
        if any(a not in self.actions for row in rows for a in row):
            raise ValueError("policy entries must belong to the action universe")
        object.__setattr__(self, "rows", rows)

    def action(self, intention, context):
        if intention not in self.intentions or context not in self.contexts:
            raise ValueError("unknown intention or context")
        return self.rows[self.intentions.index(intention)][self.contexts.index(context)]


def compatible_intentions(policy, observations):
    """Keep intentions matching every observation; contradictory records give ()."""
    if isinstance(observations, (str, bytes)):
        raise TypeError("observations must be a collection, not a scalar str/bytes")
    observations = tuple(observations)
    if any(isinstance(observation, (str, bytes)) for observation in observations):
        raise TypeError("observations must be pairs, not scalar str/bytes")
    observations = tuple(tuple(observation) for observation in observations)
    for observation in observations:
        if len(observation) != 2:
            raise ValueError("an observation must be a (context, action) pair")
        context, action = observation
        if context not in policy.contexts or action not in policy.actions:
            raise ValueError("unknown observation context or action")
    return tuple(
        intention for intention in policy.intentions
        if all(policy.action(intention, context) == action for context, action in observations)
    )


def behavioral_classes(policy, contexts):
    """Partition intentions by their action vector on the selected contexts."""
    contexts = _labels(contexts, "selected contexts")
    if any(context not in policy.contexts for context in contexts):
        raise ValueError("selected context is unknown")
    blocks = {}
    for intention in policy.intentions:
        signature = tuple(policy.action(intention, context) for context in contexts)
        blocks.setdefault(signature, []).append(intention)
    return tuple(tuple(block) for block in blocks.values())


def admissible_norms(universe, required=(), forbidden=()):
    """Enumerate C with required <= C and C disjoint from forbidden.

    These explicit bridges are assumptions. Feasibility is not an implicit bridge.
    Overlapping required/forbidden sets produce an empty family, not an exception.
    """
    universe = _labels(universe, "action universe")
    required = frozenset(_labels(required, "required actions"))
    forbidden = frozenset(_labels(forbidden, "forbidden actions"))
    if not required <= set(universe) or not forbidden <= set(universe):
        raise ValueError("bridge actions must belong to the action universe")
    if required & forbidden:
        return ()
    codes = tuple(
        frozenset(action for i, action in enumerate(universe) if mask & (1 << i))
        for mask in range(1 << len(universe))
    )
    return tuple(code for code in codes if required <= code and not code & forbidden)


def normative_status(action, universe, candidate_norms):
    """Four statuses; an empty family is inconsistent, never unanimous approval."""
    universe = _labels(universe, "action universe")
    if action not in universe:
        raise ValueError("action must belong to the action universe")
    if isinstance(candidate_norms, (str, bytes)):
        raise TypeError("candidate_norms must be a collection, not a scalar str/bytes")
    codes = tuple(frozenset(_labels(code, "normative code")) for code in candidate_norms)
    if any(not code <= set(universe) for code in codes):
        raise ValueError("all code actions must belong to the action universe")
    if not codes:
        return "inconsistent"
    judgments = {action in code for code in codes}
    if judgments == {True}:
        return "all_permit"
    if judgments == {False}:
        return "all_forbid"
    return "underdetermined"
