#!/usr/bin/env python3
"""Original finite teaching model for Prior Analytics II.23; not biology."""
import json
from itertools import product


def subset(left, right):
    """Bit-mask inclusion; callers enumerate masks in one fixed universe."""
    return (left & ~right) == 0


def members(mask, n):
    return [i for i in range(n) if mask & (1 << i)]


def require(condition, message):
    # Deliberately not assert: verification survives -O and -OO.
    if not condition:
        raise RuntimeError(message)


def countermodel(name, n, a, b, c):
    return dict(name=name, n=n, A=members(a, n), B=members(b, n),
                C=members(c, n), observations=subset(c, a),
                classification=subset(c, b), coverage=subset(b, c),
                universal=subset(b, a), particular=bool(a & b),
                missed_failures=members(b & ~a, n))


def experiment(max_n=4):
    if type(max_n) is not int or not 0 <= max_n <= 6:
        raise ValueError('max_n must be an integer from 0 through 6')
    names = ('full_induction', 'minimal_transfer', 'particular_from_nonempty',
             'forward_deduction', 'error_localization')
    rules = {name: dict(premise_models=0, violations=0) for name in names}
    worlds = 0
    by_n = []
    weak_total = weak_failures = 0
    coverage_pairs = coverage_with_classification = 0
    for n in range(max_n + 1):
        size = 1 << n
        local = 0
        for a, b, c in product(range(size), repeat=3):
            worlds += 1
            local += 1
            observed, classified, covered = subset(c, a), subset(c, b), subset(b, c)
            checks = {
                'full_induction': (observed and classified and covered, subset(b, a)),
                'minimal_transfer': (observed and covered, subset(b, a)),
                'particular_from_nonempty': (observed and classified and c != 0, bool(a & b)),
                'forward_deduction': (subset(b, a) and classified, subset(c, a)),
                # Once every C passes A, all B failures are outside C, exactly.
                'error_localization': (observed, (b & ~a) == ((b & ~c) & ~a)),
            }
            for name, (premise, conclusion) in checks.items():
                if premise:
                    rules[name]['premise_models'] += 1
                    if not conclusion:
                        rules[name]['violations'] += 1
            if observed and classified:
                weak_total += 1
                weak_failures += not subset(b, a)
        by_n.append(dict(n=n, worlds=local))
        # Separately quantify over every possible A for each fixed (B,C).
        for b, c in product(range(size), repeat=2):
            transfer_for_every_a = all(not subset(c, a) or subset(b, a) for a in range(size))
            require(transfer_for_every_a == subset(b, c), 'coverage iff universal transfer failed')
            coverage_pairs += 1
            coverage_with_classification += subset(c, b)
    for name, result in rules.items():
        require(result['violations'] == 0, name + ' violated')
    examples = [
        countermodel('missing_coverage_nonempty', 2, 1, 3, 1),
        countermodel('missing_observations', 1, 0, 1, 1),
        countermodel('empty_sample_no_existence', 1, 0, 1, 0),
        countermodel('classification_not_needed_for_minimal_transfer', 2, 3, 1, 3),
        countermodel('incomplete_but_accidentally_true', 2, 3, 3, 1),
        countermodel('complete_toy_enumeration', 3, 7, 7, 7),
    ]
    return dict(schema_version=1, scope='finite modern extensional teaching model; not historical biology',
                max_n=max_n, worlds=worlds, by_n=by_n, rules=rules,
                weak_observation_classification=dict(models=weak_total, false_universal=weak_failures),
                coverage_iff_forall_A=dict(pairs=coverage_pairs, classified_pairs=coverage_with_classification, violations=0),
                examples=examples)


if __name__ == '__main__':
    print(json.dumps(experiment(), ensure_ascii=False, indent=2, sort_keys=True))
