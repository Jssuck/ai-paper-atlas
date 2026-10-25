"""Independent review oracle: zero, one, or two arbitrary positive Horn rules."""
from itertools import combinations, product
import json
from model import closure, minimal_supports


def powerset(items):
    return [frozenset(s) for k in range(len(items) + 1)
            for s in combinations(items, k)]


def entailed_by_models(atoms, facts, rules):
    models = []
    for bits in product([0, 1], repeat=len(atoms)):
        true = {a for a, bit in zip(atoms, bits) if bit}
        if not facts <= true:
            continue
        if all(not body <= true or head in true for body, head in rules):
            models.append(true)
    if not models:
        raise RuntimeError('Positive Horn rules must admit the all-true model')
    return frozenset.intersection(*(frozenset(m) for m in models))


def main():
    atoms = ['a', 'b', 'c']
    subsets = powerset(atoms)
    candidate_rules = [(body, head) for body in subsets for head in atoms]
    rule_sets = [r for k in range(3) for r in combinations(candidate_rules, k)]
    closures_checked = supports_checked = 0
    for rules in rule_sets:
        semantic = {facts: entailed_by_models(atoms, facts, rules) for facts in subsets}
        for facts in subsets:
            if closure(facts, rules) != semantic[facts]:
                raise RuntimeError('Closure disagrees with independent assignments')
            closures_checked += 1
            for goal in atoms:
                sufficient = [s for s in subsets if s <= facts and goal in semantic[s]]
                expected = {s for s in sufficient if not any(t < s for t in sufficient)}
                if set(minimal_supports(facts, rules, goal)) != expected:
                    raise RuntimeError('Minimal supports disagree with semantic oracle')
                supports_checked += 1
    print(json.dumps({'candidate_rules': len(candidate_rules), 'rule_sets': len(rule_sets),
                      'closures_checked': closures_checked,
                      'supports_checked': supports_checked, 'mismatches': 0,
                      'scope': 'Three atoms; all zero/one/two-rule subsets, including empty and conjunctive bodies and self-loops. Not all arbitrary-size Horn systems.'}, indent=2))


if __name__ == '__main__':
    main()
