"""Original finite inclusion-graph teaching model for Prior Analytics II.17.
An edge (s,p) represents All s are p. Impossibility is an external label.
No explosion, negative syllogistic, truth certification or causal inference.
"""
from itertools import combinations
import json


def normalize(edges, nodes):
    ns = tuple(nodes)
    if not ns or any(not isinstance(x, str) or not x for x in ns) or len(set(ns)) != len(ns):
        raise ValueError('nodes must be distinct nonempty strings')
    es = set()
    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError('edge must be a pair')
        a, b = edge
        if a not in ns or b not in ns:
            raise ValueError('edge endpoint outside nodes')
        es.add((a, b))
    return frozenset(es), ns


def pair(value, nodes):
    if not isinstance(value, (tuple, list)) or len(value) != 2 or any(x not in nodes for x in value):
        raise ValueError('pair endpoints must be declared')
    return tuple(value)


def closure(edges, nodes):
    es, ns = normalize(edges, nodes)
    out = set(es) | {(x, x) for x in ns}
    for k in ns:
        for i in ns:
            for j in ns:
                if (i, k) in out and (k, j) in out:
                    out.add((i, j))
    return frozenset(out)


def minimal_supports(edges, target, nodes):
    es, ns = normalize(edges, nodes)
    start, finish = pair(target, ns)
    if start == finish:
        return (frozenset(),)
    found = set()
    def visit(here, seen, used):
        if here == finish:
            found.add(frozenset(used))
            return
        for a, b in sorted(es):
            if a == here and b not in seen:
                visit(b, seen | {b}, used + [(a,b)])
    visit(start, {start}, [])
    return tuple(sorted((s for s in found if not any(t < s for t in found)),
                        key=lambda x: (len(x), sorted(x))))


def analyze(edges, hypothesis, target, nodes, proof_path=None):
    es, ns = normalize(edges, nodes)
    h, t = pair(hypothesis, ns), pair(target, ns)
    if h not in es:
        raise ValueError('hypothesis must be a current premise edge')
    used = None
    if proof_path is not None:
        pp = tuple(proof_path)
        if not pp or pp[0] != t[0] or pp[-1] != t[1] or any(x not in ns for x in pp):
            raise ValueError('proof endpoints invalid')
        proof_edges = tuple(zip(pp, pp[1:]))
        if any(e not in es for e in proof_edges):
            raise ValueError('proof uses unavailable edge')
        used = h in proof_edges
    before = t in closure(es, ns)
    after = t in closure(es - {h}, ns)
    supports = minimal_supports(es, t, ns)
    return {'before': before, 'after_deleted': after,
            'necessary_within_graph': before and not after,
            'supports': [[list(e) for e in sorted(s)] for s in supports],
            'proof_uses_hypothesis': used}


def scenarios():
    records = {}
    down = [('B','A'),('C','B'),('D','C')]
    up = [('B','A'),('A','E'),('E','F')]
    cases = [
      ('down_irrelevant',down,('B','A'),('D','B'),'ABCD',['D','C','B']),
      ('down_necessary',down,('B','A'),('D','A'),'ABCD',['D','C','B','A']),
      ('up_irrelevant',up,('B','A'),('A','F'),'ABEF',['A','E','F']),
      ('up_necessary',up,('B','A'),('B','F'),'ABEF',['B','A','E','F']),
      ('disconnected',[('B','A'),('Y','X'),('Z','Y')],('B','A'),('Z','X'),'ABXYZ',['Z','Y','X']),
      ('used_but_redundant',down+[('C','K'),('K','A')],('B','A'),('D','A'),'ABCDK',['D','C','B','A']),
      ('not_initially_derived',[('B','A')],('B','A'),('C','A'),'ABC',None),
      ('identity',[('B','A')],('B','A'),('A','A'),'AB',['A']),
      ('cyclic_detour',[('B','A'),('A','B'),('C','A')],('B','A'),('C','A'),'ABC',['C','A','B','A'])]
    for name, es, h, t, ns, proof in cases:
        records[name] = analyze(es,h,t,ns,proof)
    original = analyze(down,('B','A'),('D','A'),'ABCD')
    replacement = [('C','K'),('K','A'),('D','C')]
    records['replacement_not_deletion'] = {
        'original_after_deleted': original['after_deleted'],
        'changed_background_derives_target': ('D','A') in closure(replacement,'ABCDK'),
        'different_premises': True}
    return records


def exhaustive():
    ns = ('A','B','C')
    possible = [(a,b) for a in ns for b in ns if a != b]
    counts = {'graphs': 64, 'deletion_records': 0, 'initially_derived': 0,
              'still_derived': 0, 'necessary': 0, 'support_equivalence_checks': 0}
    for mask in range(64):
        es = frozenset(e for i,e in enumerate(possible) if mask >> i & 1)
        for h in sorted(es):
            for a in ns:
                for b in ns:
                    r = analyze(es,h,(a,b),ns)
                    counts['deletion_records'] += 1
                    counts['initially_derived'] += r['before']
                    counts['still_derived'] += r['after_deleted']
                    counts['necessary'] += r['necessary_within_graph']
                    avoiding = any(list(h) not in s for s in r['supports'])
                    if avoiding != r['after_deleted']:
                        raise RuntimeError('support/deletion mismatch')
                    counts['support_equivalence_checks'] += 1
    return counts

if __name__ == '__main__':
    print(json.dumps({'scope':'finite affirmative inclusion graph; no truth or causality certification',
                      'scenarios':scenarios(),'exhaustive':exhaustive()},ensure_ascii=False,indent=2,sort_keys=True))
