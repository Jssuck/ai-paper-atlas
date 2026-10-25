"""Finite extensional teaching model, not a detector of scientific immediacy."""
from itertools import product
import json


def all_of(subject, predicate):
    return subject <= predicate


def none_of(subject, predicate):
    return not subject & predicate


def status(quality, subject, predicate):
    """Empty subjects are true, never 'wholly false', in modern semantics."""
    if quality not in ('all', 'none'):
        raise ValueError('quality must be all or none')
    truth = all_of if quality == 'all' else none_of
    opposite = none_of if quality == 'all' else all_of
    if truth(subject, predicate):
        return 'true'
    if opposite(subject, predicate):
        return 'wholly_false'
    return 'partly_false'


def premises(form, a, b, c):
    """Return major then minor as (quality, subject, predicate)."""
    return {
        'Barbara': (('all', c, a), ('all', b, c)),
        'Celarent': (('none', c, a), ('all', b, c)),
        'Cesare': (('none', a, c), ('all', b, c)),
        'Camestres': (('all', a, c), ('none', b, c)),
    }[form]


def evaluate(form, a, b, c):
    states = tuple(status(*p) for p in premises(form, a, b, c))
    conclusion = all_of(b, a) if form == 'Barbara' else none_of(b, a)
    return states, conclusion


def subsets(n, nonempty=False):
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 if nonempty else 0, 1 << n)]


def summarize(n=3):
    """All triples incl. empties for validity; nonempty terms for error taxonomy."""
    forms = ('Barbara', 'Celarent', 'Cesare', 'Camestres')
    out = {'universe_size': n, 'triples_including_empty': (2**n)**3,
           'nonempty_triples': (2**n-1)**3, 'forms': {}}
    for form in forms:
        invalid = 0
        for a, b, c in product(subsets(n), repeat=3):
            states, conclusion = evaluate(form, a, b, c)
            invalid += states == ('true', 'true') and not conclusion
        counts = {}
        witnesses = {}
        for a, b, c in product(subsets(n, True), repeat=3):
            # The true contrary is stronger than merely falsifying a universal.
            target = none_of(b, a) if form == 'Barbara' else all_of(b, a)
            if not target:
                continue
            states, conclusion = evaluate(form, a, b, c)
            if conclusion:
                raise RuntimeError('nonempty contrary should make conclusion false')
            key = ','.join(states)
            counts[key] = counts.get(key, 0) + 1
            witnesses.setdefault(key, {'A': sorted(a), 'B': sorted(b), 'C': sorted(c)})
        out['forms'][form] = {'soundness_counterexamples': invalid,
                             'false_conclusion_profiles': dict(sorted(counts.items())),
                             'witnesses': dict(sorted(witnesses.items()))}
    # This is a stated scenario restriction, NOT a computation of immediacy.
    out['barbara_minor_false_scenario_profiles'] = sorted(
        key for key in out['forms']['Barbara']['false_conclusion_profiles']
        if key.split(',')[1] != 'true')
    out['scope'] = ('Finite extension checks only; no scientific immediacy, '
                    'causal priority, or psychological belief is computed.')
    return out


if __name__ == '__main__':
    print(json.dumps(summarize(), ensure_ascii=False, indent=2, sort_keys=True))
