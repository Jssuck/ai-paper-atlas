"""Independent element-membership oracle and targeted fault checks."""
from pathlib import Path
import sys, json, itertools, hashlib, platform, types
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
import modal as prod
checks=0

def check(value, label):
    global checks
    checks+=1
    if not value: raise RuntimeError(label)

def cat(q,S,P):
    if q=='A': return all(x in P for x in S)
    if q=='E': return all(x not in P for x in S)
    if q=='I': return any(x in P for x in S)
    return any(x not in P for x in S)

def oracle(n, worlds,q,s,p,sem):
    sets=[[{i for i in range(n) if w[t]//(2**i)%2} for t in range(3)] for w in worlds]
    if sem=='actual':return cat(q,sets[0][s],sets[0][p])
    if sem=='sentence':return all(cat(q,w[s],w[p]) for w in sets)
    subj=sets[0][s]
    if q=='A':return all(all(x in w[p] for w in sets) for x in subj)
    if q=='E':return all(all(x not in w[p] for w in sets) for x in subj)
    if q=='I':return any(all(x in w[p] for w in sets) for x in subj)
    return any(all(x not in w[p] for w in sets) for x in subj)

modes={'Darapti':('A','A','I'),'Felapton':('E','A','O'),'Disamis':('I','A','I'),'Datisi':('A','I','I'),'Bocardo':('O','A','O'),'Ferison':('E','I','O')}
rows={(sem,name,side):[0,0] for sem in ('anchored','sentence') for name in modes for side in ('major','minor')}
for vals in itertools.product(range(4),repeat=6):
    ws=(vals[:3],vals[3:]);m=prod.Model(2,ws)
    for sem,q,s,p in itertools.product(('actual','anchored','sentence'),'AEIO',range(3),range(3)):
        check(prod.evaluate(m,q,s,p,sem)==oracle(2,ws,q,s,p,sem),'evaluator oracle')
    for key,count in rows.items():
        sem,name,side=key;a,b,c=modes[name]
        pre=bool(ws[0][2]) and oracle(2,ws,a,2,0,sem if side=='major' else 'actual') and oracle(2,ws,b,2,1,sem if side=='minor' else 'actual')
        check(prod.satisfies(m,name,side,sem)==pre,'premise oracle')
        if pre:
            count[0]+=1
            count[1]+=not oracle(2,ws,c,1,0,sem)
    shared=any(all((w[0]//2**i)%2 and (w[1]//2**i)%2 for w in ws) for i in range(2))
    check(prod.fixed_shared_witness(m,0,1)==shared,'shared oracle')

saved=json.loads((BASE/'results.json').read_text())
check(saved['models']==4096,'saved population')
for r in saved['rows']:
    key=(r['semantics'],r['mode'],r['necessary']);count=rows[key]
    check([r['premise_models'],r['countermodels']]==count,'saved row counts')
    check(r['finite_valid']==(key[0]=='anchored' and key[2]=='major'),'six and eighteen')
    if count[1]:
        cm=r['minimum_domain_countermodel'];check(cm['domain_size']==1,'minimal domain nonempty')
        worlds=tuple(tuple(sum(2**i for i in w[t]) for t in 'ABC') for w in cm['worlds'])
        a,b,c=modes[key[1]];sem,_,side=key
        check(bool(worlds[0][2]) and oracle(1,worlds,a,2,0,sem if side=='major' else 'actual') and oracle(1,worlds,b,2,1,sem if side=='minor' else 'actual') and not oracle(1,worlds,c,1,0,sem),'reported countermodel')

invalid=0
def reject(call,exc=(ValueError,TypeError)):
    global invalid
    invalid+=1
    try:call()
    except exc:return
    raise RuntimeError('invalid input accepted')
for n in (0,-1,True,False,1.5,'2',None): reject(lambda n=n:prod.Model(n,((0,0,0),)))
for ws in ((),[],None,((0,0),),((0,0,0,0),),([0,0,0],),((0,0,-1),),((0,0,4),),((0,0,True),),((0,0,0.5),)):
    reject(lambda ws=ws:prod.Model(2,ws))
m=prod.Model(2,((3,2,1),(1,0,2)))
for t in (-1,3,True,False,1.5,'1',None):
    for method in (m.actual,m.stable,m.possible):reject(lambda method=method,t=t:method(t))
    reject(lambda t=t:prod.evaluate(m,'I',t,0));reject(lambda t=t:prod.evaluate(m,'I',0,t))
for q in ('Z','',None,1,[]):reject(lambda q=q:prod.evaluate(m,q,0,1))
for sem in ('',None,1,'necessary'):reject(lambda sem=sem:prod.evaluate(m,'A',0,1,sem))
for n,w in ((0,1),(1,0),(-1,2),(2,-1),(True,2),(2,False),(2.0,2),(2,1.5)):
    reject(lambda n=n,w=w:list(prod.models(n,w)))
for s,p in ((True,1),(1,False),(-1,0),(0,-1),(1.5,0),(0,None)):reject(lambda s=s,p=p:prod.categorical('A',s,p))
reject(lambda:prod.evaluate(None,'A',0,1));reject(lambda:prod.satisfies(m,'unknown','major','anchored'));reject(lambda:prod.satisfies(m,'Darapti','wrong','anchored'));reject(lambda:prod.satisfies(m,'Darapti','major','actual'))

source=(BASE/'modal.py').read_text()
mutations=[
('stable_union','mask &= w[term]','mask |= w[term]'),
('possible_intersection','mask |= w[term]','mask &= w[term]'),
('actual_last','return self.worlds[0][term]','return self.worlds[-1][term]'),
('A_overlap','return s & ~p == 0','return bool(s & p)'),
('E_overlap','return s & p == 0','return bool(s & p)'),
('I_disjoint','return bool(s & p)','return s & p == 0'),
('O_inclusion','return bool(s & ~p)','return s & ~p == 0'),
('sentence_any','return all(categorical','return any(categorical'),
('anchor_subject_stable','m.actual(subject),p','m.stable(subject),p'),
('anchor_predicate_actual',"p = m.stable(predicate) if kind in ('A','I') else m.possible(predicate)","p = m.actual(predicate)"),
('swap_necessary_side',"necessary_side=='major'","necessary_side=='minor'"),
('drop_nonempty','return bool(m.actual(2)) and evaluate','return True and evaluate'),
('fixed_union','m.stable(s) & m.stable(p)','m.stable(s) | m.stable(p)')]
detected=[]
for name,old,new in mutations:
    if old not in source:raise RuntimeError('mutation target absent '+name)
    module=types.ModuleType('mutation_'+name);sys.modules[module.__name__]=module
    exec(compile(source.replace(old,new,1),'<targeted mutation>','exec'),module.__dict__)
    found=False
    for vals in itertools.product(range(2),repeat=6):
        ws=(vals[:3],vals[3:]);mm=module.Model(1,ws)
        for sem,q,s,p in itertools.product(('actual','anchored','sentence'),'AEIO',range(3),range(3)):
            if module.evaluate(mm,q,s,p,sem)!=oracle(1,ws,q,s,p,sem):found=True;break
        if found:break
        expected_shared=all(w[0] and w[1] for w in ws)
        if module.fixed_shared_witness(mm,0,1)!=expected_shared:found=True;break
        for sem,name2,side in itertools.product(('anchored','sentence'),modes,('major','minor')):
            a,b,c=modes[name2]
            pre=bool(ws[0][2]) and oracle(1,ws,a,2,0,sem if side=='major' else 'actual') and oracle(1,ws,b,2,1,sem if side=='minor' else 'actual')
            if module.satisfies(mm,name2,side,sem)!=pre:found=True;break
        if found:break
    check(found,'undetected mutant '+name);detected.append(name)

out={'status':'PASS','checks':checks,'invalid_input_calls':invalid,'models':4096,'configurations':24,'anchored_major_valid':6,'other_configurations_with_countermodels':18,'targeted_mutants_detected':detected,'rows':[{'semantics':k[0],'mode':k[1],'necessary':k[2],'premise_models':v[0],'countermodels':v[1]} for k,v in rows.items()]}
print(json.dumps(out,ensure_ascii=False,indent=2))
