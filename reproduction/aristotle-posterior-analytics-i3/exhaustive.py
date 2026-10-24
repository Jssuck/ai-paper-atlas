"""Bounded enumerations. Results are tests, never an infinite-regress proof."""
import itertools
import json
from model import Rule, closure, truth_oracle, certificate_ok, inclusion_cycle, finite_chain


def check_case(atoms, seeds, rules):
    got, ranks, witness = closure(atoms, seeds, rules)
    want, _ = truth_oracle(atoms, seeds, rules)
    if got != want or not certificate_ok(atoms, seeds, rules, got, ranks, witness):
        raise RuntimeError('closure/oracle or certificate mismatch')


def run():
    unary = conjunction = inclusion = cycles = 0
    atoms = ('A', 'B', 'C')
    candidates = [Rule(frozenset([a]), b) for a in atoms for b in atoms]
    for mask in range(1 << len(candidates)):
        rules = [r for i, r in enumerate(candidates) if mask & (1 << i)]
        for seedbits in range(8):
            seeds = [a for i, a in enumerate(atoms) if seedbits & (1 << i)]
            check_case(atoms, seeds, rules)
            unary += 1
    atoms = ('A', 'B')
    antecedents = [frozenset(['A']), frozenset(['B']), frozenset(atoms)]
    candidates = [Rule(p, h) for p in antecedents for h in atoms]
    for mask in range(64):
        rules = [r for i, r in enumerate(candidates) if mask & (1 << i)]
        for seedbits in range(4):
            seeds = [a for i, a in enumerate(atoms) if seedbits & (1 << i)]
            check_case(atoms, seeds, rules)
            conjunction += 1
    subsets = [frozenset(i for i in range(3) if mask & (1 << i)) for mask in range(8)]
    for a, b, c in itertools.product(subsets, repeat=3):
        inclusion += 1
        if inclusion_cycle(a, b, c):
            cycles += 1
            if not a == b == c:
                raise RuntimeError('inclusion cycle is not equality')
    for n in range(1, 33):
        for rooted in (False, True):
            atoms, seeds, rules = finite_chain(n, rooted)
            got, ranks, witness = closure(atoms, seeds, rules)
            if got != (frozenset(atoms) if rooted else frozenset()):
                raise RuntimeError('chain mismatch')
            if not certificate_ok(atoms, seeds, rules, got, ranks, witness):
                raise RuntimeError('chain certificate mismatch')
    return {'unary_graph_seed_cases': unary, 'two_atom_horn_seed_cases': conjunction,
            'set_triples': inclusion, 'inclusion_cycles': cycles, 'finite_chain_cases': 64,
            'oracle_or_certificate_mismatches': 0,
            'scope': 'finite teaching models; no empirical or infinite-regress validation'}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
