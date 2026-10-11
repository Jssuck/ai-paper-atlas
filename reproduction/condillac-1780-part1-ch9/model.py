"""A small, non-empirical reconstruction of Condillac, La Logique I.IX.

All weights and capacity/decay rules are modern teaching assumptions.  The model
stores dispositions to react, not histories of episodes or lasting idea-events.
Only Python's standard library is used.  See MODEL.zh-CN.md for the exact contract.
"""
from dataclasses import dataclass
from typing import Hashable, Optional


def _integer(name: str, value: int, minimum: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _text(name: str, value: str, empty: bool = False) -> None:
    if not isinstance(value, str) or (not empty and not value):
        raise ValueError(f"{name} must be {'a' if empty else 'a nonempty'} string")


@dataclass(frozen=True)
class Choice:
    status: str  # chosen, missing, ambiguous
    value: Optional[Hashable] = None  # None can also be a *chosen* END
    strength: int = 0
    contenders: tuple = ()


class WeightedHabits:
    """Sparse positive integer edges; weakest then oldest edge is evicted.

    Capacity is a bound on edges, NOT bits, episodes, neurons, or human memory.
    Ties in retrieval are reported, never resolved by dictionary order.
    """

    def __init__(self, capacity: Optional[int] = None):
        if capacity is not None:
            _integer("capacity", capacity, 1)
        self.capacity = capacity
        self._weights: dict[tuple[Hashable, Hashable], int] = {}
        self._born: dict[tuple[Hashable, Hashable], int] = {}
        self._serial = 0

    @property
    def edge_count(self) -> int:
        return len(self._weights)

    def snapshot(self) -> dict:
        """A copy for observers; changing the result cannot change the model."""
        return dict(self._weights)

    def reinforce(self, key: Hashable, value: Hashable, amount: int = 1) -> None:
        _integer("amount", amount, 1)
        hash(key)
        hash(value)
        edge = (key, value)
        if edge not in self._weights:
            self._born[edge] = self._serial
            self._serial += 1
        self._weights[edge] = self._weights.get(edge, 0) + amount
        if self.capacity is not None and len(self._weights) > self.capacity:
            victim = min(self._weights, key=lambda e: (self._weights[e], self._born[e]))
            del self._weights[victim]
            del self._born[victim]

    def choose(self, key: Hashable) -> Choice:
        row = [(value, weight) for (k, value), weight in self._weights.items() if k == key]
        if not row:
            return Choice("missing")
        maximum = max(weight for _, weight in row)
        winners = tuple(value for value, weight in row if weight == maximum)
        if len(winners) != 1:
            return Choice("ambiguous", strength=maximum, contenders=winners)
        return Choice("chosen", winners[0], maximum, winners)

    def forget(self, steps: int = 1) -> None:
        _integer("steps", steps, 0)
        for edge in tuple(self._weights):
            remaining = max(0, self._weights[edge] - steps)
            if remaining == 0:
                del self._weights[edge]
                del self._born[edge]
            else:
                self._weights[edge] = remaining


@dataclass(frozen=True)
class Replay:
    tokens: tuple[str, ...]
    stop: str  # end, missing, ambiguous, budget
    decisions: tuple[Choice, ...]


class SequenceMemory:
    """A first-order, context-indexed transition disposition."""

    def __init__(self, capacity: Optional[int] = None):
        self.habits = WeightedHabits(capacity)

    def practice(self, tokens, context: str = "", repetitions: int = 1) -> None:
        _text("context", context, empty=True)
        _integer("repetitions", repetitions, 1)
        if isinstance(tokens, (str, bytes)):
            raise ValueError("tokens must be a nonempty sequence, not a bare string")
        tokens = tuple(tokens)
        if not tokens:
            raise ValueError("an episode must have at least one token")
        for token in tokens:
            _text("token", token)
        successors = tokens[1:] + (None,)
        for _ in range(repetitions):
            for current, successor in zip(tokens, successors):
                self.habits.reinforce((context, current), successor)

    def replay(self, cue: str, context: str = "", max_transitions: int = 100) -> Replay:
        _text("cue", cue)
        _text("context", context, empty=True)
        _integer("max_transitions", max_transitions, 0)
        output = [cue]
        decisions = []
        for _ in range(max_transitions):
            choice = self.habits.choose((context, output[-1]))
            decisions.append(choice)
            if choice.status != "chosen":
                return Replay(tuple(output), choice.status, tuple(decisions))
            if choice.value is None:
                return Replay(tuple(output), "end", tuple(decisions))
            output.append(choice.value)
        return Replay(tuple(output), "budget", tuple(decisions))


@dataclass(frozen=True)
class Signal:
    organ: str
    value: str

    def __post_init__(self):
        _text("organ", self.organ)
        _text("signal value", self.value)


@dataclass(frozen=True)
class Observation:
    idea: str
    signal: Signal

    def __post_init__(self):
        _text("idea", self.idea)
        if not isinstance(self.signal, Signal):
            raise ValueError("signal must be a Signal")


@dataclass(frozen=True)
class IdeaEvent:
    idea: str
    source: str  # external, cue, replay, feedback

    @property
    def supports_external_object(self) -> bool:
        """Event provenance, not a claim about human source-monitoring skill."""
        return self.source == "external"


@dataclass(frozen=True)
class BodyEvent:
    signal: Signal
    cause: IdeaEvent


@dataclass(frozen=True)
class Activation:
    event: Optional[IdeaEvent]
    status: str  # chosen, missing, ambiguous, blocked


@dataclass(frozen=True)
class EmbodiedReplay:
    replay: Replay
    events: tuple[IdeaEvent, ...]
    outputs: tuple[Optional[BodyEvent], ...]


class EmbodiedMemory:
    """Separate central, incoming, and outgoing learned dispositions.

    The same capacity is applied independently to each of three tables.
    No automatic plasticity occurs during recall or sensory feedback.
    Current activation is one event, not a persistent bank of ideas.
    Returned traces are the experimenter's observations, not internal memory.
    """

    def __init__(self, capacity: Optional[int] = None):
        self.brain = SequenceMemory(capacity)
        self.incoming = WeightedHabits(capacity)
        self.outgoing = WeightedHabits(capacity)
        self.active: Optional[IdeaEvent] = None
        self.afferent_enabled = True
        self.efferent_enabled = True

    def teach(self, observations, context: str = "", repetitions: int = 1) -> None:
        _text("context", context, empty=True)
        _integer("repetitions", repetitions, 1)
        observations = tuple(observations)
        if not observations or any(not isinstance(o, Observation) for o in observations):
            raise ValueError("observations must be a nonempty sequence of Observation")
        self.brain.practice((o.idea for o in observations), context, repetitions)
        for _ in range(repetitions):
            for observation in observations:
                self.incoming.reinforce((context, observation.signal), observation.idea)
                self.outgoing.reinforce((context, observation.idea), observation.signal)

    def clear_active(self) -> None:
        self.active = None

    def set_cue(self, idea: str) -> IdeaEvent:
        _text("idea", idea)
        self.active = IdeaEvent(idea, "cue")
        return self.active

    def _receive(self, signal: Signal, context: str, source: str) -> Activation:
        if not isinstance(signal, Signal):
            raise ValueError("signal must be a Signal")
        _text("context", context, empty=True)
        if not self.afferent_enabled:
            self.active = None
            return Activation(None, "blocked")
        choice = self.incoming.choose((context, signal))
        if choice.status != "chosen":
            self.active = None
            return Activation(None, choice.status)
        self.active = IdeaEvent(choice.value, source)
        return Activation(self.active, "chosen")

    def sense(self, signal: Signal, context: str = "") -> Activation:
        return self._receive(signal, context, "external")

    def express(self, context: str = "") -> Optional[BodyEvent]:
        _text("context", context, empty=True)
        if self.active is None or not self.efferent_enabled:
            return None
        choice = self.outgoing.choose((context, self.active.idea))
        if choice.status != "chosen":
            return None
        return BodyEvent(choice.value, self.active)

    def feedback(self, body: BodyEvent, context: str = "") -> Activation:
        if not isinstance(body, BodyEvent):
            raise ValueError("body must be a BodyEvent")
        # A motor-produced observation is not independent external evidence.
        return self._receive(body.signal, context, "feedback")

    def recall(self, context: str = "", max_transitions: int = 100) -> EmbodiedReplay:
        _text("context", context, empty=True)
        _integer("max_transitions", max_transitions, 0)
        if self.active is None:
            raise ValueError("activate a sensory or explicit cue before recall")
        first = self.active
        result = self.brain.replay(first.idea, context, max_transitions)
        events = [first]
        outputs = [self.express(context)]
        for token in result.tokens[1:]:
            self.active = IdeaEvent(token, "replay")
            events.append(self.active)
            outputs.append(self.express(context))
        return EmbodiedReplay(result, tuple(events), tuple(outputs))

    def forget(self, steps: int = 1) -> None:
        for table in (self.brain.habits, self.incoming, self.outgoing):
            table.forget(steps)
