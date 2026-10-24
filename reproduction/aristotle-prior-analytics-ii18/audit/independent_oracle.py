"""Independent truth-assignment audit of II.18 teaching reconstructions.
Uses exhaustive models and path enumeration, not production backtracking.
"""
import itertools, json, sys
from pathlib import Path

def require(ok, message):
    if not ok: raise RuntimeError(message)

def enumerate_tree():
    nodes = ('D','E','F','G','A','B','C')
    edges = {'A':('D','E'), 'B':('F','G'), 'C':('A','B')}
    rows=[]
    for bits in itertools.product((False,True),repeat=7):
        v=dict(zip(nodes,bits))
        valid=all(not all(v[p] for p in ps) or v[c] for c,ps in edges.items())
        if not valid: continue
        paths=[]
        for mid, leaves in (('A',('D','E')),('B',('F','G'))):
            for leaf in leaves:
                if not v['C'] and not v[mid] and not v[leaf]: paths.append(['C',mid,leaf])
        require(v['C'] or bool(paths),'false root lacks false path')
        rows.append({'values':v,'false_paths':paths})
    return rows

def generic_chain(n):
    count=false=0
    for bits in itertools.product((False,True),repeat=2*n+1):
        # Each node i uses previous output (or initial leaf) and new leaf.
        prev=bits[0]; leaves=[prev]; admissible=True
        for i in range(n):
            leaf,out=bits[2*i+1:2*i+3];leaves.append(leaf)
            if prev and leaf and not out: admissible=False
            prev=out
        if admissible:
            count+=1
            if not prev:
                false+=1;require(not all(leaves),'chain counterexample')
    return {'steps':n,'admissible':count,'false_root':false}

def main():
    rows=enumerate_tree()
    false=[r for r in rows if not r['values']['C']]
    # More than one false leaf can be implicated: no uniqueness claim.
    require(any(len(r['false_paths'])==4 for r in false),'missing nonunique case')
    # True roots can coexist with false premises: no converse claim.
    require(any(r['values']['C'] and not all(r['values'][x] for x in 'DEFG') for r in rows),'missing converse boundary')
    # Invalid local step permits false conclusion from all true leaves.
    bad=dict.fromkeys('DEFGAB',True);bad['C']=False
    require(all(bad[x] for x in 'DEFG') and not bad['C'],'invalid boundary')
    out={'tree_assignments_total':128,'admissible':len(rows),'false_root':len(false),'path_counts':{str(i):sum(len(r['false_paths'])==i for r in false) for i in range(1,5)},'chains':[generic_chain(n) for n in range(1,5)],'rows':rows}
    import importlib.util
    production = Path(__file__).resolve().parents[1] / "publish/reproduction/aristotle-prior-analytics-ii18/diagnose.py"
    if not production.exists():
        production = Path(__file__).resolve().parents[1] / "diagnose.py"
    spec=importlib.util.spec_from_file_location("production",production)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    records=module.enumerate_records()
    require(len(records)==128,"production record count")
    for r in records:
        v=r['values']
        violations=sorted(c for c,p,q in [('A','D','E'),('B','F','G'),('C','A','B')] if v[p] and v[q] and not v[c])
        expected=[]
        if not violations and not v['C']:
            expected=sorted([['C',m,l] for m,ls in [('A','DE'),('B','FG')] for l in ls if not v[m] and not v[l]])
        require(r['valuation_condition_holds']==(not violations),"admissibility mismatch")
        require(r['violating_steps']==violations,"violation mismatch")
        require(r['false_leaf_paths']==expected,"path mismatch")
        require(r['false_leaves']==sorted({p[-1] for p in expected}),"leaf mismatch")
    # A false leaf behind a true intermediate is not on a wholly false path.
    v=dict(A=False,B=True,C=False,D=False,E=True,F=False,G=True)
    require(module.diagnose(module.STEPS,v,'C')['false_leaves']==['D'],"all-false-path scope")
    # One false leaf may be shared by two paths in an acyclic DAG.
    dag=(('A',('D','E')),('B',('D','F')),('C',('A','B')))
    r=module.diagnose(dag,dict(A=False,B=False,C=False,D=False,E=True,F=True),'C')
    require(r['false_leaves']==['D'] and len(r['false_leaf_paths'])==2,"shared leaf distinction")
    for steps,values,target in [
        ((('A',('B','D')),('B',('A','D'))),dict(A=False,B=False,D=True),'A'),
        (module.STEPS,dict.fromkeys('ABCDEF',True),'C'),
        (module.STEPS,dict.fromkeys('ABCDEFG',1),'C'),
        (module.STEPS,dict.fromkeys('ABCDEFG',True),'unknown')]:
        try: module.diagnose(steps,values,target)
        except ValueError: pass
        else: raise RuntimeError('invalid input was accepted')
    out['boundary_checks']=6
    out['production_records_cross_checked']=len(records)
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))
if __name__=='__main__':main()
