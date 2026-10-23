"""Exhaustive finite checks; explicit failures remain active under Python -O/-OO."""
import json
from model import Model, powerset, families


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run():
    totals = dict(family_models=0, weak_without_strong=0, covered_models=0,
                  triples=0, all_chain_cases=0, some_chain_cases=0, some_not_all_cases=0)
    per_size = []
    for n in range(1, 4):
        d = frozenset(range(n))
        subsets = powerset(d)
        start = totals.copy()
        for a in subsets:
            for b in subsets:
                m = Model(d, a, b)
                for c in subsets:
                    totals['triples'] += 1
                    if b <= a and c <= b:
                        require(m.all_chain(c), 'all-chain failure')
                        totals['all_chain_cases'] += 1
                    if b <= a and c & b:
                        witness = m.some_chain_witness(c)
                        require(witness in a & b & c, 'witness failure')
                        totals['some_chain_cases'] += 1
                        if not c <= a:
                            totals['some_not_all_cases'] += 1
                for family in families(subsets):
                    m = Model(d, a, b, family)
                    strong, weak, u = m.strong(), m.weak(), m.eligible_union()
                    require(not strong or weak, 'strong-to-weak failure')
                    require(weak == (u <= a), 'union equivalence failure')
                    require(u <= b, 'eligible union escaped b')
                    if m.covers_b():
                        totals['covered_models'] += 1
                        require(strong == weak, 'coverage converse failure')
                    totals['family_models'] += 1
                    totals['weak_without_strong'] += int(weak and not strong)
        per_size.append({'n': n, **{k: totals[k] - start[k] for k in totals}})
    weak_example = Model({0, 1, 2}, {0}, {0, 1}, ({0}, {1, 2}))
    require(weak_example.weak() and not weak_example.strong(), 'weak counterexample lost')
    require(not ({1, 2} & weak_example.a) and bool({1, 2} & weak_example.b), 'counterexample overlap failure')
    result = {'scope': 'all A,B,C subsets and all families of subsets, nonempty domains n=1,2,3',
              'per_size': per_size, 'totals': totals,
              'counterexample': {'D': [0, 1, 2], 'A': [0], 'B': [0, 1], 'F': [[0], [1, 2]],
                                 'eligible_union': [0], 'C': [1, 2], 'weak': True, 'strong': False},
              'limit': 'Finite implementation check only; no proof of a general theorem or ancient semantics.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    run()
