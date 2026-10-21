"""Deterministic finite checks. Failure raises even under python -O/-OO."""
import json
from itertools import product
from model import Model, TERMS, FORMS, MODALITIES, models, examples


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def endpoint_checks():
    family = {name: examples()[name] for name in ('disjoint', 'identical')}
    rows = []
    for major, minor in product(FORMS, repeat=2):
        for name, m in family.items():
            require(m.categorical('A', 'B', major, 'contingent'), 'major ' + name)
            require(m.categorical('A', 'C', minor, 'contingent'), 'minor ' + name)
        failures = {}
        for modality, conclusion in product(MODALITIES, FORMS):
            names = [name for name, m in family.items()
                     if not m.categorical('B', 'C', conclusion, modality)]
            require(bool(names), 'unrefuted endpoint conclusion')
            failures[modality + ':' + conclusion] = names
        rows.append({'premises': [major, minor], 'countermodels': failures})
    return rows


def exhaustive_checks():
    counts = dict(configurations=0, term_pairs=0, quality_equalities=0,
                  noncontingency_decompositions=0, modal_implications=0,
                  conversion_failures=0, empty_actual_subject_pairs=0)
    for n in (1, 2):
        for m in models(n):
            counts['configurations'] += 1
            for p, s in product(TERMS, repeat=2):
                counts['term_pairs'] += 1
                for first, second in (('A', 'E'), ('I', 'O')):
                    require(m.categorical(p, s, first, 'contingent') ==
                            m.categorical(p, s, second, 'contingent'), 'quality identity')
                    counts['quality_equalities'] += 1
                w = m.noncontingency_witnesses(p, s)
                fixed = bool(w['necessary_positive'] or w['necessary_negative'])
                require((not m.categorical(p, s, 'A', 'contingent')) == fixed,
                        'noncontingency disjunction')
                counts['noncontingency_decompositions'] += 1
                for form in FORMS:
                    values = {mode: m.categorical(p, s, form, mode) for mode in MODALITIES}
                    for antecedent, consequent in (('necessary', 'actual'),
                                                   ('actual', 'possible'),
                                                   ('contingent', 'possible')):
                        require(not values[antecedent] or values[consequent], 'modal implication')
                        counts['modal_implications'] += 1
                if m.categorical(p, s, 'E', 'contingent') and not m.categorical(s, p, 'E', 'contingent'):
                    counts['conversion_failures'] += 1
                if not m.extension(s):
                    counts['empty_actual_subject_pairs'] += 1
    return counts


def run():
    ex = examples()
    require(ex['conversion_failure'].categorical('A', 'B', 'E', 'contingent'), 'conversion premise')
    require(not ex['conversion_failure'].categorical('B', 'A', 'E', 'contingent'), 'conversion counterexample')
    branches = {}
    for name in ('necessary_positive', 'necessary_negative', 'mixed_fixed'):
        m = ex[name]
        require(not m.categorical('A', 'B', 'A', 'contingent'), 'noncontingency example')
        branches[name] = m.noncontingency_witnesses('A', 'B')
    alt = ex['alternating_witnesses']
    require(alt.categorical('A', 'B', 'A', 'contingent'), 'objectwise contingency')
    require(not alt.jointly_possible('A', 'B'), 'not jointly all positive')
    require(not alt.jointly_possible('A', 'B', False), 'not jointly all negative')
    return {'scope': 'finite modern actual-subject semantics; no proof of ancient general theory',
            'examples': {name: m.as_dict() for name, m in ex.items()},
            'noncontingency_branches': branches, 'endpoint_matrix': endpoint_checks(),
            'exhaustive': exhaustive_checks()}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
