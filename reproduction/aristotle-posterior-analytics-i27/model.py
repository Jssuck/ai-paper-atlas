"""Original finite teaching models, not a scientific-precision ranking."""
from fractions import Fraction
from itertools import product, permutations
import json


def scm(model, u, intervention=None):
    """Binary U, X=U naturally; intervention replaces the X equation only."""
    if model not in ('direct', 'common') or u not in (0, 1):
        raise ValueError('unknown model or nonbinary U')
    if intervention not in (None, 0, 1):
        raise ValueError('nonbinary intervention')
    x = u if intervention is None else intervention
    y = x if model == 'direct' else u
    return (x, y)


def causal_summary():
    observations = [scm('direct', u) for u in (0, 1)]
    comparison = [{'u': u, 'do_x': x, 'direct': list(scm('direct', u, x)),
                   'common': list(scm('common', u, x))}
                  for u, x in product((0, 1), repeat=2)]
    return {'natural_rows': [list(v) for v in observations],
            'natural_disagreements': sum(scm('direct', u) != scm('common', u) for u in (0, 1)),
            'intervention_rows': comparison,
            'intervention_disagreements': sum(r['direct'] != r['common'] for r in comparison)}


def forget_positions(positions):
    """Keep labelled-object identities 0..n-1; erase positions (collisions allowed)."""
    return tuple(range(len(positions)))


def first_distance(positions):
    if len(positions) < 2:
        raise ValueError('two labels needed')
    return abs(positions[0] - positions[1])


def position_summary():
    rows = []
    for n in range(1, 5):
        configurations = list(product(range(3), repeat=n))
        bases = {forget_positions(p) for p in configurations}
        distances = sorted({first_distance(p) for p in configurations}) if n >= 2 else []
        rows.append({'labels': n, 'configurations': len(configurations),
                     'base_fibers': len(bases), 'first_pair_distances': distances,
                     'distance_not_recoverable': len(distances) > 1})
    return {'rows': rows, 'configurations': sum(r['configurations'] for r in rows),
            'ambiguous_distance_fibers': sum(r['distance_not_recoverable'] for r in rows),
            'witness': {'first': [0, 0], 'second': [0, 1], 'base_labels': [0, 1],
                        'distances': [0, 1]}}


def closure(seed, rules):
    """Finite positive unary Horn rules; no negation or scientific truth labels."""
    reached = set(seed)
    while True:
        updated = reached | {b for a, b in rules if a in reached}
        if updated == reached:
            return reached
        reached = updated


def horn_summary():
    old = {'a', 'b'}
    base = closure({'a'}, [])
    candidates = list(permutations(('a', 'b', 'c'), 2))
    conservative = monotonic_violations = 0
    for bits in product((False, True), repeat=len(candidates)):
        rules = [r for r, take in zip(candidates, bits) if take]
        reached = closure({'a'}, rules)
        conservative += (reached & old) == base
        monotonic_violations += not base <= reached
    return {'rule_configurations': 2 ** len(candidates),
            'conservative_at_fixed_seed': conservative,
            'nonconservative_at_fixed_seed': 2 ** len(candidates) - conservative,
            'old_conclusion_loss_cases': monotonic_violations,
            'conservative_example': sorted(closure({'a'}, [('a', 'c')]) & old),
            'nonconservative_example': sorted(closure({'a'}, [('a', 'c'), ('c', 'b')]) & old)}


def prediction_summary():
    data = [(x, z, x + z) for x, z in product((0, 1), repeat=2)]
    simple = sum(Fraction((x-y)**2) for x, z, y in data) / len(data)
    richer = sum(Fraction((x+z-y)**2) for x, z, y in data) / len(data)
    return {'dataset': [list(r) for r in data], 'simple_mse': str(simple),
            'richer_mse': str(richer), 'claim': 'constructed example only; no real dataset'}


def results():
    return {'causal': causal_summary(), 'positions': position_summary(),
            'horn': horn_summary(), 'prediction': prediction_summary()}

if __name__ == '__main__':
    print(json.dumps(results(), ensure_ascii=False, indent=2))
