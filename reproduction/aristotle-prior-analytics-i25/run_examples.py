"""Deterministic author checks. Fail explicitly even under Python -O/-OO."""
import json
from itertools import product
from model import chain_report, closure, verify_certificate, proof_tree_stats

def check(ok, message):
    if not ok: raise RuntimeError(message)

def bfs(edges):
    vertices={v for e in edges for v in e}
    result=set()
    for s in vertices:
        seen=set()
        todo=[b for a,b in edges if a==s]
        while todo:
            x=todo.pop()
            if x in seen: continue
            seen.add(x)
            todo.extend(b for a,b in edges if a==x and b not in seen)
        result.update((s,x) for x in seen)
    return result

def run():
    chains=[]; certificates=0; insertions=0
    for n in range(2,31):
        ts=[f'T{i}' for i in range(n)]
        r=chain_report(ts)
        check(r['premise_count']==n-1,'premises')
        check(r['conclusion_count']==(n-1)*(n-2)//2,'conclusions')
        for target in r['conclusions']:
            check(verify_certificate(r['premises'],r['steps'],target),'certificate')
            certificates+=1
        old=set(r['conclusions'])
        for position in range(n+1):
            new=ts[:position]+['X']+ts[position:]
            nr=chain_report(new)
            check(old <= set(nr['conclusions']),'old conclusions retained')
            check(len(set(nr['conclusions'])-old)==n-1,'insertion difference')
            insertions+=1
        tree=('given',ts[-2],ts[-1])
        for i in reversed(range(n-2)):
            tree=('via',('given',ts[i],ts[i+1]),tree)
        stat=proof_tree_stats(tree)
        check(stat['inferences']==n-2,'tree inferences')
        check(stat['leaf_occurrences']==n-1,'tree leaves')
        check(stat['premise_slots']==2*(n-2),'tree slots')
        chains.append({'n':n,'premises':n-1,'distinct_nonadjacent_conclusions':r['conclusion_count'],
                       'one_target_inferences':stat['inferences'],'one_target_premise_slots':stat['premise_slots']})
    all_edges=list(product('ABC', repeat=2))
    for mask in range(1<<len(all_edges)):
        es={e for i,e in enumerate(all_edges) if mask>>i&1}
        check(closure(es)==bfs(es),'closure vs traversal')
    base=chain_report(list('ABC')); inserted=chain_report(list('ABXC'))
    t=('via',('given','A','B'),('given','B','A'))
    shared=('via',t,t)
    return {'chain_range':[2,30],'chains_checked':len(chains),'conclusion_certificates_checked':certificates,
            'insertions_checked':insertions,'three_label_graphs_checked':512,'chains':chains,
            'internal_insertion_example':{'old':base,'new':inserted,'newly_classified_conclusions':sorted(set(inserted['conclusions'])-set(base['conclusions']))},
            'branch_counterexample':{'edges':[['A','B'],['A','C']],'closure':sorted(closure([('A','B'),('A','C')]))},
            'cycle_counterexample':{'edges':[['A','B'],['B','A']],'closure':sorted(closure([('A','B'),('B','A')]))},
            'shared_subtree':{'tree_occurrence_counts':proof_tree_stats(shared),'unique_node_objects':4,'unique_inference_objects':2,
                              'warning':'The repeated subtree is unfolded; counting unique DAG objects does not obey the same tree leaf identity.'},
            'status':'passed','limit':'Finite checks of an explicit positive-length transitivity model, not a proof of the counting theorems or unique ancient semantics.'}

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
