"""Modern finite observation model for a Condillac reading; standard library only.

Not a transcription of a historical algorithm and not an empirical model of minds.
All tables are stipulated, total, deterministic, and noiseless. See README.md.
"""
from dataclasses import dataclass
from typing import Optional


def _text(value: object, label: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{label} must be a string")
    if not value.strip():
        raise ValueError(f"{label} must be nonempty and not whitespace-only")


def _tuple(value: object, label: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{label} must be a tuple")


@dataclass(frozen=True)
class Observation:
    """A named total function, with one string outcome per ordered world."""
    name: str
    outcomes: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.name, "observation name")
        _tuple(self.outcomes, "outcomes")
        if not self.outcomes:
            raise ValueError("outcomes must not be empty")
        for value in self.outcomes:
            _text(value, "outcome")


@dataclass(frozen=True)
class Model:
    """Finite world domain and observations; zero observations are permitted."""
    worlds: tuple[str, ...]
    observations: tuple[Observation, ...]

    def __post_init__(self) -> None:
        _tuple(self.worlds, "worlds")
        _tuple(self.observations, "observations")
        if not self.worlds:
            raise ValueError("worlds must not be empty")
        for world in self.worlds:
            _text(world, "world")
        if len(set(self.worlds)) != len(self.worlds):
            raise ValueError("world names must be unique")
        for obs in self.observations:
            if type(obs) is not Observation:
                raise TypeError("observations must contain Observation instances")
            if len(obs.outcomes) != len(self.worlds):
                raise ValueError("each observation must give one outcome per world")
        names = tuple(obs.name for obs in self.observations)
        if len(set(names)) != len(names):
            raise ValueError("observation names must be unique")

    def observation(self, name: str) -> Observation:
        _text(name, "query")
        for obs in self.observations:
            if obs.name == name:
                return obs
        raise ValueError(f"unknown query: {name!r}")

    def world_index(self, world: str) -> int:
        _text(world, "world")
        try:
            return self.worlds.index(world)
        except ValueError:
            raise ValueError(f"unknown world: {world!r}") from None

    def outcome(self, query: str, world: str) -> str:
        """Read a stipulated table; this is not a real-world sensing operation."""
        obs = self.observation(query)
        return obs.outcomes[self.world_index(world)]

    def signature(self, world: str) -> tuple[str, ...]:
        index = self.world_index(world)
        return tuple(obs.outcomes[index] for obs in self.observations)

    def fiber(self, world: str) -> tuple[str, ...]:
        """Worlds indistinguishable under every observation in this model."""
        signature = self.signature(world)
        return tuple(w for w in self.worlds if self.signature(w) == signature)


@dataclass(frozen=True)
class Evidence:
    query: str
    outcome: str

    def __post_init__(self) -> None:
        _text(self.query, "query")
        _text(self.outcome, "outcome")


class InconsistentEvidence(ValueError):
    """No world can satisfy this complete evidence history."""


@dataclass(frozen=True)
class Belief:
    """Immutable evidence history. Candidates are derived, never guessed.

    `observe` accepts an outcome supplied by the caller. It checks consistency,
    not truth. Only `consult` generates stipulated truthful outcomes internally.
    """
    model: Model
    history: tuple[Evidence, ...] = ()

    def __post_init__(self) -> None:
        if type(self.model) is not Model:
            raise TypeError("model must be a Model instance")
        _tuple(self.history, "history")
        for evidence in self.history:
            if type(evidence) is not Evidence:
                raise TypeError("history must contain Evidence instances")
            obs = self.model.observation(evidence.query)
            if evidence.outcome not in obs.outcomes:
                raise ValueError("outcome is outside this query's range")
        if not self.candidates:
            raise InconsistentEvidence("evidence eliminates every world")

    @property
    def candidates(self) -> tuple[str, ...]:
        return tuple(
            world for world in self.model.worlds
            if all(self.model.outcome(e.query, world) == e.outcome
                   for e in self.history)
        )

    def observe(self, query: str, outcome: str) -> "Belief":
        """Append checked evidence; conflicting evidence raises, without mutation."""
        return Belief(self.model, self.history + (Evidence(query, outcome),))

    def consult(self, query: str, true_world: str, *, accept: bool = True) -> "Belief":
        """A simulation helper; the learner otherwise does not know true_world.

        Refusal returns this same state. Accepted feedback comes from the model's
        table. Retention of truth assumes the prior history also retained truth.
        """
        if type(accept) is not bool:
            raise TypeError("accept must be a bool")
        self.model.observation(query)
        self.model.world_index(true_world)
        if not accept:
            return self
        return self.observe(query, self.model.outcome(query, true_world))

    def recognizes(self) -> Optional[str]:
        """A unique candidate, or None. Uniqueness does not validate false input."""
        candidates = self.candidates
        return candidates[0] if len(candidates) == 1 else None

    def distinguishes(self, query: str) -> bool:
        """Whether this query has at least two outcomes on current candidates."""
        self.model.observation(query)
        return len({self.model.outcome(query, w) for w in self.candidates}) > 1


@dataclass(frozen=True)
class Judgment:
    """A checked guess and a separate stipulated feeling; neither updates Belief."""
    correct: bool
    satisfied: bool

    def __post_init__(self) -> None:
        if type(self.correct) is not bool or type(self.satisfied) is not bool:
            raise TypeError("judgment fields must be bools")


def judge(model: Model, guess: str, true_world: str, *, satisfied: bool) -> Judgment:
    if type(model) is not Model:
        raise TypeError("model must be a Model instance")
    model.world_index(guess)
    model.world_index(true_world)
    if type(satisfied) is not bool:
        raise TypeError("satisfied must be a bool")
    return Judgment(correct=(guess == true_world), satisfied=satisfied)
