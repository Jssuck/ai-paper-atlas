"""Finite teaching model: assumptions support derivations, not their own truth."""
from itertools import combinations, product
import json


def powerset(items):
    items = tuple(items)
    return tuple(frozenset(c) for size in range(len(items)+1)
                 for c in combinations(items, size))


def validate(atoms, base, rules):
    if not base <= atoms:
        raise ValueError('base outside language')
    for body, head in rules:
        if not body or not body <= atoms or head not in atoms:
            raise ValueError('rules need a nonempty in-language body and head')


def derive(atoms, base, rules):
    """Return least closure and an ordered certificate of (rule index, head)."""
    atoms, base = frozenset(atoms), frozenset(base)
    validate(atoms, base, rules)
    known = set(base)
    certificate = []
    changed = True
    while changed:
        changed = False
        for i, (body, head) in enumerate(rules):
            if body <= known and head not in known:
                known.add(head)
                certificate.append((i, head))
                changed = True
    return frozenset(known), tuple(certificate)


def check_certificate(atoms, base, rules, certificate, target):
    """Validate a finite derivation only; no reality/causality certification."""
    atoms, base = frozenset(atoms), frozenset(base)
    validate(atoms, base, rules)
    if target not in atoms:
        return False
    known = set(base)
    for index, head in certificate:
        if type(index) is not int or index < 0 or index >= len(rules):
            return False
        body, expected = rules[index]
        if head != expected or not body <= known or head in known:
            return False
        known.add(head)
    return target in known


def semantic_consequences(atoms, base, rules):
    """Independent oracle: intersect every truth assignment satisfying premises."""
    atoms, base = frozenset(atoms), frozenset(base)
    validate(atoms, base, rules)
    models = [v for v in powerset(sorted(atoms))
              if base <= v and all(not body <= v or head in v for body, head in rules)]
    # The all-true assignment always satisfies this positive fragment.
    return frozenset.intersection(*models)


def definition_case(domain, unit, description):
    """Extensional equality and witness existence, not an arithmetic definition."""
    if not unit <= domain or not description <= domain:
        raise ValueError('extension outside domain')
    return {'same_extension': unit == description,
            'unit_exists': bool(unit), 'description_exists': bool(description)}


def experiment():
    atoms = frozenset('abc')
    available = tuple((body, h) for h in sorted(atoms)
                      for body in powerset(sorted(atoms-{h})) if body)
    systems = instances = mismatches = invalid_certificates = empty_base_derived = 0
    for choices in product((False, True), repeat=len(available)):
        rules = tuple(r for r, selected in zip(available, choices) if selected)
        systems += 1
        for base in powerset(sorted(atoms)):
            instances += 1
            closure, certificate = derive(atoms, base, rules)
            mismatches += closure != semantic_consequences(atoms, base, rules)
            empty_base_derived += not base and bool(closure)
            for target in closure:
                invalid_certificates += not check_certificate(atoms, base, rules, certificate, target)
    pairs = equal = equal_empty = equal_nonempty = 0
    for n in range(5):
        domain = frozenset(range(n))
        for u, d in product(powerset(range(n)), repeat=2):
            c = definition_case(domain, u, d)
            pairs += 1
            if c['same_extension']:
                equal += 1
                equal_nonempty += c['unit_exists']
                equal_empty += not c['unit_exists']
    if mismatches or invalid_certificates or empty_base_derived:
        raise RuntimeError('independent verification failed')
    return {'rule_count': len(available), 'systems': systems, 'base_system_instances': instances,
            'semantic_mismatches': mismatches, 'invalid_certificates': invalid_certificates,
            'empty_base_nonempty_closures': empty_base_derived,
            'extension_pairs': pairs, 'equal_pairs': equal,
            'equal_empty_pairs': equal_empty, 'equal_nonempty_pairs': equal_nonempty}


if __name__ == '__main__':
    print(json.dumps(experiment(), indent=2))
