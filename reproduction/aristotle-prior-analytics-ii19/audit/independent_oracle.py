"""Independent finite-model audit; expected entailments use Boolean valuations."""
import importlib.util
import itertools
import json
from pathlib import Path
import sys

DEFAULT = Path(__file__).resolve().parents[1] / 'presentation.py'
path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
spec = importlib.util.spec_from_file_location('subject', path)
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)

def check(condition, detail):
    if not condition:
        raise RuntimeError(detail)

def expected(terms, edges):
    models = [set(t for t, bit in zip(terms, bits) if bit)
              for bits in itertools.product((0, 1), repeat=len(terms))]
    models = [m for m in models if all(s not in m or p in m for s,p in edges)]
    return frozenset((s,p) for s,p in itertools.permutations(terms,2)
                     if all(s not in m or p in m for m in models))

terms = 'ABCD'
pairs = tuple(itertools.permutations(terms,2))
witness_checks = 0
for mask in range(1 << len(pairs)):
    edges = tuple(e for i,e in enumerate(pairs) if mask & (1<<i))
    want = expected(terms, edges)
    check(subject.closure(edges) == want, ('semantic mismatch', mask))
    for s,p in pairs:
        path = subject.witness(edges,s,p)
        check((path is not None) == ((s,p) in want), ('witness existence',mask,s,p))
        if path is not None:
            check(path[0] == s and path[-1] == p and len(set(path)) == len(path), ('endpoints',mask))
            check(all(e in edges for e in zip(path,path[1:])), ('invalid edge',mask))
            # All shorter simple paths independently enumerated, not BFS.
            for nmiddle in range(len(path)-2):
                for mids in itertools.permutations([t for t in terms if t not in (s,p)], nmiddle):
                    candidate = (s,)+mids+(p,)
                    check(not all(e in edges for e in zip(candidate,candidate[1:])), ('not shortest',mask,s,p))
        witness_checks += 1

# Construct chain independently rather than borrowing production constants.
chain = tuple(zip('BCDEF','ABCDE'))
hist = {}
for order in itertools.permutations(chain):
    profile = subject.profile(order)
    counts = [len(expected('ABCDEF',order[:k])) for k in range(1,6)]
    check(profile['prefix_closure_sizes'] == counts, ('prefix counts',order))
    check(profile['prefix_target_available'] == [False]*4+[True], ('target timing',order))
    adjacency = sum(len(set(order[i]).intersection(order[i+1])) > 0 for i in range(4))
    check(profile['adjacent_shared_term_pairs'] == adjacency, ('adjacency',order))
    hist[adjacency] = hist.get(adjacency,0)+1
check(hist == {0:14,1:40,2:48,3:16,4:2}, ('histogram',hist))
print(json.dumps({'status':'PASS','four_term_graphs':4096,'semantic_queries_and_witness_checks':witness_checks,'permutations':120,'prefix_models_checked':600,'adjacency_histogram':hist,'scope':'positive universal inclusion, nonreflexive queries; no human deception experiment'},sort_keys=True))
