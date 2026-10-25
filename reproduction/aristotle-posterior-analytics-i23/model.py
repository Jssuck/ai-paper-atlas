"""Original finite teaching models for Posterior Analytics I.23; no scientific-cause oracle."""
from itertools import combinations, product
import json


def strict_closure(n, edges):
    if not isinstance(n, int) or n < 0:
        raise ValueError('n must be nonnegative integer')
    relation = set(edges)
    if any(not (0 <= a < n and 0 <= b < n) for a, b in relation):
        raise ValueError('vertex outside vocabulary')
    for k in range(n):
        relation |= {(a, b) for a in range(n) for b in range(n)
                     if (a, k) in relation and (k, b) in relation}
    if any((a, a) in relation for a in range(n)):
        raise ValueError('strict-order model rejects cycles')
    return frozenset(relation)


def inside(n, relation, low, high):
    return tuple(x for x in range(n) if (low, x) in relation and (x, high) in relation)


def common_middles(n, relation, c, d, a):
    """Strict internal common upper bounds; endpoints do not count as new explanations."""
    return tuple(x for x in range(n) if (c, x) in relation and (d, x) in relation and (x, a) in relation)


def refinements(n, relation, chain):
    """One fresh internal insertion; accepts a valid increasing chain of >=2 vertices."""
    if len(chain) < 2 or any((a, b) not in relation for a, b in zip(chain, chain[1:])):
        raise ValueError('invalid increasing chain')
    return tuple(chain[:i+1] + (x,) + chain[i+1:]
                 for i, (a, b) in enumerate(zip(chain, chain[1:]))
                 for x in inside(n, relation, a, b))


def refinement_states(n, relation, low, high):
    start = (low, high)
    seen, todo = {start}, [start]
    while todo:
        current = todo.pop()
        for nxt in refinements(n, relation, current):
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return tuple(sorted(seen))


def chain_counts(chain):
    if len(chain) < 2:
        raise ValueError('need two endpoints')
    return {'terms': len(chain), 'internal_terms': len(chain)-2,
            'adjacent_premises': len(chain)-1}


def rule_values(s, p, m):
    """Each pair = (premises true, intended conclusion true). Universal formulas permit empties."""
    e = not bool(s & p)
    o = bool(s - p)
    return {
        'Celarent': (s <= m and not bool(m & p), e),
        'Camestres': (p <= m and not bool(s & m), e),
        'Baroco': (p <= m and bool(s - m), o),
        'Felapton_nonempty_M': (not bool(m & p) and m <= s and bool(m), o),
        'Bocardo': (bool(m - p) and m <= s, o),
    }


def enumerate_rules(max_n=4):
    counts = {name: {'premise_models': 0, 'counterexamples': 0}
              for name in rule_values(set(), set(), set())}
    assignments = 0
    for n in range(max_n+1):
        subsets = [frozenset(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]
        for s, p, m in product(subsets, repeat=3):
            assignments += 1
            for name, (prem, conclusion) in rule_values(s, p, m).items():
                counts[name]['premise_models'] += int(prem)
                counts[name]['counterexamples'] += int(prem and not conclusion)
    return {'universe_sizes': list(range(max_n+1)), 'assignments': assignments, 'rules': counts}


def enumerate_orders(max_n=4):
    out = dict(generated_dags=0, intervals=0, refinement_states=0, saturated_chains=0,
               incomparable_common_target_cases=0, without_internal_common_middle=0,
               counting_violations=0, insertion_violations=0)
    for n in range(1, max_n+1):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            r = strict_closure(n, [e for i,e in enumerate(possible) if mask >> i & 1])
            out['generated_dags'] += 1
            for c,d in combinations(range(n), 2):
                if (c,d) in r or (d,c) in r:
                    continue
                for a in range(n):
                    if (c,a) in r and (d,a) in r:
                        out['incomparable_common_target_cases'] += 1
                        out['without_internal_common_middle'] += int(not common_middles(n,r,c,d,a))
            for low,high in r:
                out['intervals'] += 1
                states = refinement_states(n,r,low,high)
                out['refinement_states'] += len(states)
                for chain in states:
                    counts = chain_counts(chain)
                    out['counting_violations'] += int(counts['adjacent_premises'] != counts['internal_terms']+1)
                    successors = refinements(n,r,chain)
                    if not successors:
                        out['saturated_chains'] += 1
                    for nxt in successors:
                        okay = (nxt[0] == low and nxt[-1] == high and len(nxt)==len(chain)+1
                                and len(nxt)<=n and len(set(nxt))==len(nxt)
                                and all(x in inside(n,r,low,high) for x in nxt[1:-1]))
                        out['insertion_violations'] += int(not okay)
    return out


def report():
    fork = strict_closure(3, [(0,2),(1,2)])
    expanded = strict_closure(4, [(0,2),(1,2),(2,3)])
    return {'scope':'Finite teaching reconstruction, not certification of causes, genera, intuition or infinite termination.',
            'orders': enumerate_orders(), 'negative_rules': enumerate_rules(),
            'examples': {'fork_common_middles': list(common_middles(3,fork,0,1,2)),
                         'expanded_common_middles': list(common_middles(4,expanded,0,1,3)),
                         'one_middle_count':chain_counts((0,1,2)),
                         'Baroco_not_universal': {'S':[0,1], 'P':[0], 'M':[0]},
                         'empty_middle_Felapton_failure': {'S':[0], 'P':[0], 'M':[]}}}

if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2))
