"""Original finite teaching models for Posterior Analytics I.31, not historical physics."""
from itertools import product
import json


def validate(n, observations):
    if type(n) is not int or not 0 <= n <= 12:
        raise ValueError('n must be an integer from 0 to 12 (enumeration safety limit)')
    rows = tuple(observations)
    for row in rows:
        if not isinstance(row, (tuple, list)) or len(row) != 2:
            raise ValueError('each observation must be (index, Boolean value)')
        i, v = row
        if type(i) is not int or not 0 <= i < n or type(v) is not bool:
            raise ValueError('invalid index or non-Boolean value')
    return rows


def compatible_models(n, observations):
    """All truth assignments on the declared finite universe satisfying every row."""
    rows = validate(n, observations)
    return tuple(h for h in product((False, True), repeat=n)
                 if all(h[i] == value for i, value in rows))


def report(n, observations):
    rows = validate(n, observations)
    models = compatible_models(n, rows)
    counter = next((h for h in models if not all(h)), None)
    # Empty model class is inconsistent, not empirical confirmation by vacuity.
    return {'n': n, 'observations': [list(r) for r in rows],
            'distinct_indices': len({i for i, _ in rows}),
            'compatible_count': len(models), 'consistent': bool(models),
            'universal_true_in_all_compatible_models': bool(models) and all(all(h) for h in models),
            'countermodel': None if counter is None else list(counter)}


def mechanism(name, x, z):
    """Two stipulated deterministic mechanisms. Neither is a discovered natural law."""
    if type(x) is not bool or type(z) is not bool:
        raise ValueError('x and z must be Boolean')
    if name == 'X':
        return x
    if name == 'Z':
        return z
    raise ValueError('unknown mechanism')


def experiment():
    cases = {
        'none': report(4, []),
        'partial_positive': report(4, [(0, True), (1, True)]),
        'repeated_positive': report(4, [(0, True), (1, True)] * 5),
        'full_positive': report(4, [(i, True) for i in range(4)]),
        'one_negative': report(4, [(0, False)]),
        'contradiction': report(4, [(0, True), (0, False)]),
        'empty_universe': report(0, [])}
    observed = [(False, False), (True, True)]
    causal = {'observed_inputs': [list(t) for t in observed],
              'outputs_X': [mechanism('X', *t) for t in observed],
              'outputs_Z': [mechanism('Z', *t) for t in observed],
              'stipulated_do_x_true_z_fixed_false': {'X': mechanism('X', True, False),
                                                    'Z': mechanism('Z', True, False)}}
    return {'scope': 'finite teaching reconstruction; no general physical or causal theorem established',
            'cases': cases, 'mechanism_comparison': causal}

if __name__ == '__main__':
    print(json.dumps(experiment(), ensure_ascii=False, indent=2))
