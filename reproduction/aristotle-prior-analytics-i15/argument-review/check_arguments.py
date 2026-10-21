"""Independent set-semantic checks for explicit modern I.15 teaching theorems.

No claim of historical uniqueness or infinite-model verification. All assertions
use explicit exceptions so optimized Python retains checks. Standard library.
"""
import json
from itertools import product
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import Model

counts = {}
def checked(ok, name):
    counts[name] = counts.get(name, 0) + 1
    if not ok:
        raise RuntimeError(name)

for n, k in ((1, 1), (1, 2), (2, 2), (1, 3)):
    subsets = tuple(frozenset(x for x in range(n) if mask & (1 << x)) for mask in range(1 << n))
    for flat in product(range(1 << n), repeat=3*k):
        ws = tuple(tuple(subsets[i] for i in flat[3*w:3*w+3]) for w in range(k))
        masks = tuple(tuple(flat[3*w:3*w+3]) for w in range(k))
        for actual in range(k):
            m = Model(n, masks, actual)
            counts['model_actual_configurations'] = counts.get('model_actual_configurations', 0)+1
            def weak(p,x,sign):
                return any((x in w[p]) == sign for w in ws)
            def strong(p,x):
                return weak(p,x,True) and weak(p,x,False)
            def modal(p,s,mode,quantity):
                vals = [(strong(p,x) if mode=='K' else weak(p,x,mode=='M+')) for x in ws[actual][s]]
                return all(vals) if quantity=='all' else any(vals)
            for p,s in product(range(3), repeat=2):
                for mode,q in product(('K','M+','M-'),('all','some')):
                    checked(modal(p,s,mode,q)==m.modal('ABC'[p],'ABC'[s],mode,q), 'independent_modal_values')
                for sign in (False,True):
                    joint=any(all((x in w[p])==sign for x in ws[actual][s]) for w in ws)
                    checked(joint==m.jointly_possible('ABC'[p],'ABC'[s],sign),'independent_joint_values')
            A,B,C=ws[actual]
            for q in ('all','some'):
                minor= C<=B if q=='all' else bool(C&B)
                if modal(0,1,'K','all') and minor:
                    checked(modal(0,2,'K',q),'direct_range_theorems')
                for neg in (False,True):
                    stable=all(not(w[0]&w[1]) if neg else w[1]<=w[0] for w in ws)
                    if stable and modal(1,2,'K',q):
                        checked(modal(0,2,'M-' if neg else 'M+',q),'stable_weak_theorems')
                    guards=[strong(1,x) and weak(0,x,neg) for x in C]
                    guard=all(guards) if q=='all' else any(guards)
                    checked(guard==m.reverse_strong_guard('A','B','C',neg,q),'same_object_guard_values')
                    if stable and guard:
                        checked(modal(0,2,'K',q),'extra_witness_strong_theorems')

# General-proof illustrations, independently constructed as sets of worlds.
W=set(range(4))
for ps in product((False,True),repeat=4):
    P={w for w in W if ps[w]}
    for qs in product((False,True),repeat=4):
        Q={w for w in W if qs[w]}
        if P<=Q and P:
            checked(bool(Q),'possibility_preservation')
        if P<=Q and P==W:
            checked(Q==W,'necessity_preservation')
checked({1}<={0,1} and 0 not in {1} and 0 in {0,1},'falsity_not_preserved')
checked(bool({0}) and bool({1}) and not({0}&{1}), 'separate_not_joint')
# Neither overall modal possibilities nor actual truth licenses keeping a background.
K={0}; H={1}; R=set()
checked((K&H)<=R and 0 in K and bool(H) and not R, 'background_countermodel')
# Nonempty actual terms in the reversed-branch failure.
m=Model(2,((1,1,2),(1,3,2)))
checked(all(m.extension(t) for t in 'ABC') and m.categorical('A','B') and m.modal('B','C') and not m.modal('A','C','M+'), 'nonempty_snapshot_failure')
# Quantifier swap failure with two actual subject objects.
m=Model(2,((1,0,3),(2,0,3)))
checked(m.modal('A','C') and not m.jointly_possible('A','C') and not m.jointly_possible('A','C',False),'pointwise_not_joint_countermodel')
print(json.dumps({'status':'passed','scope':'independent finite set semantics; general proof remains textual','counts':counts},ensure_ascii=False,sort_keys=True,indent=2))
