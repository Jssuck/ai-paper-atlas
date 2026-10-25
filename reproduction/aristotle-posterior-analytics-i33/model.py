"""Original finite teaching models for Posterior Analytics I.33, not a knowledge oracle."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True)
class World:
    a: frozenset[int]
    b: frozenset[int]
    c: frozenset[int]

    def premises(self):
        return self.c <= self.b and self.b <= self.a

    def conclusion(self):
        return self.c <= self.a


def modal_profile(truths, actual=0):
    """Truth at actual index, all-world truth, and existence of a false instance.

    Only a chosen finite model's modality. No claim that these worlds exhaust
    metaphysical possibilities. Empty contexts and invalid actual indices fail.
    """
    truths = tuple(truths)
    if not truths or not 0 <= actual < len(truths):
        raise ValueError('nonempty worlds and an in-range actual index required')
    if any(type(t) is not bool for t in truths):
        raise TypeError('truth values must be bool')
    return {'actual': truths[actual], 'necessary_in_model': all(truths),
            'can_be_false_in_model': not all(truths)}

@dataclass(frozen=True)
class Judgment:
    agent: str
    time: str
    respect: str
    object_id: str
    proposition: str
    mode: str
    reason_trace: tuple[str, ...] = ()

    def __post_init__(self):
        if self.mode not in ('necessary', 'can_be_otherwise', 'uncommitted'):
            raise ValueError('unknown apprehension mode')

    def key(self):
        return self.agent, self.time, self.respect, self.object_id, self.proposition


def conflicts(judgments):
    """Explicit consistency convention, NOT a psychological impossibility proof.

    Labels are asserted apprehension modes, not objective truth or knowledge.
    A false necessity claim is representable. Distinct people/times/respects
    do not contradict each other under this deliberately narrow check.
    """
    grouped = {}
    for j in judgments:
        grouped.setdefault(j.key(), set()).add(j.mode)
    return sorted(key for key, modes in grouped.items() if {'necessary', 'can_be_otherwise'} <= modes)


def exhaustive_summary():
    subsets = [frozenset(i for i in range(2) if mask & (1 << i)) for mask in range(4)]
    worlds = [World(a, b, c) for a, b, c in product(subsets, repeat=3)]
    counts = dict(worlds=len(worlds), paired_models=0, necessary_premise_models=0,
                  necessary_premise_failures=0, actual_premise_models=0,
                  actual_premise_nonnecessary_conclusion=0)
    for w0, w1 in product(worlds, repeat=2):
        counts['paired_models'] += 1
        if w0.premises() and w1.premises():
            counts['necessary_premise_models'] += 1
            if not (w0.conclusion() and w1.conclusion()):
                counts['necessary_premise_failures'] += 1
        if w0.premises():
            counts['actual_premise_models'] += 1
            if not w1.conclusion():
                counts['actual_premise_nonnecessary_conclusion'] += 1
    return counts


def demonstration():
    # The same syntactic reason trace need not encode the same apprehension.
    trace = ('C subset B', 'B subset A', 'therefore C subset A')
    knower_claim = Judgment('reader-1', 't0', 'essential', 'C', 'C subset A', 'necessary', trace)
    opinion_claim = Judgment('reader-2', 't0', 'essential', 'C', 'C subset A', 'can_be_otherwise', trace)
    actual = World(frozenset({0}), frozenset({0}), frozenset({0}))
    alternate = World(frozenset(), frozenset({0}), frozenset({0}))
    return {
        'finite_enumeration': exhaustive_summary(),
        'actual_true_not_necessary': modal_profile([actual.conclusion(), alternate.conclusion()]),
        'necessary_truth_can_be_misapprehended': {'truth_profile': modal_profile([True, True]), 'asserted_mode': opinion_claim.mode},
        'shared_reason_trace': knower_claim.reason_trace == opinion_claim.reason_trace,
        'different_agents_conflicts': len(conflicts([knower_claim, opinion_claim])),
        'same_agent_conflicts': len(conflicts([knower_claim, Judgment('reader-1', 't0', 'essential', 'C', 'C subset A', 'can_be_otherwise', trace)])),
        'empty_reason_is_not_required_for_opinion': bool(opinion_claim.reason_trace),
    }

if __name__ == '__main__':
    print(json.dumps(demonstration(), indent=2, sort_keys=True))
