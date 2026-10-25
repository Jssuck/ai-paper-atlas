"""Independent DFS/permutation and pointwise-Boolean audit, not an infinite proof."""
from itertools import permutations, combinations, product
import json
import model


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def dfs_relation(n, edges):
    adjacency = {i: [] for i in range(n)}
    for a, b in edges:
        adjacency[a].append(b)
    relation = set()
    for source in range(n):
        todo = list(adjacency[source])
        reached = set()
        while todo:
            target = todo.pop()
            if target not in reached:
                reached.add(target)
                todo.extend(adjacency[target])
        relation.update((source, x) for x in reached)
    return relation


def order_audit():
    n = 4
    possible = [(a, b) for a in range(n) for b in range(n) if a != b]
    counts = dict(directed_graphs=0, dags=0, cyclic=0, intervals=0,
                  compared_chains=0, common_target_cases=0, mismatches=0)
    for mask in range(1 << len(possible)):
        edges = [e for bit, e in enumerate(possible) if mask & (1 << bit)]
        expected = dfs_relation(n, edges)
        counts['directed_graphs'] += 1
        if any((a, a) in expected for a in range(n)):
            counts['cyclic'] += 1
            try:
                model.strict_closure(n, edges)
            except ValueError:
                continue
            raise RuntimeError('cycle accepted')
        counts['dags'] += 1
        actual = model.strict_closure(n, edges)
        require(actual == expected, 'closure mismatch')
        for c, d in combinations(range(n), 2):
            if (c, d) in expected or (d, c) in expected:
                continue
            for a in range(n):
                if (c, a) in expected and (d, a) in expected:
                    counts['common_target_cases'] += 1
                    wanted = {x for x in range(n) if all(e in expected for e in [(c,x),(d,x),(x,a)])}
                    require(set(model.common_middles(n, actual, c, d, a)) == wanted, 'common-middle mismatch')
        for low, high in expected:
            counts['intervals'] += 1
            others = [x for x in range(n) if x not in (low, high)]
            wanted = set()
            for k in range(len(others)+1):
                for middle in permutations(others, k):
                    chain = (low,)+middle+(high,)
                    if all(e in expected for e in zip(chain, chain[1:])):
                        wanted.add(chain)
            actual_chains = set(model.refinement_states(n, actual, low, high))
            require(actual_chains == wanted, 'chain enumeration mismatch')
            for chain in wanted:
                counts['compared_chains'] += 1
                require(model.chain_counts(chain) == {'terms':len(chain), 'internal_terms':len(chain)-2,
                                                       'adjacent_premises':len(chain)-1}, 'chain counts')
                # A successor is independently identified by deleting one internal node.
                successors = {candidate for candidate in wanted if len(candidate)==len(chain)+1
                              and any(candidate[:i]+candidate[i+1:]==chain for i in range(1,len(candidate)-1))}
                require(set(model.refinements(n, actual, chain)) == successors, 'successor mismatch')
    return counts


def subset_audit():
    names = ['Celarent','Camestres','Baroco','Felapton_nonempty_M','Bocardo']
    counts = {name:dict(premise_models=0,counterexamples=0) for name in names}
    assignments = 0
    for n in range(6):
        for sm, pm, mm in product(range(1 << n), repeat=3):
            triples = [(bool(sm & (1 << i)), bool(pm & (1 << i)), bool(mm & (1 << i))) for i in range(n)]
            all_sp_disjoint = all(not(s and p) for s,p,m in triples)
            some_s_not_p = any(s and not p for s,p,m in triples)
            premises = [all(not s or m for s,p,m in triples) and all(not(m and p) for s,p,m in triples),
                        all(not p or m for s,p,m in triples) and all(not(s and m) for s,p,m in triples),
                        all(not p or m for s,p,m in triples) and any(s and not m for s,p,m in triples),
                        all(not(m and p) for s,p,m in triples) and all(not m or s for s,p,m in triples) and any(m for s,p,m in triples),
                        any(m and not p for s,p,m in triples) and all(not m or s for s,p,m in triples)]
            conclusions = [all_sp_disjoint]*2+[some_s_not_p]*3
            actual = model.rule_values({i for i in range(n) if sm & (1<<i)},
                                       {i for i in range(n) if pm & (1<<i)},
                                       {i for i in range(n) if mm & (1<<i)})
            assignments += 1
            for name, prem, conc in zip(names,premises,conclusions):
                require(actual[name] == (prem,conc), 'rule implementation mismatch')
                counts[name]['premise_models'] += int(prem)
                counts[name]['counterexamples'] += int(prem and not conc)
                require(not prem or conc, 'invalid negative rule')
    return dict(universe_sizes=list(range(6)), assignments=assignments, rules=counts, mismatches=0)


if __name__ == '__main__':
    print(json.dumps({'scope':'Independent finite implementation check; no claim about scientific causes or infinite structures.',
                      'orders':order_audit(), 'negative_rules':subset_audit()},indent=2))
