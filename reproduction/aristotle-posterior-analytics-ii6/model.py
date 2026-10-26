"""Modern finite teaching models for Posterior Analytics II.6, not essence discovery."""
from itertools import product


def conjunction_report(subject, left, right, unity_claim=False):
    """unity_claim is supplied metadata; no set operation certifies it."""
    if type(unity_claim) is not bool:
        raise TypeError('unity_claim must be bool')
    h, p, q = map(frozenset, (subject, left, right))
    return {'both_predicated': h <= p and h <= q,
            'intersection_contains_subject': h <= p & q,
            'coextensive': h == p & q,
            'unity_claim_supplied': unity_claim,
            'unity_certified_by_sets': False}


def minimal_supports(facts, rules):
    """Least ground definite-Horn closure with inclusion-minimal fact supports.

    rules: iterable of (iterable-of-premise-atoms, conclusion-atom).
    Empty premise rules count as explicit axioms, with empty fact support.
    Rules are assumed, not validated as scientific truths. Atom strings are exact.
    """
    facts = frozenset(facts)
    rules = [(frozenset(ps), c) for ps, c in rules]
    atoms = set(facts)
    for ps, c in rules:
        atoms.update(ps)
        atoms.add(c)
    if any(not isinstance(a, str) or not a for a in atoms):
        raise ValueError('atoms must be nonempty strings')
    supports = {a: set() for a in atoms}
    for a in facts:
        supports[a].add(frozenset([a]))
    changed = True
    while changed:
        changed = False
        for ps, c in rules:
            choices = [tuple(supports[a]) for a in sorted(ps)]
            for combo in product(*choices):
                s = frozenset().union(*combo)
                if any(old <= s for old in supports[c]):
                    continue
                supports[c] = {old for old in supports[c] if not s < old}
                supports[c].add(s)
                changed = True
    return supports


def independent_support(supports, target, forbidden_facts):
    """Existence of a recorded support avoiding an explicit forbidden set.

    Include aliases manually. This does not detect hidden equivalence, assumptions
    encoded in rules, semantic circularity, or all forms of begging the question.
    """
    banned = frozenset(forbidden_facts)
    return any(s.isdisjoint(banned) for s in supports.get(target, set()))


def opposite_transfer(source_definition, subject_contrary, formula_contrary, bridge):
    """Apply a stipulated four-premise rule, not a theorem about all contraries."""
    values = (source_definition, subject_contrary, formula_contrary, bridge)
    if any(type(x) is not bool for x in values):
        raise TypeError('all premises must be bool')
    return all(values)
