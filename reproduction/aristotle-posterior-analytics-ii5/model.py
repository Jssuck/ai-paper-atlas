"""Finite teaching models for Posterior Analytics II.5; no essence oracle."""
from itertools import product


def subsets(n):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    return [frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]


def division(parent, left, right):
    """Extensional coverage and disjointness are separate conditions."""
    return {'within': left <= parent and right <= parent,
            'covers': left | right == parent,
            'disjoint': not bool(left & right)}


def elimination(h, parent, left, right):
    """Check a certificate, not an unprovided membership premise."""
    checks = division(parent, left, right)
    premises = checks['covers'] and h <= parent and not bool(h & right)
    return {'premises': premises, 'conclusion': h <= left,
            'violation': premises and not h <= left}


def check_path(h, root, steps):
    """Steps: (left, right, choice, provenance); provenance is only a label.

    Accepted provenance labels distinguish an assumption, observation, or supplied
    proof. No label verifies scientific knowledge or the reliability of its source.
    """
    current = root
    records = []
    for left, right, choice, provenance in steps:
        if choice not in ('left', 'right'):
            raise ValueError('choice must be left or right')
        if provenance not in ('assumption', 'observation', 'supplied_proof'):
            raise ValueError('unsupported provenance label')
        selected = left if choice == 'left' else right
        d = division(current, left, right)
        records.append({**d, 'target_in_parent': h <= current,
                        'target_in_selected': h <= selected,
                        'choice': choice, 'provenance': provenance})
        current = selected
    return {'steps': records, 'endpoint': sorted(current),
            'extensional_certificate': h <= root and all(
                r['within'] and r['covers'] and r['disjoint'] and
                r['target_in_parent'] and r['target_in_selected'] for r in records),
            'essence_certified': False}


def conjunction(universe, predicates):
    result = frozenset(universe)
    for predicate in predicates:
        if not predicate <= universe:
            raise ValueError('predicate outside universe')
        result &= predicate
    return result


def relative_atom(cell, vocabulary):
    """No supplied predicate properly splits a NONEMPTY cell; vocabulary-relative."""
    return bool(cell) and all(not (cell & p) or cell <= p for p in vocabulary)


def enumerate_models(max_n=3):
    if type(max_n) is not int or not 0 <= max_n <= 4:
        raise ValueError('max_n must be an integer from 0 through 4')
    counts = dict(models=0, partitions_with_target=0, selection_failures=0,
                  elimination_cases=0, elimination_violations=0, oracle_mismatches=0,
                  empty_target_models=0)
    for n in range(max_n + 1):
        universe = set(range(n))
        for h, parent, left, right in product(subsets(n), repeat=4):
            counts['models'] += 1
            counts['empty_target_models'] += not bool(h)
            d = division(parent, left, right)
            if d['covers'] and d['disjoint'] and h <= parent:
                counts['partitions_with_target'] += 1
                counts['selection_failures'] += not h <= left
            e = elimination(h, parent, left, right)
            # Independent pointwise boolean oracle, not set-subset operations.
            cover_oracle = all((i in parent) == (i in left or i in right) for i in universe)
            premise_oracle = cover_oracle and all(not (i in h) or i in parent for i in universe) and all(not (i in h and i in right) for i in universe)
            conclusion_oracle = all(not (i in h) or i in left for i in universe)
            counts['oracle_mismatches'] += e['premises'] != premise_oracle or e['conclusion'] != conclusion_oracle
            counts['elimination_cases'] += e['premises']
            counts['elimination_violations'] += e['violation']
    return {'max_n': max_n, **counts}


def examples():
    u = frozenset(range(4)); h = frozenset({0}); l = frozenset({0, 1}); r = frozenset({2, 3})
    missing_target = elimination(frozenset({2}), u, l, r)
    gap = elimination(frozenset({1}), frozenset({0, 1}), frozenset({0}), frozenset())
    path = check_path(h, u, [(l, r, 'left', 'observation'),
                            (h, frozenset({1}), 'left', 'assumption')])
    predicates = [frozenset({0, 1, 2}), frozenset({0, 1}), frozenset({0, 2})]
    full = conjunction(u, predicates)
    return {'partition_without_selection': missing_target,
            'coverage_gap': gap, 'path': path,
            'formula_full': sorted(full),
            'omit_last': sorted(conjunction(u, predicates[:-1])),
            'skip_middle': sorted(conjunction(u, [predicates[0], predicates[2]])),
            'redundant_addition_same_extension': conjunction(u, predicates + [frozenset({0, 3})]) == full,
            'relative_atom_before_new_predicate': relative_atom(l, [u, l]),
            'relative_atom_after_new_predicate': relative_atom(l, [u, l, h])}
