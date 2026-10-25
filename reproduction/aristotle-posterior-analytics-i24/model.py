"""Finite teaching models for Posterior Analytics I.24, not causal certification."""
from itertools import product
import json


def subsets(n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError('n must be a nonnegative integer')
    return [frozenset(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]


def restriction_census(max_n=4):
    """Enumerate all S,G,P in universes of sizes 0..max_n, including empty S."""
    if not isinstance(max_n, int) or isinstance(max_n, bool) or not 0 <= max_n <= 6:
        raise ValueError('max_n must be an integer in 0..6')
    total = forward = violations = converse_counterexamples = nonempty_counterexamples = 0
    witness = None
    for n in range(max_n + 1):
        for s, g, p in product(subsets(n), repeat=3):
            total += 1
            if s <= g and g <= p:
                forward += 1
                violations += not s <= p
            if s <= g and s <= p and not g <= p:
                converse_counterexamples += 1
                nonempty_counterexamples += bool(s)
                if s and witness is None:
                    witness = {'universe_size': n, 'S': sorted(s), 'G': sorted(g), 'P': sorted(p)}
    return dict(assignments=total, forward_premise_cases=forward,
                forward_violations=violations, converse_counterexamples=converse_counterexamples,
                converse_nonempty_counterexamples=nonempty_counterexamples,
                first_nonempty_counterexample=witness)


def closure(facts, rules):
    """Positive propositional Horn closure. No implicit membership/causal rules."""
    known = set(facts)
    normalized = [(frozenset(premises), conclusion) for premises, conclusion in rules]
    # At most one addition per atom in the finite rule heads; cycles are harmless.
    while True:
        new = {head for body, head in normalized if body <= known} - known
        if not new:
            return frozenset(known)
        known.update(new)


def knowledge_example():
    universal = 'all_triangles_have_interior_sum_180'
    bridge = 'iso_is_triangle'
    target = 'all_iso_have_interior_sum_180'
    rule = [(frozenset((universal, bridge)), target)]
    explicit = frozenset((universal,))
    return {
        'explicit': sorted(explicit),
        'closure_without_bridge': sorted(closure(explicit, rule)),
        'closure_with_bridge': sorted(closure(explicit | {bridge}, rule)),
        'target_explicit_without_bridge': target in explicit,
        'target_derivable_without_bridge': target in closure(explicit, rule),
        'target_derivable_with_bridge': target in closure(explicit | {bridge}, rule),
        'scope': 'computable rule closure, not Aristotle potential knowledge or human awareness',
    }


def geometry_examples():
    """Exact integer formulas for planar convex Euclidean polygons; assumed theorem."""
    rows = [{'sides': n, 'interior_sum_degrees': (n - 2) * 180,
             'exterior_sum_degrees': n * 180 - (n - 2) * 180} for n in range(3, 9)]
    return {'assumptions': 'planar convex Euclidean polygon; one exterior angle at each vertex',
            'rows': rows, 'interior_180_sides': [r['sides'] for r in rows if r['interior_sum_degrees'] == 180],
            'all_exterior_360': all(r['exterior_sum_degrees'] == 360 for r in rows),
            'scope': 'arithmetic under an assumed geometric theorem; not its geometric proof'}


def homonym_example():
    # Public spelling does not identify a predicate; sense is part of the key.
    facts = {('crane', 'bird', 'has_feathers'), ('crane', 'machine', 'lifts_load')}
    return {'typed_machine_has_feathers': ('crane', 'machine', 'has_feathers') in facts,
            'collapsed_name_has_feathers': ('crane', 'has_feathers') in {(name, prop) for name, sense, prop in facts},
            'scope': 'collapsing senses can create spurious transfer; no claim about Greek examples'}


def extension_not_cause():
    # Two arbitrary labels have identical extensions, yet no explanatory annotations.
    extension = frozenset({'u', 'v'})
    predicates = {'label_A': extension, 'label_B': extension, 'property_P': extension}
    true_candidates = sorted(k for k in ('label_A', 'label_B') if predicates[k] <= predicates['property_P'])
    return {'true_candidates': true_candidates, 'equal_extensions': predicates['label_A'] == predicates['label_B'],
            'causal_status': 'undetermined', 'scope': 'truth and coextension alone carry no causal evidence'}


def run():
    return {'restriction': restriction_census(), 'knowledge': knowledge_example(),
            'geometry': geometry_examples(), 'homonym': homonym_example(),
            'extension': extension_not_cause()}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
