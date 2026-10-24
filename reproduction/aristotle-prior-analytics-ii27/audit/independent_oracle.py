"""Independent pointwise-truth oracle; never imports the production implementation."""
import argparse
import itertools
import json
from pathlib import Path

NAMES = ('first', 'second_affirmative', 'third_particular',
         'third_universal_overreach', 'third_missing_existence',
         'correlative_sign', 'one_way_sign_inverse')


def pointwise(a, b, c):
    ba = all(not y or x for x, y in zip(a, b))
    cb = all(not z or y for y, z in zip(b, c))
    ca = all(not z or x for x, z in zip(a, c))
    ab = all(not x or y for x, y in zip(a, b))
    overlap = any(x and y for x, y in zip(a, b))
    common = ca and cb
    return ((ba and cb, ca), (ba and ca, cb),
            (common and any(c), overlap), (common and any(c), ba),
            (common, overlap), (a == b and cb, ca), (ab and cb, ca))


def code(bits):
    return sum(int(v) * 2 ** i for i, v in enumerate(bits))


def oracle():
    totals = {k: {'premise_models': 0, 'countermodels': 0,
                 'first_countermodel': None,
                 'first_all_nonempty_countermodel': None} for k in NAMES}
    worlds = 0
    for n in range(5):
        vectors = sorted(itertools.product((False, True), repeat=n), key=code)
        for a, b, c in itertools.product(vectors, repeat=3):
            worlds += 1
            for key, (premise, result) in zip(NAMES, pointwise(a, b, c)):
                if not premise:
                    continue
                entry = totals[key]
                entry['premise_models'] += 1
                if result:
                    continue
                entry['countermodels'] += 1
                model = dict(n=n, A=code(a), B=code(b), C=code(c))
                if entry['first_countermodel'] is None:
                    entry['first_countermodel'] = model
                if all(map(any, (a, b, c))) and entry['first_all_nonempty_countermodel'] is None:
                    entry['first_all_nonempty_countermodel'] = model
    return {'worlds': worlds, 'max_n': 4, 'routes': totals}


def possible_pairings(rows):
    # Directly test the two possible bijections, with no production helper.
    direct = all(t0 == s0 and t1 == s1 for t0, t1, s0, s1 in rows)
    crossed = all(t0 == s1 and t1 == s0 for t0, t1, s0, s1 in rows)
    return ([ [0, 1] ] if direct else []) + ([ [1, 0] ] if crossed else [])


def validate(path):
    actual = json.loads(Path(path).read_text())
    expected = oracle()
    for field in ('worlds', 'max_n', 'routes'):
        if actual[field] != expected[field]:
            raise RuntimeError('Mismatch: ' + field)
    obs = actual['identification']
    prescribed = {'cooccurrence': [[True, True, True, True]],
                  'separated': [[True, True, True, True], [True, False, True, False]],
                  'extended': [[True, True, True, True], [True, False, True, False],
                               [True, False, False, True]]}
    if obs['rows'] != prescribed:
        raise RuntimeError('Observation rows differ from teaching specification')
    for label, rows in prescribed.items():
        if obs[label + '_mappings'] != possible_pairings(rows):
            raise RuntimeError('Mapping mismatch: ' + label)
    population = tuple(i < 9 for i in range(10))
    expected_majority = dict(population_size=10, successes=9, frequency='9/10',
                             strict_majority=sum(population)*2 > len(population),
                             universal=all(population), exception_index=9)
    if actual['majority'] != expected_majority:
        raise RuntimeError('Majority mismatch')
    return {'status': 'PASS', 'worlds_independently_enumerated': expected['worlds'],
            'route_evaluations_independently_recomputed': expected['worlds'] * 7,
            'comparison_scope': 'all route aggregate counts and first-countermodel fields; all identification and majority fields',
            'route_aggregate_fields_compared': 28, 'route_results': expected['routes']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result')
    args = parser.parse_args()
    print(json.dumps(validate(args.result), ensure_ascii=False, indent=2, sort_keys=True))
