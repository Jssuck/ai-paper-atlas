"""Bounded regression checks, not a proof of a general theorem."""
import itertools
import json
from model import Atom, Ref, And, Not, Definitions, Model


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def subsets(n):
    return [frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]


def main():
    p, q, r = Atom('P'), Atom('Q'), Atom('R')
    defs = Definitions({'both': And(p, q), 'outside': Not(p), 'nested': And(Ref('both'), Not(r)), 'alias': Ref('nested')})
    pairs = [(Ref('both'), And(p, q)), (Ref('outside'), Not(p)),
             (Ref('nested'), And(And(p, q), Not(r))), (Ref('alias'), Ref('nested'))]
    models = extension_checks = proposition_checks = 0
    for n in range(4):
        for pv, qv, rv in itertools.product(subsets(n), repeat=3):
            m = Model(range(n), {'P': pv, 'Q': qv, 'R': rv})
            models += 1
            for left, right in pairs:
                check(defs.equivalent_by_definition(left, right), 'missing definition certificate')
                check(m.extension(left, defs) == m.extension(right, defs), 'extension not preserved')
                extension_checks += 1
                for other in (p, q, r, Not(p)):
                    for kind in 'AEIO':
                        check(m.proposition(kind, left, other, defs) == m.proposition(kind, right, other, defs), 'subject replacement failure')
                        check(m.proposition(kind, other, left, defs) == m.proposition(kind, other, right, defs), 'predicate replacement failure')
                        proposition_checks += 2
    # P subset Q is true, but replacing P by Q in A(P,R) can destroy truth.
    m = Model([0, 1], {'P': [0], 'Q': [0, 1], 'R': [0]})
    check(m.proposition('A', p, q, defs), 'subset premise')
    check(m.proposition('A', p, r, defs) and not m.proposition('A', q, r, defs), 'one-way counterexample')
    # Coincidence in one model is not a definition certificate or all-model identity.
    coincident = Model([0], {'P': [0], 'Q': [0], 'R': []})
    check(coincident.extension(p, defs) == coincident.extension(q, defs), 'coincidence example')
    check(not defs.equivalent_by_definition(p, q), 'false certificate from coincidence')
    check(m.extension(p, defs) != m.extension(q, defs), 'separating model')
    # Ambiguous printed middle term: M1 and M2 are different predicates.
    m1, m2, a, c = map(Atom, ('M1', 'M2', 'A', 'C'))
    ambiguous = Model([0, 1], {'M1': [0], 'M2': [1], 'A': [1], 'C': [0]})
    check(ambiguous.proposition('A', c, m1, defs), 'first ambiguous premise')
    check(ambiguous.proposition('A', m2, a, defs), 'second ambiguous premise')
    check(not ambiguous.proposition('A', c, a, defs), 'ambiguous middle counterexample')
    print(json.dumps({'model_count_domain_0_to_3': models, 'definition_pairs': len(pairs),
                      'extension_equalities': extension_checks, 'proposition_truth_equalities': proposition_checks,
                      'counterexamples': ['one_way_inclusion', 'coincidence_not_definition', 'ambiguous_middle'],
                      'result': 'pass', 'scope': 'finite extensional teaching model; not a general proof or natural-language synonym verifier'}, indent=2))


if __name__ == '__main__':
    main()
