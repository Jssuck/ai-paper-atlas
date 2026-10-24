"""Original finite teaching model of II.27; not empirical character inference."""
import argparse
import itertools
import json
from fractions import Fraction


def subset(x, y):
    return (x & ~y) == 0


def evaluate(a, b, c):
    """Return premise/conclusion booleans. A/B/C are sets as nonnegative masks."""
    if any(type(x) is not int or x < 0 for x in (a, b, c)):
        raise ValueError('sets must be nonnegative integer masks')
    common = subset(c, a) and subset(c, b)
    return {
        'first': (subset(b, a) and subset(c, b), subset(c, a)),
        'second_affirmative': (subset(b, a) and subset(c, a), subset(c, b)),
        'third_particular': (common and c != 0, bool(a & b)),
        'third_universal_overreach': (common and c != 0, subset(b, a)),
        'third_missing_existence': (common, bool(a & b)),
        'correlative_sign': (a == b and subset(c, b), subset(c, a)),
        'one_way_sign_inverse': (subset(a, b) and subset(c, b), subset(c, a)),
    }


def mappings(rows):
    """Two traits T0,T1 and signs S0,S1; assume a bijection and exact iff.

    Rows contain four booleans. Returned permutations only fit observed rows;
    they do NOT establish a rule for unseen objects.
    """
    rows = tuple(tuple(row) for row in rows)
    if any(len(row) != 4 or any(type(x) is not bool for x in row) for row in rows):
        raise ValueError('each row must contain four booleans')
    return [list(p) for p in itertools.permutations(range(2))
            if all(row[t] == row[2 + p[t]] for row in rows for t in range(2))]


def majority_example():
    # Explicit modern teaching threshold, not Aristotle's numerical definition.
    population = [True] * 9 + [False]
    frequency = Fraction(sum(population), len(population))
    return {'population_size': len(population), 'successes': sum(population),
            'frequency': str(frequency), 'strict_majority': frequency > Fraction(1, 2),
            'universal': all(population), 'exception_index': population.index(False)}


def identification_example():
    cooccurs = [(True, True, True, True)]
    separates = cooccurs + [(True, False, True, False)]
    # An unobserved object destroys the inferred identity mapping.
    extended = separates + [(True, False, False, True)]
    return {'cooccurrence_mappings': mappings(cooccurs),
            'separated_mappings': mappings(separates),
            'extended_mappings': mappings(extended),
            'rows': {'cooccurrence': cooccurs, 'separated': separates, 'extended': extended}}


def enumerate_models(max_n):
    if type(max_n) is not int or not 0 <= max_n <= 6:
        raise ValueError('max_n must be an integer from 0 to 6')
    totals = {key: {'premise_models': 0, 'countermodels': 0,
                    'first_countermodel': None, 'first_all_nonempty_countermodel': None}
              for key in evaluate(0, 0, 0)}
    worlds = 0
    for n in range(max_n + 1):
        for a, b, c in itertools.product(range(1 << n), repeat=3):
            worlds += 1
            for key, (premise, conclusion) in evaluate(a, b, c).items():
                entry = totals[key]
                if premise:
                    entry['premise_models'] += 1
                    if not conclusion:
                        entry['countermodels'] += 1
                        model = {'n': n, 'A': a, 'B': b, 'C': c}
                        if entry['first_countermodel'] is None:
                            entry['first_countermodel'] = model
                        if a and b and c and entry['first_all_nonempty_countermodel'] is None:
                            entry['first_all_nonempty_countermodel'] = model
    return {'max_n': max_n, 'worlds': worlds, 'routes': totals,
            'majority': majority_example(), 'identification': identification_example()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(enumerate_models(args.max_n), indent=2, sort_keys=True))
