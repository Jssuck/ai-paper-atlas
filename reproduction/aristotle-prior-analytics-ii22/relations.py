"""Original finite teaching reconstruction of Prior Analytics II.22.

Sets describe extensions, not Aristotle's own formal language. Preferences
are a separate, expressly modern numerical model. No external dependencies.
"""
from itertools import product
import json

RULES = ('chain', 'negative_conversion', 'negative_transfer',
         'partition_transport', 'complement_pair', 'only_coverage',
         'middle_transfer')


def partition(x, y, universe):
    return x.isdisjoint(y) and x | y == universe


def evaluate(a, b, c, d, universe):
    """Return (premises, conclusion) for each named reconstructed rule."""
    if any(not isinstance(s, frozenset) for s in (a, b, c, d, universe)):
        raise TypeError('sets and universe must be frozensets')
    if any(not s <= universe for s in (a, b, c, d)):
        raise ValueError('term outside universe')
    return {
        'chain': (c <= b and b <= a and a <= c, a == b == c),
        'negative_conversion': (
            c <= b and a.isdisjoint(b),
            a.isdisjoint(c) and b.isdisjoint(a) and c.isdisjoint(a)),
        'negative_transfer': (
            b == c and a.isdisjoint(c),
            b.isdisjoint(a)),
        'partition_transport': (
            a == b and c == d and partition(a, c, universe),
            partition(b, d, universe)),
        'complement_pair': (
            partition(a, b, universe) and partition(c, d, universe)
            and a == c, b == d),
        'only_coverage': (
            b | c <= a and a <= b | c and c <= b, a == b),
        'middle_transfer': (c <= a and c <= b and b <= c, b <= a),
    }


def worlds(n):
    """All four labelled extensions on {0,...,n-1}; empty terms permitted."""
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    subsets = [frozenset(i for i in range(n) if mask & (1 << i))
               for mask in range(1 << n)]
    yield from product(subsets, repeat=4)


def census(n):
    universe = frozenset(range(n))
    counts = {name: {'premise_models': 0, 'violations': 0} for name in RULES}
    total = 0
    for a, b, c, d in worlds(n):
        total += 1
        for name, (premise, conclusion) in evaluate(a, b, c, d, universe).items():
            counts[name]['premise_models'] += int(premise)
            counts[name]['violations'] += int(premise and not conclusion)
    return {'n': n, 'worlds': total, 'rules': counts}


def preference(a, b, c, d):
    """Modern additive comparator, not a claim of ancient cardinal utility."""
    return a > b and d > c and a + c > b + d, a > d


def preference_census():
    total = models = failures = 0
    witness = None
    for values in product(range(-3, 4), repeat=4):
        total += 1
        premise, conclusion = preference(*values)
        if premise:
            models += 1
            if not conclusion:
                failures += 1
                if witness is None:
                    witness = values
    symmetric_models = symmetric_failures = 0
    for a, d in product(range(1, 6), repeat=2):
        premise, conclusion = preference(a, -a, -d, d)
        symmetric_models += int(premise)
        symmetric_failures += int(premise and not conclusion)
    return {'unrestricted': {'assignments': total, 'premise_models': models,
                            'violations': failures, 'first_counterexample': witness},
            'symmetric_positive': {'assignments': 25,
                                   'premise_models': symmetric_models,
                                   'violations': symmetric_failures}}


def main():
    print(json.dumps({'scope': 'finite modern reconstruction, not a general proof',
                      'sets': [census(n) for n in (1, 2, 3)],
                      'preferences': preference_census()},
                     ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
