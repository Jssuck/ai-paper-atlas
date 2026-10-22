"""Independent finite checks of I.25 teaching lemmas; no author-code imports.
These executions do not prove their universally quantified counterparts.
"""
import json
import platform
import sys
from itertools import combinations

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def reachable(vertices, edges):
    # A path-search oracle, not the closed count formula.
    out = set()
    for origin in vertices:
        pending = [v for u, v in edges if u == origin]
        visited = set()
        while pending:
            v = pending.pop()
            if v in visited:
                continue
            visited.add(v)
            out.add((origin, v))
            pending.extend(w for u, w in edges if u == v)
    return out

def counts(tree):
    if tree is None:
        return 0, 1, 0, 1
    left, right = tree
    lk, ll, ls, ln = counts(left)
    rk, rl, rs, rn = counts(right)
    return 1 + lk + rk, ll + rl, 2 + ls + rs, 1 + ln + rn

def shapes(k):
    if k == 0:
        return (None,)
    return tuple((left, right) for i in range(k)
                 for left in shapes(i) for right in shapes(k - 1 - i))

def run():
    path_cases = insertion_cases = append_cases = pair_checks = 0
    examples = []
    for n in range(2, 41):
        vertices = tuple(range(n))
        edges = set(zip(vertices, vertices[1:]))
        facts = reachable(vertices, edges)
        conclusions = facts - edges
        expected = {(i, j) for i, j in combinations(vertices, 2) if j-i >= 2}
        require(conclusions == expected, 'nonadjacent characterization')
        require(len(edges) == n-1, 'edge count')
        require(len(conclusions) == (n-1)*(n-2)//2, 'quadratic count')
        require((n % 2) != (len(edges) % 2), 'opposite parity')
        require((len(conclusions)>n and len(conclusions)>len(edges)) == (n>=5), 'threshold')
        path_cases += 1
        pair_checks += len(facts)
        if n <= 7:
            examples.append({'terms':n, 'premises':len(edges), 'nonadjacent_conclusions':len(conclusions)})
        expanded = vertices + (n,)
        new_edges = set(zip(expanded, expanded[1:]))
        new_facts = reachable(expanded, new_edges)
        new_conclusions = new_facts - new_edges
        require(len(new_conclusions)-len(conclusions)==n-1, 'append increment')
        require(new_conclusions-conclusions == {(i,n) for i in range(n-1)}, 'append new pairs')
        append_cases += 1
        for slot in range(1, n):
            expanded = vertices[:slot]+(n,)+vertices[slot:]
            new_edges=set(zip(expanded,expanded[1:]))
            new_facts=reachable(expanded,new_edges)
            new_conclusions=new_facts-new_edges
            old_boundary=(slot-1,slot)
            require(conclusions <= new_conclusions, 'preserved old conclusions')
            require({p for p in new_facts if n not in p}==facts, 'old facts unchanged')
            added=new_conclusions-conclusions
            require(len(added)==n-1, 'interior increment')
            require(old_boundary in added, 'old premise becomes derived')
            require(len({p for p in added if n in p})==n-2, 'new-term derived pairs')
            insertion_cases += 1
    tree_cases=0
    for k in range(9):
        for t in shapes(k):
            steps, leaves, slots, nodes=counts(t)
            require(steps==k and leaves==k+1 and slots==2*k and nodes==2*k+1, 'full binary tree')
            tree_cases+=1
    # Three concrete boundaries: reachability counts alone do not characterize a chain.
    diamond={(0,1),(0,2),(1,3),(2,3)}
    require(len(reachable(range(4),diamond)-diamond)==1, 'branch counterexample')
    cycle={(0,1),(1,2),(2,0)}
    require(len(reachable(range(3),cycle))==9, 'cycle includes reflexive paths')
    disconnected={(0,1),(2,3)}
    require(reachable(range(4),disconnected)==disconnected, 'disconnected no bridge')
    return {'python':platform.python_version(),'optimization':sys.flags.optimize,
            'path_cases':path_cases,'append_cases':append_cases,'interior_insertions':insertion_cases,
            'reachable_pair_checks':pair_checks,'binary_tree_shapes':tree_cases,
            'boundary_graphs':3,'examples':examples,'passed':True,
            'limits':'Finite independent checks, not general proofs, historical semantics, or an arbitrary proof-system checker.'}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
