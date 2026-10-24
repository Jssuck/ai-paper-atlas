"""Original finite-time teaching model, not an account of Aristotle's ontology."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True)
class Slice:
    a: frozenset
    b: frozenset
    c: frozenset


def relation(s):
    """Major B⊆A, minor C⊆B, conclusion C⊆A at one time."""
    return s.b <= s.a, s.c <= s.b, s.c <= s.a


def summarize(trace):
    """Nonempty finite horizon only; 'all' is not an assertion about eternity."""
    trace = tuple(trace)
    if not trace:
        raise ValueError('nonempty horizon required')
    rows = tuple(relation(s) for s in trace)
    return {
        'major_all': all(r[0] for r in rows),
        'minor_all': all(r[1] for r in rows),
        'conclusion_all': all(r[2] for r in rows),
        'conclusion_failure_times': [i for i, r in enumerate(rows) if not r[2]],
        'premise_failure_times': {
            'major': [i for i, r in enumerate(rows) if not r[0]],
            'minor': [i for i, r in enumerate(rows) if not r[1]],
        },
    }


def event_summary(trigger, event):
    trigger, event = tuple(trigger), tuple(event)
    if not trigger or len(trigger) != len(event):
        raise ValueError('equal nonempty horizons required')
    if any(type(x) is not bool for x in trigger + event):
        raise ValueError('boolean values required')
    return {'conditional_all': all(not t or e for t, e in zip(trigger, event)),
            'event_all': all(event), 'event_some': any(event),
            'trigger_some': any(trigger)}


def continuation(prefix, future, time):
    """Value of an explicitly defined infinite binary sequence at a finite index."""
    prefix = tuple(prefix)
    if type(time) is not int or time < 0:
        raise ValueError('nonnegative integer time required')
    if type(future) is not bool or any(type(x) is not bool for x in prefix):
        raise ValueError('boolean sequence required')
    return prefix[time] if time < len(prefix) else future


def all_subsets(n):
    return tuple(frozenset(i for i in range(n) if mask & (1 << i))
                 for mask in range(1 << n))


def oracle_row(s, universe):
    # Independently evaluate quantified implications, without subset operators.
    return tuple(all((not antecedent(x)) or consequent(x) for x in universe)
                 for antecedent, consequent in ((lambda x: x in s.b, lambda x: x in s.a),
                                                (lambda x: x in s.c, lambda x: x in s.b),
                                                (lambda x: x in s.c, lambda x: x in s.a)))


def enumerate_models():
    universe = range(2)
    subsets = all_subsets(2)
    states = tuple(Slice(*p) for p in product(subsets, repeat=3))
    counts = {'traces': 0, 'oracle_mismatches': 0, 'both_premises_all': 0,
              'preservation_failures': 0, 'conclusion_not_all': 0,
              'contrapositive_failures': 0, 'snapshot_upgrade_counterexamples': 0}
    for trace in product(states, repeat=2):
        counts['traces'] += 1
        actual = summarize(trace)
        expected = tuple(all(oracle_row(s, universe)[j] for s in trace) for j in range(3))
        got = actual['major_all'], actual['minor_all'], actual['conclusion_all']
        counts['oracle_mismatches'] += got != expected
        both = actual['major_all'] and actual['minor_all']
        counts['both_premises_all'] += both
        counts['preservation_failures'] += both and not actual['conclusion_all']
        counts['conclusion_not_all'] += not actual['conclusion_all']
        counts['contrapositive_failures'] += not actual['conclusion_all'] and both
        counts['snapshot_upgrade_counterexamples'] += all(relation(trace[0])[:2]) and not actual['conclusion_all']
    event_cases = 0
    event_oracle_mismatches = 0
    for values in product((False, True), repeat=6):
        trigger, event = values[:3], values[3:]
        actual = event_summary(trigger, event)
        expected = not any(t and not e for t, e in zip(trigger, event))
        event_cases += 1
        event_oracle_mismatches += actual['conditional_all'] != expected
    return {'scope': 'two objects, two times; event model: three times',
            'temporal_models': counts,
            'event_cases': event_cases, 'event_oracle_mismatches': event_oracle_mismatches,
            'examples': {
                'intermittent_event': event_summary((False, True, False), (False, True, False)),
                'vacuous_condition': event_summary((False, False, False), (False, False, False)),
                'equal_prefix_different_future': {
                    'prefix': [True] * 4,
                    'constant_extension_at_4': continuation((True,) * 4, True, 4),
                    'changed_extension_at_4': continuation((True,) * 4, False, 4)}}}

if __name__ == '__main__':
    print(json.dumps(enumerate_models(), ensure_ascii=False, indent=2))
