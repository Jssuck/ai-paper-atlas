"""Original finite teaching models for Posterior Analytics I.26, not an edition."""
from itertools import product
import json


def checked_sets(a, b, c):
    for value in (a, b, c):
        if not isinstance(value, (set, frozenset)):
            raise TypeError('terms must be sets or frozensets')
    return frozenset(a), frozenset(b), frozenset(c)


def all_of(predicate, subject):
    """All subject is predicate, with modern vacuous truth."""
    p, s, _ = checked_sets(predicate, subject, set())
    return s <= p


def none_of(predicate, subject):
    p, s, _ = checked_sets(predicate, subject, set())
    return not (p & s)


def certificate(a, b, c):
    """Separate premises, legitimate conclusion and tempting overstatement."""
    a, b, c = checked_sets(a, b, c)
    direct_premises = none_of(a, b) and all_of(b, c)
    reductio_background = none_of(a, c) and all_of(b, c) and bool(c)
    return {
        'direct_premises': direct_premises,
        'direct_conclusion': none_of(a, c),
        'direct_valid': not direct_premises or none_of(a, c),
        'reductio_background': reductio_background,
        'not_all_b_are_a': not all_of(a, b),
        'reductio_valid': not reductio_background or not all_of(a, b),
        'tempting_universal_negative': none_of(a, b),
        'empty_c_all_and_none': not c and all_of(a, c) and none_of(a, c),
    }


def witness_trace(a, b, c, w):
    """Read actual membership under fixed direct premises, no invented witness."""
    a, b, c = checked_sets(a, b, c)
    if not (none_of(a, b) and all_of(b, c)):
        raise ValueError('fixed direct premises do not hold')
    if w not in c:
        raise ValueError('candidate must be in C')
    return {'in_c': True, 'in_b': w in b, 'in_a': w in a,
            'intersection_witness': w in a and w in c}


def implication(p, q, r):
    for value in (p, q, r):
        if type(value) is not bool:
            raise TypeError('propositional values must be booleans')
    return not (p and q) or r


def background_models(q=None, r=None, p=None):
    """Classical truth-table models of a fixed rule; None is unknown, not false."""
    for value in (q, r, p):
        if value is not None and type(value) is not bool:
            raise TypeError('facts are bool or None')
    return [dict(p=x, q=y, r=z) for x, y, z in product((False, True), repeat=3)
            if implication(x, y, z)
            and (q is None or y == q) and (r is None or z == r)
            and (p is None or x == p)]


def diagnose(q=None, r=None, p=None):
    worlds = background_models(q=q, r=r, p=p)
    if not worlds:
        return {'status': 'inconsistent_background', 'model_count': 0,
                'not_p_supported': None}
    return {'status': 'consistent', 'model_count': len(worlds),
            'not_p_supported': all(not w['p'] for w in worlds)}


def subsets(n):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]


def run(max_n=4):
    if type(max_n) is not int or not 0 <= max_n <= 5:
        raise ValueError('bounded enumeration requires 0 <= max_n <= 5')
    rows = []
    for n in range(max_n + 1):
        row = dict(n=n, assignments=0, direct_premise_cases=0,
                   direct_counterexamples=0, reductio_background_cases=0,
                   reductio_counterexamples=0, overstrong_counterexamples=0,
                   empty_c_overlap_cases=0, witness_checks=0,
                   witness_violations=0)
        for a, b, c in product(subsets(n), repeat=3):
            v = certificate(a, b, c)
            row['assignments'] += 1
            row['direct_premise_cases'] += v['direct_premises']
            row['direct_counterexamples'] += not v['direct_valid']
            row['reductio_background_cases'] += v['reductio_background']
            row['reductio_counterexamples'] += not v['reductio_valid']
            row['overstrong_counterexamples'] += (v['reductio_background'] and
                                                  not v['tempting_universal_negative'])
            row['empty_c_overlap_cases'] += v['empty_c_all_and_none']
            if v['direct_premises']:
                for w in c:
                    trace = witness_trace(a, b, c, w)
                    row['witness_checks'] += 1
                    row['witness_violations'] += not trace['in_b'] or trace['in_a']
        rows.append(row)
    truth_rows = []
    for p, q, r in product((False, True), repeat=3):
        rule = implication(p, q, r)
        truth_rows.append(dict(p=p, q=q, r=r, rule=rule,
                              reductio_valid=not (rule and q and not r) or not p))
    return {'scope': 'finite extensional sets, n=0..max_n; classical propositional rule',
            'max_n': max_n, 'rows': rows,
            'totals': {key: sum(row[key] for row in rows) for key in rows[0] if key != 'n'},
            'truth_rows': truth_rows,
            'overstrong_example': {'universe': [0, 1], 'A': [1], 'B': [0, 1], 'C': [0],
                                   'certificate': certificate({1}, {0, 1}, {0})},
            'empty_example': {'A': [], 'B': [], 'C': [],
                              'certificate': certificate(set(), set(), set())},
            'fixed_q_negative_r': diagnose(q=True, r=False),
            'missing_q_negative_r': diagnose(r=False),
            'false_q_negative_r': diagnose(q=False, r=False),
            'inconsistent_fixed_background': diagnose(p=True, q=True, r=False)}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2) )
