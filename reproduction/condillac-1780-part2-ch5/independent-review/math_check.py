"""Independent finite arithmetic and relation audit; imports no release code."""
from itertools import product, permutations
import json


def ensure(value, message):
    if not value:
        raise RuntimeError(message)


def closure(n, edges):
    r = set(edges) | {(a, a) for a in range(n)}
    while True:
        enlarged = r | {(a, d) for a, b in r for c, d in r if b == c}
        if enlarged == r:
            return r
        r = enlarged


positions = [(a,b) for a in range(3) for b in range(3) if a != b]
subsets = [frozenset(x for x in range(2) if mask & (1 << x)) for mask in range(4)]
counts = dict(extension_assignments=0, graph_contexts=0, valid_graphs=0, invalid_graphs=0,
              reachability_queries=0, semantic_queries=0, certified_queries=0,
              true_unencoded_queries=0, failed_inclusions=0, mutual_reachability_pairs=0,
              renamed_valid_graphs=0, renamed_queries=0,
              equal_partitions_but_incomplete_valid_graphs=0)
for ex in product(subsets, repeat=3):
    counts['extension_assignments'] += 1
    semantic = {(a,b) for a in range(3) for b in range(3) if ex[a] <= ex[b]}
    semantic_equal = {(a,b) for a,b in semantic if (b,a) in semantic}
    for mask in range(64):
        graph = {edge for i, edge in enumerate(positions) if mask & (1 << i)}
        reach = closure(3, graph)
        counts['graph_contexts'] += 1
        valid = graph <= semantic
        ensure(valid == (reach <= semantic), 'Soundness equivalence failed')
        counts['valid_graphs' if valid else 'invalid_graphs'] += 1
        counts['reachability_queries'] += 9
        counts['semantic_queries'] += 9
        counts['failed_inclusions'] += 9-len(semantic)
        mutual = {(a,b) for a,b in reach if (b,a) in reach}
        if valid:
            counts['certified_queries'] += 9
            counts['true_unencoded_queries'] += len(semantic-reach)
            counts['mutual_reachability_pairs'] += len(mutual)
            ensure(mutual <= semantic_equal, 'SCC refinement failed')
            if mutual == semantic_equal and not semantic <= reach:
                counts['equal_partitions_but_incomplete_valid_graphs'] += 1
            for perm in permutations(range(3)):
                graph2 = {(perm[a],perm[b]) for a,b in graph}
                reach2 = closure(3,graph2)
                ensure(reach2 == {(perm[a],perm[b]) for a,b in reach}, 'Rename failed')
                counts['renamed_valid_graphs'] += 1
                counts['renamed_queries'] += 9

# Explicit counterexample: same quotient partitions, different quotient order.
ex = ({0},{0},{0,1})
graph = {(0,1),(1,0)}
reach = closure(3, graph)
semantic = {(a,b) for a in range(3) for b in range(3) if ex[a] <= ex[b]}
ensure({(a,b) for a,b in reach if (b,a) in reach} == {(a,b) for a,b in semantic if (b,a) in semantic}, 'Counterexample partitions differ')
ensure((0,2) in semantic and (0,2) not in reach, 'Counterexample complete')

# Mathematical zero-label and empty-universe cases; not implementation API tests.
ensure(closure(0,set()) == set(), 'Empty label relation failed')
empty_universe_graphs = 0
for mask in range(16):
    positions2 = [(a,b) for a in range(2) for b in range(2)]
    g = {edge for i,edge in enumerate(positions2) if mask & (1 << i)}
    ensure(closure(2,g) <= set(positions2), 'Empty universe soundness failed')
    empty_universe_graphs += 1

output = {'status':'passed', 'imports_release_implementation':False,
          'closure_method':'set saturation until a fixed point',
          'counts':counts,
          'boundaries':{'zero_label_mathematical_model':True, 'empty_universe_two_label_graphs_including_self_loops':empty_universe_graphs},
          'caution':'Finite relation arithmetic is not an independent rerun of the implementation and not a general proof.'}
print(json.dumps(output, ensure_ascii=False, indent=2))
