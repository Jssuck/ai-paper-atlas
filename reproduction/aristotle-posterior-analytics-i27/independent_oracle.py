"""Independent finite semantic audit; no assertion statements, standard library only."""
import json
from itertools import combinations, product
from fractions import Fraction
import model


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def semantic_closure(seed, rules):
    # Enumerate all truth valuations satisfying facts and material implications.
    valuations = []
    for bits in range(8):
        truth = {a for i, a in enumerate('abc') if bits & (1 << i)}
        if seed <= truth and all(a not in truth or b in truth for a, b in rules):
            valuations.append(truth)
    return set.intersection(*valuations)


def main():
    edges = [(a, b) for a in 'abc' for b in 'abc' if a != b]
    rulesets = [set(e for i, e in enumerate(edges) if mask & (1 << i)) for mask in range(64)]
    seeds = [{a for i, a in enumerate('abc') if mask & (1 << i)} for mask in range(8)]
    closures = {}
    for i, rules in enumerate(rulesets):
        for j, seed in enumerate(seeds):
            reference = semantic_closure(seed, rules)
            check(reference == model.closure(seed, rules), 'semantic closure mismatch')
            closures[i, j] = reference
    mono = 0
    for i, r in enumerate(rulesets):
        for k, s in enumerate(rulesets):
            if r <= s:
                for j in range(8):
                    check(closures[i, j] <= closures[k, j], 'rule monotonicity mismatch')
                    mono += 1
    conserved = sum((semantic_closure({'a'}, r) & {'a', 'b'}) == {'a'} for r in rulesets)
    check(conserved == 24, 'fixed-seed count mismatch')
    check(model.horn_summary()['conservative_at_fixed_seed'] == conserved, 'reported count mismatch')
    scm_cases = 0
    for kind in ('direct', 'common'):
        for u in (0, 1):
            for intervention in (None, 0, 1):
                # Constraint satisfaction, independently of sequential SCM evaluator.
                solutions = [(x, y) for x, y in product((0, 1), repeat=2)
                             if (x == u if intervention is None else x == intervention)
                             and (y == x if kind == 'direct' else y == u)]
                check(len(solutions) == 1 and model.scm(kind, u, intervention) == solutions[0], 'SCM mismatch')
                scm_cases += 1
    configurations = 0
    distance_cases = 0
    for n in range(1, 5):
        distances = set()
        for number in range(3**n):
            q = number
            coordinates = []
            for _ in range(n):
                coordinates.append(q % 3)
                q //= 3
            check(model.forget_positions(coordinates) == tuple(range(n)), 'forget mismatch')
            if n >= 2:
                d = max(coordinates[:2]) - min(coordinates[:2])
                check(model.first_distance(coordinates) == d, 'first-pair mismatch')
                distances.add(d)
                distance_cases += 1
            configurations += 1
        check(distances == (set() if n == 1 else {0, 1, 2}), 'fiber distances mismatch')
    # Distinguish first-pair distance from whole-configuration diameter.
    check(model.first_distance((0, 0, 2)) == 0, 'pair is not diameter')
    check(model.first_distance((0, 1)) != model.first_distance((0, 2)), 'noncollision witness')
    prediction = model.prediction_summary()
    reference_simple = Fraction(sum(z*z for z in (0, 1, 0, 1)), 4)
    check(prediction['simple_mse'] == str(reference_simple) and prediction['richer_mse'] == '0', 'MSE mismatch')
    return {'semantic_closure_cases': 512, 'rule_inclusion_monotonicity_cases': mono,
            'fixed_seed_conservative': conserved, 'fixed_seed_nonconservative': 64-conserved,
            'scm_constraint_cases': scm_cases, 'position_configurations': configurations,
            'first_pair_distance_cases': distance_cases,
            'pair_not_diameter_and_noncollision_witnesses': 'passed',
            'exact_mse': ['1/2', '0'], 'mismatches': 0,
            'scope': 'finite teaching models only; not a general scientific ranking or full-theory conservativity claim'}

if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
