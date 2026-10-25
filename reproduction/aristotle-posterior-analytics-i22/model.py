"""Original finite teaching models for Posterior Analytics I.22.

All relations and axioms are supplied, not discovered or scientifically certified.
Dependency arrows point from a defined term to a term used in its definition.
An order arrow x -> y is a separately supplied strict ascent, NOT a claim that
all definition dependencies are Aristotelian predications or proper subsets.
"""
import itertools
import json
from pathlib import Path


def definition_link(subject, predicate, kind):
    """kind 1: predicate occurs in subject's definition; kind 2: reverse.

This returns bookkeeping for a declared per-se relation, not a validity test.
"""
    if not isinstance(subject, str) or not subject or not isinstance(predicate, str) or not predicate:
        raise ValueError('nonempty term names required')
    if kind == 1:
        return subject, predicate
    if kind == 2:
        return predicate, subject
    raise ValueError('kind must be 1 or 2')


def checked_graph(vertices, edges):
    vertices = frozenset(vertices)
    edges = frozenset(tuple(e) for e in edges)
    if any(len(e) != 2 or e[0] not in vertices or e[1] not in vertices for e in edges):
        raise ValueError('edge outside vertex set')
    return vertices, edges


def strict_ranks(vertices, edges):
    """Longest distance to a sink; rank(x)>rank(y) for every x->y.

Raises for any directed cycle, including self-loops. Categories play no role.
"""
    vertices, edges = checked_graph(vertices, edges)
    children = {x: {v for u, v in edges if u == x} for x in vertices}
    ranks, visiting = {}, set()
    def visit(x):
        if x in visiting:
            raise ValueError('directed cycle: strict finite rank impossible')
        if x in ranks:
            return ranks[x]
        visiting.add(x)
        ranks[x] = 1 + max((visit(y) for y in children[x]), default=-1)
        visiting.remove(x)
        return ranks[x]
    for x in vertices:
        visit(x)
    return ranks


def order_closure(vertices, edges):
    """Strict transitive closure of a DAG; never silently accepts cycles."""
    vertices, edges = checked_graph(vertices, edges)
    strict_ranks(vertices, edges)
    relation = set(edges)
    while True:
        expanded = relation | {(a, d) for a, b in relation for c, d in relation if b == c}
        if expanded == relation:
            return frozenset(relation)
        relation = expanded


def refinement_successors(chain, vertices, relation):
    """Insert one middle into an existing adjacent interval, preserving ends.

relation must be a strict transitive order, not just its generating edges.
"""
    chain = tuple(chain)
    vertices, relation = checked_graph(vertices, relation)
    if order_closure(vertices, relation) != relation:
        raise ValueError('relation must be transitively closed')
    if not chain or any(x not in vertices for x in chain) or len(set(chain)) != len(chain):
        raise ValueError('invalid chain vertices')
    if any((x, y) not in relation for x, y in zip(chain, chain[1:])):
        raise ValueError('not an ordered chain')
    return frozenset(chain[:i+1] + (z,) + chain[i+1:]
                     for i, (x, y) in enumerate(zip(chain, chain[1:]))
                     for z in vertices if (x, z) in relation and (z, y) in relation)


def all_refinements(left, right, vertices, edges):
    """All reachable refinement states starting with (left,right)."""
    vertices, edges = checked_graph(vertices, edges)
    relation = order_closure(vertices, edges)
    if (left, right) not in relation:
        raise ValueError('endpoints must be strictly comparable')
    seen, pending, terminals = {(left, right)}, [(left, right)], set()
    while pending:
        chain = pending.pop()
        successors = refinement_successors(chain, vertices, relation)
        if not successors:
            terminals.add(chain)
        for new in successors - seen:
            seen.add(new)
            pending.append(new)
    return seen, terminals


def horn_closure(atoms, rules, seeds):
    """Synchronous least syntactic closure; no epistemic truth certification.

A rule is (iterable of premises, conclusion). An empty premise is an axiom.
Return final set and nonempty sets added at each round.
"""
    atoms, known = frozenset(atoms), set(seeds)
    rules = [(frozenset(premises), conclusion) for premises, conclusion in rules]
    if not known <= atoms or any(not p <= atoms or c not in atoms for p, c in rules):
        raise ValueError('unknown atom')
    rounds = []
    while True:
        added = {c for p, c in rules if p <= known} - known
        if not added:
            return frozenset(known), rounds
        rounds.append(frozenset(added))
        known.update(added)


def experiment():
    totals = dict(graphs=0, comparable_intervals=0, refinement_states=0,
                  saturated_chains=0, endpoint_violations=0, cover_violations=0,
                  insertion_bound_violations=0, rank_violations=0)
    for n in range(1, 5):
        vertices = tuple(range(n))
        possible = tuple(itertools.combinations(vertices, 2))
        for bits in range(1 << len(possible)):
            edges = {e for i, e in enumerate(possible) if bits >> i & 1}
            totals['graphs'] += 1
            relation = order_closure(vertices, edges)
            rank = strict_ranks(vertices, edges)
            totals['rank_violations'] += sum(rank[x] <= rank[y] for x, y in relation)
            for left, right in relation:
                totals['comparable_intervals'] += 1
                states, terminals = all_refinements(left, right, vertices, edges)
                totals['refinement_states'] += len(states)
                totals['saturated_chains'] += len(terminals)
                totals['endpoint_violations'] += sum(c[0] != left or c[-1] != right for c in states)
                totals['insertion_bound_violations'] += sum(len(c)-2 > n-2 for c in states)
                for c in terminals:
                    totals['cover_violations'] += sum(any((x,z) in relation and (z,y) in relation for z in vertices) for x,y in zip(c,c[1:]))
    cycle = {(0,1), (1,0)}
    try:
        strict_ranks({0,1}, cycle)
        cycle_rejected = False
    except ValueError:
        cycle_rejected = True
    rules = [({'p'},'q'), ({'q'},'p'), ({'q'},'r')]
    empty, _ = horn_closure({'p','q','r'}, rules, set())
    seeded, rounds = horn_closure({'p','q','r'}, rules, {'p'})
    return {'finite_orders': totals,
            'declared_definition_links': [list(definition_link('human','animal',1)), list(definition_link('number','odd',2))],
            'one_category_cycle': {'vertices':2,'categories':1,'rank_rejected':cycle_rejected},
            'horn_example': {'without_seed': sorted(empty), 'with_seed_p':sorted(seeded), 'added_rounds':[sorted(r) for r in rounds]},
            'scope':'Finite supplied syntactic structures only; not a proof of Aristotle\'s infinite claim or a certification of knowledge.'}

if __name__ == '__main__':
    result = experiment()
    Path('results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
