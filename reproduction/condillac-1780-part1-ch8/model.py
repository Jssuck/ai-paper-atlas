"""Original qualitative teaching reconstruction of Condillac, La Logique I.8.

This is a modern finite semantics, not an algorithm attributed to Condillac.
The definitions model one object at one moment. No probability, utility,
learning threshold, clinical measurement, or action policy is supplied.
"""
from dataclasses import dataclass
from typing import FrozenSet, Tuple


def _boolean(value, name):
    if type(value) is not bool:
        raise TypeError(f"{name} must be a bool")


@dataclass(frozen=True)
class Affect:
    """Annotated present affective context; imagined pleasure need not be enjoyed.

    habitual_imagination records an established represented prospect, with no
    stipulated repetition count. Lacking is present, unlike future obtains.

    Deprivation-caused suffering is a stipulated link from the text. The
    directed flag records the orientation described there; it is not learned.
    A desire habit may persist while the present desire is suspended.
    """
    lacking: bool = False
    known: bool = False
    habitual_enjoyment: bool = False
    habitual_imagination: bool = False
    faculties_directed: bool = False
    desire_habit: bool = False

    def __post_init__(self):
        for name in self.__dataclass_fields__:
            _boolean(getattr(self, name), name)
        if (self.habitual_enjoyment or self.habitual_imagination) and not self.known:
            raise ValueError("enjoyment/imagination presupposes a known object")

    @property
    def deprivation(self):
        return self.lacking and self.known and (self.habitual_enjoyment or self.habitual_imagination)

    @property
    def need(self):
        # Textual causal stipulation, not a numerical measure of suffering.
        return self.deprivation

    @property
    def desire(self):
        return self.need and self.faculties_directed

    @property
    def passion_disposition(self):
        return self.desire_habit

    @property
    def passion_active(self):
        return self.passion_disposition and self.desire


@dataclass(frozen=True)
class JudgmentHabit:
    """An experience-backed habit is input evidence, not learned by this code."""
    established: bool = False
    from_experience: bool = False

    def __post_init__(self):
        _boolean(self.established, "established")
        _boolean(self.from_experience, "from_experience")

    @property
    def experience_backed(self):
        return self.established and self.from_experience


@dataclass(frozen=True)
class World:
    name: str
    # Future attainment in this case; not present possession.
    obtains: bool
    obstacle_free: bool

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("world name must be a nonempty string")
        _boolean(self.obtains, "obtains")
        _boolean(self.obstacle_free, "obstacle_free")


@dataclass(frozen=True)
class Beliefs:
    """Nonempty finite support for a categorical, possibly false judgment.

    The actual world belongs to the universe but need not belong to support.
    Predicates are deliberately separate. A bridge must be explicitly checked.
    """
    worlds: Tuple[World, ...]
    support: FrozenSet[str]
    actual: str

    def __post_init__(self):
        if not isinstance(self.worlds, tuple) or not all(isinstance(w, World) for w in self.worlds):
            raise TypeError("worlds must be a tuple of World values")
        if not isinstance(self.support, frozenset):
            raise TypeError("support must be a frozenset")
        names = [w.name for w in self.worlds]
        if not names or len(names) != len(set(names)):
            raise ValueError("world names must be nonempty and unique")
        if not self.support:
            raise ValueError("belief support must be nonempty")
        if not self.support.issubset(set(names)):
            raise ValueError("support must lie in the world universe")
        if self.actual not in names:
            raise ValueError("actual world must lie in the world universe")

    def _check_predicate(self, predicate):
        if predicate not in ("obtains", "obstacle_free"):
            raise ValueError("unknown predicate")

    def judges(self, predicate):
        self._check_predicate(predicate)
        return all(getattr(w, predicate) for w in self.worlds if w.name in self.support)

    def actually(self, predicate):
        self._check_predicate(predicate)
        return getattr(next(w for w in self.worlds if w.name == self.actual), predicate)

    @property
    def actual_in_support(self):
        return self.actual in self.support

    @property
    def obstacle_implies_obtains_on_support(self):
        return all((not w.obstacle_free) or w.obtains for w in self.worlds if w.name in self.support)

    def restrict(self, retained):
        """Restrict support; contradictory/empty evidence raises ValueError.

        This is a teaching operation, not a historical belief-update rule.
        Never invent a world or silently restore the actual world.
        """
        if not isinstance(retained, frozenset):
            raise TypeError("retained must be a frozenset")
        if not retained.issubset(self.support):
            raise ValueError("restriction cannot add a world")
        return Beliefs(self.worlds, retained, self.actual)


def evaluate(affect, beliefs, habit):
    """Return inspectable Boolean labels, without selecting an action."""
    if not isinstance(affect, Affect) or not isinstance(beliefs, Beliefs) or not isinstance(habit, JudgmentHabit):
        raise TypeError("evaluate requires Affect, Beliefs, JudgmentHabit")
    obtain_judgment = beliefs.judges("obtains")
    obstacle_judgment = beliefs.judges("obstacle_free")
    return {
        "objective_lack": affect.lacking,
        "deprivation": affect.deprivation,
        "deprivation_suffering": affect.need,
        "need": affect.need,
        "desire": affect.desire,
        "passion_disposition": affect.passion_disposition,
        "passion_active": affect.passion_active,
        "judges_obtaining": obtain_judgment,
        "judges_no_obstacle": obstacle_judgment,
        "experience_backed_habit": habit.experience_backed,
        "hope": affect.desire and obtain_judgment,
        "narrow_will": affect.desire and habit.experience_backed and obstacle_judgment,
        "actual_obtaining": beliefs.actually("obtains"),
        "actual_no_obstacle": beliefs.actually("obstacle_free"),
        "actual_in_support": beliefs.actual_in_support,
        "bridge_holds_on_support": beliefs.obstacle_implies_obtains_on_support,
    }
