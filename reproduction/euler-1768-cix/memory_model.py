#!/usr/bin/env python3
"""A modern teaching countermodel for distinctions in Euler's Lettre CIX.

This is not Euler's algorithm, a reconstruction of a historical machine,
a psychological simulation, or evidence for or against substance dualism.
Python 3.10+; standard library only. No randomness, network, or hidden history.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from enum import Enum
from itertools import product
import json
from pathlib import Path
from typing import Any


class PreconditionError(ValueError):
    """A well-formed action is unavailable in this valid state."""


class Cue(Enum):
    FIRE = "fire"
    BELL = "bell"  # An invented second token, not an example from the letter.


class Kind(Enum):
    PERCEIVE = "perceive"
    WITHDRAW = "withdraw"
    SET_ASIDE = "set_aside"
    RECALL = "recall"
    MAKE_INACCESSIBLE = "make_inaccessible"
    ERASE_ALL = "erase_all"


CUE_ACTIONS = frozenset({Kind.PERCEIVE, Kind.RECALL, Kind.MAKE_INACCESSIBLE})


def _cue(value: Any, *, nullable: bool = False) -> Cue | None:
    if nullable and value is None:
        return None
    if type(value) is not str:
        raise TypeError("a serialized cue must be a string")
    try:
        return Cue(value)
    except ValueError as exc:
        raise ValueError(f"unknown cue: {value!r}") from exc


def _keys(data: Any, expected: set[str]) -> None:
    if type(data) is not dict:
        raise TypeError("expected a plain dictionary")
    if set(data) != expected:
        raise ValueError(f"expected exactly these keys: {sorted(expected)}")


def _cue_set(values: Any) -> frozenset[Cue]:
    if type(values) is not list:
        raise TypeError("serialized cue sets must be lists")
    parsed = [_cue(value) for value in values]
    if len(parsed) != len(set(parsed)):
        raise ValueError("duplicate cues are not allowed")
    return frozenset(parsed)


def _label(cue: Cue | None) -> str | None:
    return None if cue is None else cue.value


@dataclass(frozen=True)
class State:
    """Complete model state. Logs and real-world event history are NOT fields."""

    retained: frozenset[Cue] = frozenset()
    recallable: frozenset[Cue] = frozenset()
    attention: Cue | None = None
    sensory: Cue | None = None

    def __post_init__(self) -> None:
        for field in (self.retained, self.recallable):
            if type(field) is not frozenset:
                raise TypeError("retained and recallable must be frozensets")
            if any(type(cue) is not Cue for cue in field):
                raise TypeError("memory sets can contain only Cue members")
        if not self.recallable <= self.retained:
            raise ValueError("recallable must be a subset of retained")
        for name, cue in (("attention", self.attention), ("sensory", self.sensory)):
            if cue is not None and type(cue) is not Cue:
                raise TypeError(f"{name} must be a Cue or None")
            if cue is not None and cue not in self.recallable:
                raise ValueError(f"{name} must be recallable in this model")

    def to_dict(self) -> dict[str, Any]:
        return {
            "retained": sorted(cue.value for cue in self.retained),
            "recallable": sorted(cue.value for cue in self.recallable),
            "attention": _label(self.attention),
            "sensory": _label(self.sensory),
        }

    @classmethod
    def from_dict(cls, data: Any) -> State:
        _keys(data, {"retained", "recallable", "attention", "sensory"})
        return cls(_cue_set(data["retained"]), _cue_set(data["recallable"]),
                   _cue(data["attention"], nullable=True),
                   _cue(data["sensory"], nullable=True))


@dataclass(frozen=True)
class Action:
    kind: Kind
    cue: Cue | None = None

    def __post_init__(self) -> None:
        if type(self.kind) is not Kind:
            raise TypeError("kind must be a Kind member")
        if self.kind in CUE_ACTIONS:
            if type(self.cue) is not Cue:
                raise TypeError(f"{self.kind.value} requires a Cue")
        elif self.cue is not None:
            raise ValueError(f"{self.kind.value} takes no cue")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "cue": _label(self.cue)}

    @classmethod
    def from_dict(cls, data: Any) -> Action:
        _keys(data, {"kind", "cue"})
        if type(data["kind"]) is not str:
            raise TypeError("serialized kind must be a string")
        return cls(Kind(data["kind"]), _cue(data["cue"], nullable=True))


@dataclass(frozen=True)
class Output:
    """A report, not additional memory. Conviction is NOT external-world truth."""

    attention: Cue | None
    sensory_input: Cue | None
    current_existence_conviction: Cue | None
    recognized: bool | None = None  # Defined only on a perception event.
    recall_succeeded: bool | None = None  # Defined only on a recall attempt.

    def to_dict(self) -> dict[str, Any]:
        return {
            "attention": _label(self.attention),
            "sensory_input": _label(self.sensory_input),
            "current_existence_conviction": _label(self.current_existence_conviction),
            "recognized": self.recognized,
            "recall_succeeded": self.recall_succeeded,
        }


def transition(state: State, action: Action) -> tuple[State, Output]:
    """Pure deterministic transition. Invalid operations raise, never mutate."""
    if type(state) is not State or type(action) is not Action:
        raise TypeError("transition requires a State and an Action")
    state.__post_init__()
    action.__post_init__()
    r, a, q, s = state.retained, state.recallable, state.attention, state.sensory
    recognized = recalled = None
    x = action.cue
    if action.kind is Kind.PERCEIVE:
        recognized = x in r  # Check BEFORE storing the new perception.
        r, a, q, s = r | {x}, a | {x}, x, x
    elif action.kind is Kind.WITHDRAW:
        s = None  # The idea may remain attended after the stimulus ends.
    elif action.kind is Kind.SET_ASIDE:
        q = None  # Storage and current input are independent of attention.
    elif action.kind is Kind.RECALL:
        recalled = x in a
        if recalled:
            q = x  # Deliberately never writes to the sensory-input field.
    elif action.kind is Kind.MAKE_INACCESSIBLE:
        if x not in r:
            raise PreconditionError("cannot block access to an unretained representation")
        if s is x:
            raise PreconditionError("withdraw that sensory input before blocking recall")
        a = a - {x}
        if q is x:
            q = None
    elif action.kind is Kind.ERASE_ALL:
        # A stipulated complete reset, not a theory of human forgetting.
        r, a, q, s = frozenset(), frozenset(), None, None
    else:  # Defensive: enum validation currently makes this unreachable.
        raise ValueError("unsupported action")
    after = State(r, a, q, s)
    return after, Output(q, s, s, recognized, recalled)


def all_actions() -> tuple[Action, ...]:
    return tuple(Action(kind, cue) for kind in Kind for cue in
                 (tuple(Cue) if kind in CUE_ACTIONS else (None,)))


def all_states() -> tuple[State, ...]:
    """Enumerate all valid states independently of the transition function."""
    states = []
    # For each cue: 0 absent, 1 retained but inaccessible, 2 recallable.
    for status in product(range(3), repeat=len(Cue)):
        retained = frozenset(c for c, flag in zip(Cue, status) if flag > 0)
        recallable = frozenset(c for c, flag in zip(Cue, status) if flag == 2)
        foreground = (None,) + tuple(c for c in Cue if c in recallable)
        states.extend(State(retained, recallable, q, s)
                      for q, s in product(foreground, repeat=2))
    return tuple(states)


def _require(condition: bool, message: str) -> None:
    # Unlike assert statements, these checks also run under python -O.
    if not condition:
        raise AssertionError(message)


def exhaustive_check() -> dict[str, Any]:
    """Check the complete small domain; counts are software coverage, not data."""
    states, actions = all_states(), all_actions()
    successful = rejected = 0
    for state, action in product(states, actions):
        clone = State.from_dict(state.to_dict())
        try:
            after, output = transition(state, action)
        except PreconditionError:
            rejected += 1
            try:
                transition(clone, Action.from_dict(action.to_dict()))
            except PreconditionError:
                continue
            raise AssertionError("equal state/input changed action validity")
        successful += 1
        _require(after in states, "transition left the valid state domain")
        _require((after, output) == transition(clone, Action.from_dict(action.to_dict())),
                 "equal state/action did not produce equal state/output")
        _require(output.current_existence_conviction == after.sensory, "conviction/input mismatch")
        if action.kind is Kind.RECALL:
            _require(after.sensory == state.sensory, "recall changed sensory input")
            _require(output.recall_succeeded == (action.cue in state.recallable), "recall/access mismatch")
        if action.kind is Kind.PERCEIVE:
            _require(output.recognized == (action.cue in state.retained), "recognition/prior-retention mismatch")
        if action.kind not in (Kind.PERCEIVE, Kind.ERASE_ALL):
            _require(after.retained == state.retained, "control operation changed retention")
    reached, queue = {State()}, deque([State()])
    while queue:
        state = queue.popleft()
        for action in actions:
            try:
                after, _ = transition(state, action)
            except PreconditionError:
                continue
            if after not in reached:
                reached.add(after)
                queue.append(after)
    _require(reached == set(states), "valid-state enumeration and reachability disagree")
    return {
        "model_kind": "modern teaching countermodel, not empirical cognition",
        "states": len(states), "reachable_states": len(reached),
        "actions": len(actions), "state_action_pairs": len(states) * len(actions),
        "successful_transitions": successful, "rejected_preconditions": rejected,
        "checks": ["state invariants", "equal-state/equal-action consistency",
                   "recall does not create sensory input", "recognition checks prior retention",
                   "retention persists under non-erasing control actions", "all valid states reachable"],
        "status": "PASS",
    }


def trace(actions: list[Action], initial: State | None = None) -> dict[str, Any]:
    """Observer log only. transition() never reads this record."""
    state = State() if initial is None else initial
    result = {"initial_state": state.to_dict(), "steps": []}
    for i, action in enumerate(actions, 1):
        state, output = transition(state, action)
        result["steps"].append({"step": i, "action": action.to_dict(),
                                "state": state.to_dict(), "output": output.to_dict()})
    return result


def demo() -> dict[str, Any]:
    p = Action(Kind.PERCEIVE, Cue.FIRE)
    w, aside = Action(Kind.WITHDRAW), Action(Kind.SET_ASIDE)
    recall = Action(Kind.RECALL, Cue.FIRE)
    inaccessible = Action(Kind.MAKE_INACCESSIBLE, Cue.FIRE)
    erase = Action(Kind.ERASE_ALL)
    known, _ = transition(State(), p)
    erased, _ = transition(known, erase)
    fresh_result = transition(State(), p)
    erased_result = transition(erased, p)
    return {
        "schema_version": 1,
        "scope": "Original teaching construction for Euler, Lettre CIX, 10 March 1761; not a historical algorithm or empirical simulation.",
        "source_printed_pages": "144-148 (1768 volume II)",
        "token_note": "fire follows Euler's example; bell is an invented contrast token",
        "cases": {
            "retained_is_not_currently_attended": trace([p, w, aside, aside]),
            "recalled_fire_without_present_sensory_conviction": trace([p, w, aside, recall]),
            "inaccessible_then_recognized": trace([p, w, inaccessible, recall, p]),
            "never_seen_then_not_recognized": trace([recall, p]),
            "complete_erasure_then_not_recognized": trace([p, erase, recall, p]),
            "recall_fire_while_perceiving_bell": trace([p, Action(Kind.PERCEIVE, Cue.BELL), recall]),
            "recall_with_independent_current_fire_input": trace([p, recall]),
        },
        "equal_state_witness": {
            "erased_state": erased.to_dict(), "fresh_state": State().to_dict(),
            "same_complete_state": erased == State(), "same_next_action": p.to_dict(),
            "same_next_state_and_output": fresh_result == erased_result,
            "recognition_after_either_history": fresh_result[1].recognized,
            "warning": "Different observer histories cannot matter unless some difference survives in model state or subsequent input.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--demo", action="store_true", help="emit deterministic step-by-step examples (default)")
    mode.add_argument("--check", action="store_true", help="exhaustively check the finite model")
    parser.add_argument("--output", type=Path, help="write JSON here instead of standard output")
    args = parser.parse_args()
    rendered = json.dumps(exhaustive_check() if args.check else demo(), indent=2, ensure_ascii=False) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
