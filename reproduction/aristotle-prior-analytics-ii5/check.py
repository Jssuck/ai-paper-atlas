#!/usr/bin/env python3
"""Original finite set checks for Prior Analytics II.5; Python standard library."""
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Model:
    U: frozenset
    A: frozenset
    B: frozenset
    C: frozenset

    def nonempty_terms(self):
        return bool(self.A and self.B and self.C)

    def display(self):
        return {name: sorted(getattr(self, name)) for name in ('U', 'A', 'B', 'C')}


def models():
    # One representative per occupied ABC membership type, including type 000.
    for occupied in range(1, 256):
        u = frozenset(t for t in range(8) if occupied & (1 << t))
        yield Model(u, frozenset(t for t in u if t & 4),
                    frozenset(t for t in u if t & 2),
                    frozenset(t for t in u if t & 1))


# Each tuple is (premises, conclusion); all predicates return actual booleans.
VALID = {
    'affirmative_forward': (lambda m: m.C <= m.B and m.B <= m.A, lambda m: m.C <= m.A),
    'recover_B_subset_A': (lambda m: m.C <= m.A and m.B <= m.C, lambda m: m.B <= m.A),
    'recover_C_subset_B': (lambda m: m.C <= m.A and m.A <= m.B, lambda m: m.C <= m.B),
    'negative_forward': (lambda m: m.C <= m.B and not m.B & m.A, lambda m: not m.C & m.A),
    'recover_negative_major': (lambda m: not m.C & m.A and m.B <= m.C, lambda m: not m.B & m.A),
    'recover_with_complement_bridge': (lambda m: not m.C & m.A and m.U-m.A <= m.B, lambda m: m.C <= m.B),
    'particular_affirmative_recovery': (lambda m: bool(m.C & m.A) and m.A <= m.B, lambda m: bool(m.C & m.B)),
    'particular_negative_recovery': (lambda m: bool(m.C-m.A) and m.U-m.A <= m.B, lambda m: bool(m.C & m.B)),
}
INVALID = {
    'conclusion_and_unchanged_minor_do_not_recover_major':
        (lambda m: m.C <= m.A and m.C <= m.B, lambda m: m.B <= m.A),
    'conclusion_and_unchanged_major_do_not_recover_minor':
        (lambda m: m.C <= m.A and m.B <= m.A, lambda m: m.C <= m.B),
    'simple_E_conversion_not_complement_bridge':
        (lambda m: not m.C & m.A and not m.B & m.A, lambda m: m.C <= m.B),
    'separate_negative_witnesses_not_shared_witness':
        (lambda m: bool(m.C-m.A) and bool(m.B-m.A), lambda m: bool(m.C & m.B)),
    'particular_affirmative_does_not_recover_universal':
        (lambda m: bool(m.C & m.A) and bool(m.B & m.C), lambda m: m.B <= m.A),
    'particular_negative_does_not_recover_universal':
        (lambda m: bool(m.C-m.A) and bool(m.B & m.C), lambda m: not m.B & m.A),
}


def check_schema(domain, premises, conclusion):
    applicable = [m for m in domain if premises(m)]
    failures = [m for m in applicable if not conclusion(m)]
    return {'premise_models': len(applicable), 'counterexamples': len(failures)}, failures


def assumption_dependencies(node, proof, stack=()):
    """Audit dependency edges only, NOT a general logical inference checker.

    None denotes an explicit assumption. A tuple names required proof nodes.
    Cycles are refused instead of silently treating self-support as evidence.
    """
    if node in stack:
        raise ValueError('cyclic dependency')
    parents = proof[node]
    if parents is None:
        return {node}
    result = set()
    for parent in parents:
        result.update(assumption_dependencies(parent, proof, stack + (node,)))
    return result


def run():
    all_models = list(models())
    domains = {'nonempty_universe': all_models,
               'all_terms_nonempty': [m for m in all_models if m.nonempty_terms()]}
    report = {'model_counts': {k: len(v) for k, v in domains.items()}, 'valid': {}, 'invalid': {}}
    for name, domain in domains.items():
        report['valid'][name] = {}
        report['invalid'][name] = {}
        for schema, (premises, conclusion) in VALID.items():
            stats, failures = check_schema(domain, premises, conclusion)
            assert stats['premise_models'] > 0, schema
            assert not failures, schema
            report['valid'][name][schema] = stats
        for schema, (premises, conclusion) in INVALID.items():
            stats, failures = check_schema(domain, premises, conclusion)
            assert failures, schema
            witness = min(failures, key=lambda m: (len(m.U), tuple(sorted(m.U))))
            report['invalid'][name][schema] = dict(stats, smallest_countermodel=witness.display())
    # Explicit proof tree: C<=A appears at the root and among the assumptions.
    proof = {'assumed_C<=A': None, 'A<=B': None, 'B<=A': None,
             'C<=B': ('assumed_C<=A', 'A<=B'),
             'derived_C<=A': ('C<=B', 'B<=A')}
    deps = assumption_dependencies('derived_C<=A', proof)
    assert 'assumed_C<=A' in deps
    cycle = {'C<=A': ('C<=B', 'B<=A'), 'C<=B': ('C<=A', 'A<=B'),
             'A<=B': None, 'B<=A': None}
    try:
        assumption_dependencies('C<=A', cycle)
    except ValueError:
        refused = True
    else:
        refused = False
    assert refused
    report['dependency_demo'] = {'assumptions_retained': sorted(deps), 'cycle_refused': refused,
                                 'scope': 'dependency audit, not general proof verification'}
    return report

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
