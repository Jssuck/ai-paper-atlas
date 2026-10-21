"""Independent set-based finite sanity checks, no author-module imports.
The general arguments are supplied in the article; enumeration is not proof.
"""
from itertools import product
from collections import Counter
import json

counts = Counter()

def check(truth, label):
    counts['checks'] += 1
    if not truth:
        raise RuntimeError(label)

def semantic(worlds, actual):
    at = worlds[actual]
    def mod(p, s, mode, quantity='all'):
        def one(x):
            vals = [x in w[p] for w in worlds]
            return {'N+':all(vals), 'N-':not any(vals),
                    'M+':any(vals), 'M-':not all(vals),
                    'K':any(vals) and not all(vals)}[mode]
        return (all if quantity == 'all' else any)(one(x) for x in at[s])
    def cat(p,s,negative=False,quantity='all'):
        return (all if quantity == 'all' else any)((x not in at[p]) if negative else (x in at[p]) for x in at[s])
    def sym(p,s):
        return mod(p,s,'N-') and mod(s,p,'N-')
    def stable(p,s):
        return all(w[s] <= w[p] for w in worlds)
    return mod,cat,sym,stable

def inspect(worlds,actual):
    counts['configurations'] += 1
    m,c,e,s=semantic(worlds,actual)
    check(e(0,1)==e(1,0),'symmetry')
    for q in ('all','some'):
        if m(0,1,'K') and m(1,2,'N+',q):
            counts['direct_'+q]+=1
            check(m(0,2,'K',q),'direct '+q)
        if s(0,1) and m(1,2,'K',q):
            counts['positive_bridge_'+q]+=1
            check(m(0,2,'M+',q),'bridge '+q)
        if e(0,1) and m(1,2,'K',q):
            counts['negative_'+q]+=1
            check(c(0,2,True,q),'actual negative '+q)
            check(m(0,2,'M-',q),'weak negative '+q)
        if e(0,1) and m(1,2,'M+',q):
            counts['negative_weaker_input_'+q]+=1
            check(c(0,2,True,q),'positive possibility alone enough '+q)
        if m(0,1,'N+') and m(1,2,'K',q) and not m(0,2,'M+',q):
            counts['local_positive_failure_'+q]+=1
        if m(0,1,'N-') and m(1,2,'K',q) and not c(0,2,True,q):
            counts['oneway_negative_failure_'+q]+=1
        if e(0,1) and m(1,2,'K',q) and not m(0,2,'N-',q):
            counts['not_necessary_negative_'+q]+=1
    counts['stable_not_local'] += s(0,1) and not m(0,1,'N+')
    counts['local_not_stable'] += m(0,1,'N+') and not s(0,1)

for n,k in ((1,1),(1,2),(1,3),(2,1),(2,2)):
    subsets=[frozenset(i for i in range(n) if mask & (1<<i)) for mask in range(1<<n)]
    for raw in product(subsets,repeat=3*k):
        worlds=tuple(tuple(raw[3*j:3*j+3]) for j in range(k))
        for actual in range(k): inspect(worlds,actual)

# Explicit nonempty counterexample to modal negative strengthening.
worlds=((frozenset({0}),frozenset({1}),frozenset({2})),
        (frozenset({0,2}),frozenset({1,2}),frozenset({2})))
m,c,e,s=semantic(worlds,0)
check(e(0,1) and m(1,2,'K') and c(0,2,True) and not m(0,2,'N-'),'nonempty E* example')
# Simultaneous possibility is stronger than pointwise possibility.
w=((frozenset({0}),frozenset(),frozenset({0,1})),
   (frozenset({1}),frozenset(),frozenset({0,1})))
m,c,e,s=semantic(w,0)
check(m(0,2,'K') and not any(w[0][2] <= row[0] for row in w),'pointwise not joint')
check(counts['configurations']==9928,'enumeration size')
for label in ('stable_not_local','local_not_stable','local_positive_failure_all','oneway_negative_failure_all','not_necessary_negative_all'):
    check(counts[label]>0,'missing limit '+label)
print(json.dumps({'scope':'1 object with 1–3 worlds; 2 objects with 1–2 worlds; every actual index; repeated/isomorphic configurations retained',
                  'counts':dict(sorted(counts.items())),
                  'general_proof_claim':False},ensure_ascii=False,indent=2))
