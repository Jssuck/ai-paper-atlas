"""Original finite teaching models for Posterior Analytics I.32, not a formalization."""
from itertools import combinations, product
import json
from pathlib import Path


def nonempty_subsets(n):
    if type(n) is not int or not 1 <= n <= 6:
        raise ValueError('n must be an integer in 1..6')
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1, 1 << n)]


def syllogism_counts(n):
    sets = nonempty_subsets(n)
    counts = {'triples': 0, 'both_premises_true': 0, 'false_conclusions': 0,
              'true_conclusion_both_premises_false': 0,
              'validity_violations': 0}
    for a, b, c in product(sets, repeat=3):
        p, q, r = b <= a, c <= b, c <= a
        counts['triples'] += 1
        counts['both_premises_true'] += p and q
        counts['false_conclusions'] += not r
        counts['true_conclusion_both_premises_false'] += r and not p and not q
        counts['validity_violations'] += p and q and not r
    return counts


def closure(facts, rules):
    """Least closure of finite positive Horn rules (body frozenset, head atom)."""
    known = set(facts)
    rules = tuple((frozenset(body), head) for body, head in rules)
    changed = True
    while changed:
        changed = False
        for body, head in rules:
            if body <= known and head not in known:
                known.add(head)
                changed = True
    return frozenset(known)


def minimal_supports(facts, rules, goal):
    """Inclusion-minimal subsets of the supplied facts, holding rules fixed."""
    facts, rules = sorted(set(facts)), tuple(rules)
    supports = []
    for size in range(len(facts) + 1):
        for candidate in combinations(facts, size):
            s = frozenset(candidate)
            if any(previous <= s for previous in supports):
                continue
            if goal in closure(s, rules):
                supports.append(s)
    return supports


def successor_prefix(depth):
    """Finite prefix for base 0 and schematic rule x -> S(x), not infinity in RAM."""
    if type(depth) is not int or not 0 <= depth <= 100:
        raise ValueError('depth must be an integer in 0..100')
    result = ['0']
    for _ in range(depth):
        result.append('S(' + result[-1] + ')')
    return result


def report():
    facts = {'geom:p', 'arith:r', 'unused:u'}
    rules = [(frozenset({'geom:p'}), 'geom:q'),
             (frozenset({'arith:r'}), 'arith:s')]
    bridge = rules + [(frozenset({'geom:q'}), 'arith:s')]
    return {
        'scope': 'Modern teaching reconstruction; finite checks, not an ancient experiment or a proof by enumeration of unrestricted theorems.',
        'nonempty_set_syllogisms': {str(n): syllogism_counts(n) for n in range(1, 5)},
        'two_false_premises_example': {'A': [0], 'B': [1], 'C': [0],
            'B_subset_A': False, 'C_subset_B': False, 'C_subset_A': True},
        'supports': {goal: [sorted(s) for s in minimal_supports(facts, rules, goal)]
                     for goal in ['geom:q', 'arith:s']},
        'rules_alone': sorted(closure([], rules)),
        'geometry_facts_only': sorted(closure(['geom:p'], rules)),
        'with_explicit_bridge': sorted(closure(['geom:p'], bridge)),
        'bridge_alternative_supports': [sorted(s) for s in minimal_supports(facts, bridge, 'arith:s')],
        'successor_prefix_depth_10': successor_prefix(10),
        'successor_scope': '11 finite terms shown. Infinitude requires the separate inductive argument and unrestricted term grammar, not this run.'
    }


if __name__ == '__main__':
    result = json.dumps(report(), ensure_ascii=False, indent=2) + '\n'
    Path(__file__).with_name('results.json').write_text(result, encoding='utf-8')
    print(result, end='')
