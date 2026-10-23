"""Original finite-type teaching model for Prior Analytics II.4. Stdlib only."""
from itertools import combinations
from collections import Counter
import hashlib
import json

TERMS = {'A': 4, 'B': 2, 'C': 1}
MODES = {
    'Darapti': ('A', 'A', 'I', True),
    'Felapton': ('E', 'A', 'O', True),
    'Disamis': ('I', 'A', 'I', False),
    'Datisi': ('A', 'I', 'I', False),
    'Bocardo': ('O', 'A', 'O', False),
    'Ferison': ('E', 'I', 'O', False),
}

def validate(model):
    """Accept a nonempty iterable of distinct integer types 0..7; return tuple."""
    try:
        data = tuple(model)
    except TypeError as exc:
        raise ValueError('model must be iterable') from exc
    if not data or any(type(t) is not int or not 0 <= t <= 7 for t in data):
        raise ValueError('nonempty model of integer types 0..7 required')
    if len(set(data)) != len(data):
        raise ValueError('duplicate types not allowed in compressed model')
    return data

def members(model, term):
    data = validate(model)
    if not isinstance(term, str) or term not in TERMS:
        raise ValueError('unknown term')
    return frozenset(t for t in data if t & TERMS[term])

def proposition(model, kind, predicate, subject):
    """Predicate first: A(X,Y) means every Y is X. Empty universal is true."""
    data = validate(model)
    if (not isinstance(kind, str) or kind not in ('A', 'E', 'I', 'O')
            or not isinstance(predicate, str) or predicate not in TERMS
            or not isinstance(subject, str) or subject not in TERMS):
        raise ValueError('invalid proposition')
    x, y = members(data, predicate), members(data, subject)
    return {'A': y <= x, 'E': not bool(x & y), 'I': bool(x & y), 'O': bool(y - x)}[kind]

def classify(model, kind, predicate, subject):
    data = validate(model)
    truth = proposition(data, kind, predicate, subject)
    if kind in ('I', 'O'):
        return 'true' if truth else 'false'
    x, y = members(data, predicate), members(data, subject)
    if not y:
        return 'vacuous_true'
    if truth:
        return 'true'
    opposite = not bool(x & y) if kind == 'A' else y <= x
    return 'wholly_false' if opposite else 'partly_false'

def evaluate(model, mode):
    data = validate(model)
    if not isinstance(mode, str) or mode not in MODES:
        raise ValueError('unknown mode')
    major, minor, conclusion, requires_c = MODES[mode]
    return {
        'premises': [proposition(data, major, 'A', 'C'), proposition(data, minor, 'B', 'C')],
        'classes': [classify(data, major, 'A', 'C'), classify(data, minor, 'B', 'C')],
        'conclusion': proposition(data, conclusion, 'A', 'B'),
        'eligible': not requires_c or bool(members(data, 'C')),
    }

def models():
    for n in range(1, 9):
        yield from combinations(range(8), n)

def implication(p, q):
    if type(p) is not bool or type(q) is not bool:
        raise ValueError('Boolean arguments required')
    return not p or q

def ending_table():
    return [{'P': p, 'Q': q, 'P_implies_Q': implication(p, q),
             'notP_implies_Q': implication(not p, q),
             'both': implication(p, q) and implication(not p, q)}
            for p in (False, True) for q in (False, True)]

def survey():
    report = {'semantics': 'A=4,B=2,C=1; predicate first; nonempty domain',
              'all_models': 0, 'all_terms_nonempty_models': 0, 'modes': {},
              'ending_truth_table': ending_table()}
    for mode in MODES:
        counts = Counter()
        witnesses = {}
        raw_violations = eligible_violations = eligible_count = 0
        nonempty_true_classes = set()
        for m in models():
            e = evaluate(m, mode)
            key = '|'.join(e['classes'] + [str(e['conclusion']).lower()])
            counts[key] += 1
            witnesses.setdefault(key, list(m))
            violation = all(e['premises']) and not e['conclusion']
            raw_violations += violation
            eligible_count += e['eligible']
            eligible_violations += e['eligible'] and violation
            if all(members(m,t) for t in TERMS) and e['conclusion']:
                nonempty_true_classes.add('|'.join(e['classes']))
        report['modes'][mode] = {
            'evaluations': 255, 'eligible_models': eligible_count,
            'raw_violations_without_existence_condition': raw_violations,
            'eligible_soundness_violations': eligible_violations,
            'all_terms_nonempty_true_conclusion_class_pairs': sorted(nonempty_true_classes),
            'counts': dict(sorted(counts.items())), 'minimum_witnesses': dict(sorted(witnesses.items()))}
    report['all_models'] = sum(1 for _ in models())
    report['all_terms_nonempty_models'] = sum(all(members(m,t) for t in TERMS) for m in models())
    return report

if __name__ == '__main__':
    report = survey()
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    with open('witnesses.json', 'w', encoding='utf-8') as f:
        f.write(payload)
    print('models:', report['all_models'])
    print('all_terms_nonempty_models:', report['all_terms_nonempty_models'])
    print('six_mode_evaluations:', report['all_models'] * len(MODES))
    print('nonempty_term_six_mode_evaluations:', report['all_terms_nonempty_models'] * len(MODES))
    for mode, r in report['modes'].items():
        print(mode, 'eligible=', r['eligible_models'], 'raw_violations=', r['raw_violations_without_existence_condition'],
              'eligible_violations=', r['eligible_soundness_violations'],
              'true_conclusion_class_pairs=', len(r['all_terms_nonempty_true_conclusion_class_pairs']))
    print('ending_both_equivalent_Q:', all(r['both'] == r['Q'] for r in ending_table()))
    print('witnesses_sha256:', hashlib.sha256(payload.encode()).hexdigest())
