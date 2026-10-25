"""Independent exhaustive small-instance oracle for the I.22 teaching model.

Uses Boolean Floyd-Warshall, full permutations, and intersection of all models,
not production DFS ranks, insertion exploration, or iterative Horn closure.
Finite implementation checking only; no scientific/epistemic certification.
"""
import itertools
import json
import platform
from model import strict_ranks, order_closure, all_refinements, horn_closure


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def graph_oracle():
    n = 4
    vertices = tuple(range(n))
    possible = tuple((x,y) for x in vertices for y in vertices if x != y)
    out = {'directed_graphs':0, 'acyclic_graphs':0, 'cyclic_graphs_rejected':0,
           'comparable_intervals':0, 'chain_states':0, 'saturated_chains':0,
           'mismatches':0}
    for mask in range(1 << len(possible)):
        edges = {edge for i,edge in enumerate(possible) if mask >> i & 1}
        out['directed_graphs'] += 1
        reach = [[(x,y) in edges for y in vertices] for x in vertices]
        for k in vertices:
            for x in vertices:
                for y in vertices:
                    reach[x][y] = reach[x][y] or (reach[x][k] and reach[k][y])
        if any(reach[x][x] for x in vertices):
            try:
                strict_ranks(vertices, edges)
            except ValueError:
                out['cyclic_graphs_rejected'] += 1
            else:
                raise RuntimeError('cycle accepted')
            continue
        out['acyclic_graphs'] += 1
        relation = {(x,y) for x in vertices for y in vertices if reach[x][y]}
        require(order_closure(vertices,edges) == relation, 'closure mismatch')
        expected_ranks = {}
        for x in vertices:
            paths = [(x,)]
            for count in range(1,n):
                paths += [(x,)+tail for tail in itertools.permutations([y for y in vertices if y != x],count)
                          if all(edge in edges for edge in zip((x,)+tail,tail))]
            expected_ranks[x] = max(len(p)-1 for p in paths)
        require(strict_ranks(vertices,edges) == expected_ranks, 'rank mismatch')
        for left,right in relation:
            out['comparable_intervals'] += 1
            candidates = [x for x in vertices if x not in (left,right)]
            states = set()
            for count in range(n-1):
                for middle in itertools.permutations(candidates,count):
                    chain = (left,) + middle + (right,)
                    if all((x,y) in relation for x,y in zip(chain,chain[1:])):
                        states.add(chain)
            terminals = {chain for chain in states if all(
                not any((x,z) in relation and (z,y) in relation for z in vertices)
                for x,y in zip(chain,chain[1:]))}
            actual_states,actual_terminals = all_refinements(left,right,vertices,edges)
            require(actual_states == states, 'refinement state mismatch')
            require(actual_terminals == terminals, 'cover-chain mismatch')
            require(all(len(c) <= n for c in states), 'insertion bound')
            out['chain_states'] += len(states)
            out['saturated_chains'] += len(terminals)
    # Self-loops are not part of the loop-free 4096-graph enumeration.
    for x in vertices:
        try:
            strict_ranks(vertices,{(x,x)})
        except ValueError:
            continue
        raise RuntimeError('self-loop accepted')
    out['self_loop_cases_rejected'] = n
    return out


def horn_oracle():
    atoms = frozenset(('p','q'))
    assignments = [frozenset(x for i,x in enumerate(sorted(atoms)) if mask >> i & 1) for mask in range(4)]
    possible = [(body,head) for body in assignments for head in sorted(atoms)]
    total = 0
    for mask in range(1 << len(possible)):
        rules = [rule for i,rule in enumerate(possible) if mask >> i & 1]
        for seeds in assignments:
            models = [value for value in assignments if seeds <= value and
                      all(not body <= value or head in value for body,head in rules)]
            expected = frozenset.intersection(*models)
            actual,rounds = horn_closure(atoms,rules,seeds)
            require(actual == expected,'Horn least-model mismatch')
            require(all(rounds),'empty recorded round')
            require(sum(len(r) for r in rounds) == len(actual-seeds),'round accounting')
            total += 1
    return {'atoms':2,'possible_rules':8,'rulebooks':256,'seed_cases_per_rulebook':4,
            'cases_checked':total,'mismatches':0}


if __name__ == '__main__':
    print(json.dumps({'python':platform.python_version(),'graph_oracle':graph_oracle(),
                      'horn_model_intersection_oracle':horn_oracle(),
                      'scope':'Exhaustive finite implementation tests; not the historical infinite theorem.'},
                     ensure_ascii=False,indent=2))
