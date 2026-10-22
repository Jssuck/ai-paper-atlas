"""Independent finite audit: per-object membership truth, not set operations."""
import itertools, json, sys
from model import Prop, holds, analyze, find_countermodel, candidate_completions, implication_chain_rows

def require(v, label):
    if not v: raise RuntimeError(label)

def oracle(p, values, size):
    rows=[(bool(values[p.subject]&(1<<i)),bool(values[p.predicate]&(1<<i))) for i in range(size)]
    if p.kind=='A': return all(not x or y for x,y in rows)
    if p.kind=='E': return all(not(x and y) for x,y in rows)
    if p.kind=='I': return any(x and y for x,y in rows)
    if p.kind=='O': return any(x and not y for x,y in rows)
    raise ValueError('bad oracle kind')

def main():
    semantic_checks=0
    for n in (1,2,3):
        for bits in itertools.product(range(2**n),repeat=3):
            d=dict(zip(('M','P','S'),bits)); ext={t:{i for i in range(n) if b&(1<<i)} for t,b in d.items()}
            for k in 'AEIO':
                for s,p in itertools.product(d,repeat=2):
                    q=Prop(k,s,p)
                    require(holds(q,ext)==oracle(q,d,n),'semantic disagreement');semantic_checks+=1
    models=[(n,dict(zip(('M','P','S'),bits))) for n in (1,2,3) for bits in itertools.product(range(2**n),repeat=3)]
    orientations=[(('M','P'),('S','M'),1),(('P','M'),('S','M'),2),(('M','P'),('M','S'),3),(('P','M'),('M','S'),None)]
    configurations=shape_checks=countermodels=no_countermodels=0
    for major,minor,figure in orientations:
        for kinds in itertools.product('AEIO',repeat=3):
            ps=[Prop(kinds[0],*major),Prop(kinds[1],*minor)]; goal=Prop(kinds[2],'S','P')
            a=analyze(ps,goal)
            require(a['figure']==figure and a['mood']==''.join(kinds),'shape')
            require(a==analyze(ps[::-1],goal),'order')
            names={'M':'中','P':'谓','S':'主'}
            renamed=[Prop(p.kind,names[p.subject],names[p.predicate]) for p in ps]
            require(analyze(renamed,Prop(goal.kind,'主','谓'))['figure']==figure,'rename');shape_checks+=3
            for mask in range(8):
                ne=tuple(t for i,t in enumerate(('M','P','S')) if mask&(1<<i))
                valid_models=[(n,d) for n,d in models if all(d[t] for t in ne)]
                premises_true=[(n,d) for n,d in valid_models if all(oracle(p,d,n) for p in ps)]
                failures=[(n,d) for n,d in premises_true if not oracle(goal,d,n)]
                r=find_countermodel(ps,goal,max_size=3,nonempty=ne)
                require(bool(failures)==(r['status']=='countermodel_found'),'finite result')
                if failures:
                    countermodels+=1;n=r['universe_size'];d={t:sum(1<<i for i in xs) for t,xs in r['model'].items()}
                    require(all(d[t] for t in ne),'existence witness');require(all(oracle(p,d,n) for p in ps) and not oracle(goal,d,n),'countermodel witness')
                else:
                    no_countermodels+=1
                    require(r['checked']==584 and r['admissible']==len(valid_models) and r['premise_models']==len(premises_true),'counts')
                configurations+=1
    known=Prop('A','M','P');goal=Prop('I','S','P');candidate=Prop('A','M','S')
    completion=candidate_completions(known,goal,[candidate,candidate],nonempty=(x for x in ['M']))
    require(completion[0]==completion[1],'one-shot constraint preserved')
    require(all(x['status']=='hypothesis_not_fact' for x in completion),'hypothesis label')
    require(completion[0]['finite_check']['status']=='no_countermodel_in_bound','constraint effect')
    require(find_countermodel([known,candidate],goal)['status']=='countermodel_found','empty counterexample')
    invalid_calls=[lambda:Prop('X','S','P'),lambda:Prop('A','','P'),lambda:analyze(['text'],goal),lambda:find_countermodel([known],goal,True),lambda:find_countermodel([known],goal,0),lambda:find_countermodel([known],goal,5),lambda:find_countermodel([known],goal,nonempty=('unknown',)),lambda:candidate_completions(known,goal,['text'])]
    for call in invalid_calls:
        try:call()
        except (TypeError,ValueError):pass
        else:raise RuntimeError('invalid accepted')
    rows=implication_chain_rows();require(len(rows)==8,'boolean size')
    for r in rows:
        h,n,s=r['H'],r['N'],r['S'];require(r['premises']==(not(h and not n) and not(n and not s)),'boolean premises');require(r['conclusion']==(not(h and not s)),'boolean conclusion');require(not r['premises'] or r['conclusion'],'boolean inference')
    print(json.dumps({'status':'PASS','semantic_checks':semantic_checks,'shape_order_rename_checks':shape_checks,'finite_configurations':configurations,'configurations_with_countermodel':countermodels,'configurations_no_countermodel_in_bound':no_countermodels,'models_per_unrestricted_check':584,'invalid_inputs_rejected':len(invalid_calls),'generator_constraint_regression':'PASS','boolean_rows':8,'scope':'finite domains 1..3, four orientations, all 64 AEIO moods, eight existence profiles; not a general theorem'},indent=2))
if __name__=='__main__':main()
