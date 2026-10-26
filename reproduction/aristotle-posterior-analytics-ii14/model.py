"""Finite teaching reconstruction, not a detector of essence or real causes."""
from itertools import product
import json


def inheritance(subject, middle, attribute):
    """Check both premises separately; vacuous truth is not existence."""
    d, a, b = map(frozenset, (subject, middle, attribute))
    return {'subject_in_middle': d <= a, 'middle_in_attribute': a <= b,
            'premises': d <= a and a <= b, 'conclusion': d <= b,
            'subject_nonempty': bool(d)}


def taxonomy_path(classes, path, attribute):
    """Path is leaf-to-root. Every supplied edge gets an extensional check."""
    path = tuple(path)
    if not path:
        raise ValueError('empty path')
    if len(set(path)) != len(path):
        raise ValueError('repeated path node')
    if any(name not in classes for name in path):
        raise ValueError('unknown class')
    ext = [frozenset(classes[name]) for name in path]
    b = frozenset(attribute)
    edges = [left <= right for left, right in zip(ext, ext[1:])]
    return {'edges': edges, 'root_attribute': ext[-1] <= b,
            'certificate': all(edges) and ext[-1] <= b,
            'leaf_attribute': ext[0] <= b, 'leaf_nonempty': bool(ext[0])}


def observation(sample, proposed_class, attribute):
    """A finite sample is not a claim that it covers all real instances."""
    sample, proposed_class, attribute = map(frozenset, (sample, proposed_class, attribute))
    if not sample <= proposed_class:
        raise ValueError('sample outside proposed class')
    return {'sample_positive': sample <= attribute,
            'sample_covers_class': sample == proposed_class,
            'class_positive': proposed_class <= attribute,
            'counterexamples': sorted(proposed_class - attribute)}


def relation_map(source_domain, target_domain, source_edges, target_edges, mapping):
    """Check total, explicitly supplied relation-preserving map; not all predicates."""
    source, target = frozenset(source_domain), frozenset(target_domain)
    sr, tr = frozenset(source_edges), frozenset(target_edges)
    if set(mapping) != source or not set(mapping.values()) <= target:
        raise ValueError('map must be total with target values')
    if any(len(e) != 2 or e[0] not in source or e[1] not in source for e in sr):
        raise ValueError('source edge outside domain')
    if any(len(e) != 2 or e[0] not in target or e[1] not in target for e in tr):
        raise ValueError('target edge outside domain')
    failures = sorted((u, v) for u, v in sr if (mapping[u], mapping[v]) not in tr)
    return {'preserves_relation': not failures, 'failed_source_edges': failures,
            'injective': len(set(mapping.values())) == len(mapping)}


def subsets(n):
    return [frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]


def experiments():
    triples = valid = empty_valid = violations = oracle_disagreements = 0
    for n in range(5):
        for d, a, b in product(subsets(n), repeat=3):
            triples += 1
            result = inheritance(d, a, b)
            # Independent element-wise oracle, no subset operator.
            premises = all(not (i in d) or i in a for i in range(n)) and all(not (i in a) or i in b for i in range(n))
            conclusion = all(not (i in d) or i in b for i in range(n))
            oracle_disagreements += result['premises'] != premises or result['conclusion'] != conclusion
            if result['premises']:
                valid += 1
                empty_valid += not d
                violations += not result['conclusion']
    edges = [(i, j) for i in range(2) for j in range(2)]
    relations = [frozenset(edges[i] for i in range(4) if mask & (1 << i)) for mask in range(16)]
    maps_checked = preserving = noninjective_preserving = relation_oracle_disagreements = 0
    for si, sr in enumerate(relations):
        for ti, tr in enumerate(relations):
            for images in product(range(2), repeat=2):
                result = relation_map(range(2), range(2), sr, tr, dict(enumerate(images)))
                oracle = all(not (si & (1 << (2*u+v))) or bool(ti & (1 << (2*images[u]+images[v]))) for u in range(2) for v in range(2))
                maps_checked += 1
                relation_oracle_disagreements += result['preserves_relation'] != oracle
                preserving += result['preserves_relation']
                noninjective_preserving += result['preserves_relation'] and not result['injective']
    if violations or oracle_disagreements or relation_oracle_disagreements:
        raise RuntimeError('oracle or implication failure')
    return {'inheritance': {'triples': triples, 'valid_chains': valid, 'empty_subject_valid': empty_valid,
                           'violations': violations, 'oracle_disagreements': oracle_disagreements},
            'analogy': {'maps_checked': maps_checked, 'preserving': preserving,
                        'noninjective_preserving': noninjective_preserving,
                        'oracle_disagreements': relation_oracle_disagreements},
            'uncovered_sample': observation({0}, {0,1}, {0})}


if __name__ == '__main__':
    print(json.dumps(experiments(), indent=2))
