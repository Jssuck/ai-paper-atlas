"""Independent n=4 graph oracle: DFS and permutation enumeration, not Floyd-Warshall/DP."""
import itertools, json, sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
from intervals import StrictOrder, enumerate_forward_dags, report

def check(c,msg):
    if not c: raise RuntimeError(msg)

def oracle(n,edges):
    adj={i:[] for i in range(n)}
    for a,b in edges: adj[a].append(b)
    reach=set()
    for a in range(n):
        todo=list(adj[a]); seen=set()
        while todo:
            b=todo.pop()
            if b not in seen:
                seen.add(b); todo.extend(adj[b])
        reach.update((a,b) for b in seen)
    if any((a,a) in reach for a in range(n)): return None
    intervals=[]
    for a,b in sorted(reach):
        mid=tuple(v for v in range(n) if (a,v) in reach and (v,b) in reach)
        full=all((u,v) in reach or (v,u) in reach for u,v in itertools.combinations(mid,2))
        longest=1
        for k in range(len(mid)+1):
            for perm in itertools.permutations(mid,k):
                seq=(a,)+perm+(b,)
                if all((u,v) in reach for u,v in zip(seq,seq[1:])): longest=max(longest,k+1)
        intervals.append((a,b,mid,full,longest))
    return frozenset(reach), intervals

n=4; slots=[(a,b) for a in range(n) for b in range(n) if a!=b]
dags=cyclic=checks=0; closures=set(); forward_closures=set(); forward_i=forward_total=forward_nontotal=0
for mask in range(1<<len(slots)):
    edges=[e for j,e in enumerate(slots) if mask>>j&1]
    expected=oracle(n,edges)
    if expected is None:
        cyclic+=1
        try: StrictOrder(n,edges)
        except ValueError: pass
        else: raise RuntimeError('cycle accepted')
        continue
    dags+=1; closure, intervals=expected; closures.add(closure)
    actual=StrictOrder(n,edges); check(actual.relation==closure,'closure mismatch')
    forward=all(a<b for a,b in edges)
    if forward: forward_closures.add(closure)
    for a,b,mid,total,longest in intervals:
        got=actual.interval(a,b); checks+=1
        check(got['middle']==list(mid),'middle mismatch')
        check(got['is_total']==total,'total mismatch')
        check(got['longest_edges']==longest,'distance mismatch')
        if total: check(len(mid)==longest-1,'finite total interval identity')
        if forward:
            forward_i+=1; forward_total+=int(total); forward_nontotal+=int(not total)
expected_counts=(len(forward_closures),forward_i,forward_total,forward_nontotal)
r=enumerate_forward_dags(4)
check(expected_counts==(r['distinct_transitive_closures'],r['ordered_interval_occurrences'],r['total_interval_occurrences'],r['nontotal_interval_occurrences']),'count mismatch')
saved=json.loads((root/'results.json').read_text())
check(report()==saved,'saved results mismatch')
print(json.dumps({'all_loopless_labeled_digraphs':4096,'acyclic_graphs':dags,'cyclic_graphs_rejected':cyclic,'distinct_labeled_strict_orders':len(closures),'interval_comparisons':checks,'fixed_order_forward_counts':{'closures':len(forward_closures),'interval_occurrences':forward_i,'total':forward_total,'nontotal':forward_nontotal},'failures':0,'method':'Independent DFS closure plus exhaustive permutation chains; all 4096 loopless labeled digraphs on 4 vertices.'},indent=2))
