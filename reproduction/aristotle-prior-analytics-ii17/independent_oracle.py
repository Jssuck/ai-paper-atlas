"""Independent audit by one-object set semantics and subset minimization.
This is an original finite teaching checker, not an edition of Aristotle.
"""
from itertools import combinations, product
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import logic as production

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def assignments(nodes):
    return [dict(zip(nodes, bits)) for bits in product((False, True), repeat=len(nodes))]

def satisfies(assignment, edge):
    subject, predicate = edge
    return not assignment[subject] or assignment[predicate]

def entailed(edges, target, nodes):
    # Universal inclusions hold pointwise. A single bit-pattern refutes entailment.
    return all(not all(satisfies(a, e) for e in edges) or satisfies(a, target)
               for a in assignments(nodes))

def subsets(items):
    for size in range(len(items) + 1):
        yield from combinations(items, size)

def semantic_supports(edges, target, nodes):
    result = []
    for candidate in subsets(tuple(sorted(edges))):
        cand = frozenset(candidate)
        if any(old <= cand for old in result):
            continue
        if entailed(cand, target, nodes):
            result.append(cand)
    return set(result)

def main():
    nodes = ('A', 'B', 'C')
    possible = tuple((a,b) for a in nodes for b in nodes if a != b)
    counts = {'graphs':0,'closure_pairs':0,'minimal_support_pairs':0,'deletion_pairs':0,'initially_derived':0,'still_derived':0,'necessary':0}
    for edges_tuple in subsets(possible):
        edges = set(edges_tuple)
        counts['graphs'] += 1
        oracle_closure = {(a,b) for a in nodes for b in nodes if entailed(edges,(a,b),nodes)}
        actual = production.closure(edges,nodes)
        require(set(actual) == oracle_closure, f'closure mismatch: {edges}')
        for target in product(nodes,repeat=2):
            counts['closure_pairs'] += 1
            expected = semantic_supports(edges,target,nodes)
            actual_supports = {frozenset(map(tuple,s)) for s in production.minimal_supports(edges,target,nodes)}
            require(actual_supports == expected, f'support mismatch: {edges}, {target}, {actual_supports}, {expected}')
            counts['minimal_support_pairs'] += 1
            for hypothesis in edges:
                result = production.analyze(edges,hypothesis,target,nodes)
                before = entailed(edges,target,nodes)
                after = entailed(edges-{hypothesis},target,nodes)
                require(result['before'] == before, 'before mismatch')
                require(result['after_deleted'] == after, 'after mismatch')
                require(result['necessary_within_graph'] == (before and not after), 'necessity mismatch')
                counts['deletion_pairs'] += 1
                counts['initially_derived'] += before
                counts['still_derived'] += after
                counts['necessary'] += before and not after
    print(json.dumps({'result':'PASS','counts':counts,'oracle':'one-object Boolean set semantics plus exhaustive edge subsets','scope':'three named terms; universal positive inclusions only'},sort_keys=True))

if __name__ == '__main__':
    main()
