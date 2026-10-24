#!/usr/bin/env python3
"""Independent element-wise oracle. No production module or bit-mask inclusion."""
import json
from itertools import combinations, product


def powerset(n):
    return [frozenset(xs) for k in range(n + 1) for xs in combinations(range(n), k)]


def contains(left, right):
    return all(x in right for x in left)


def run():
    names = ('full_induction', 'minimal_transfer', 'particular_from_nonempty',
             'forward_deduction', 'error_localization')
    rules = {k: {'premise_models': 0, 'violations': 0} for k in names}
    worlds = weak_total = weak_failures = pairs = classified_pairs = 0
    by_n = []
    for n in range(5):
        sets = powerset(n)
        local = 0
        for a, b, c in product(sets, repeat=3):
            worlds += 1
            local += 1
            observed = contains(c, a)
            classified = contains(c, b)
            covered = contains(b, c)
            universal = contains(b, a)
            overlap = any(x in a for x in b)
            failures = {x for x in b if x not in a}
            unobserved_failures = {x for x in b if x not in c and x not in a}
            claims = (
                (observed and classified and covered, universal),
                (observed and covered, universal),
                (observed and classified and len(c) > 0, overlap),
                (universal and classified, observed),
                (observed, failures == unobserved_failures),
            )
            for name, (premise, conclusion) in zip(names, claims):
                if premise:
                    rules[name]['premise_models'] += 1
                    rules[name]['violations'] += int(not conclusion)
            if observed and classified:
                weak_total += 1
                weak_failures += int(not universal)
        by_n.append({'n': n, 'worlds': local})
        for b, c in product(sets, repeat=2):
            bad_extensions = [a for a in sets if contains(c, a) and not contains(b, a)]
            if (len(bad_extensions) == 0) != contains(b, c):
                raise RuntimeError('Independent universal-quantification check failed')
            # Constructive necessity witness A=C whenever coverage fails.
            if not contains(b, c) and c not in bad_extensions:
                raise RuntimeError('Missing constructive witness A=C')
            pairs += 1
            classified_pairs += int(contains(c, b))
    # Third check: independent local-membership-pattern counting formulas.
    totals = {k: sum(k ** n for n in range(5)) for k in (3, 4, 5, 6, 8)}
    expected_counts = {'full_induction': totals[3], 'minimal_transfer': totals[4],
                       'particular_from_nonempty': totals[5] - totals[4],
                       'forward_deduction': totals[4], 'error_localization': totals[6]}
    if worlds != totals[8] or weak_total != totals[5] or weak_failures != totals[5] - totals[4]:
        raise RuntimeError('Closed-form world counts disagree')
    if any(rules[k]['premise_models'] != v for k, v in expected_counts.items()):
        raise RuntimeError('Closed-form premise counts disagree')
    if pairs != totals[4] or classified_pairs != totals[3]:
        raise RuntimeError('Closed-form pair counts disagree')
    if any(x['violations'] for x in rules.values()):
        raise RuntimeError('Independent rule failure')
    return {'worlds': worlds, 'by_n': by_n, 'rules': rules,
            'weak_observation_classification': {'models': weak_total, 'false_universal': weak_failures},
            'coverage_iff_forall_A': {'pairs': pairs, 'classified_pairs': classified_pairs, 'violations': 0}}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
