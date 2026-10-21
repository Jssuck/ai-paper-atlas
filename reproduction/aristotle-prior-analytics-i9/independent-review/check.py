"""Independent set-based checks of the explicitly stipulated educational semantics."""
import hashlib, importlib.util, itertools, json, pathlib, sys
BASE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
import modal as target
checks=0

def require(condition, label):
    global checks
    checks+=1
    if not condition:raise RuntimeError(label)

def extension(mask,n):return {x for x in range(n) if (mask // 2**x)%2}
def pair(q,s,p):
    return {'A':s<=p,'E':not(s&p),'I':bool(s&p),'O':bool(s-p)}[q]
def oracle(m,mode,q,s,p):
    ext=[tuple(extension(mask,m.n) for mask in w) for w in m.worlds]
    if mode=='T':return pair(q,ext[0][s],ext[0][p])
    if mode=='D':return all(pair(q,w[s],w[p]) for w in ext)
    chosen=ext[0][s]
    permanent=set.intersection(*(w[p] for w in ext))
    impossible=set(range(m.n))-set.union(*(w[p] for w in ext))
    good=permanent if q in 'AI' else impossible
    return chosen<=good if q in 'AE' else bool(chosen&good)

rows={}
for mode in ('N','D'):
    for name,triple in target.MOODS.items():
        for placement in ('major','minor'):rows[(mode,name,placement)]=[0,0,0]
worlds_seen=set()
for masks in itertools.product(range(4),repeat=6):
    m=target.Model(2,(tuple(masks[:3]),tuple(masks[3:])))
    worlds_seen.add(m.worlds)
    for mode,q,s,p in itertools.product(('T','N','D'),'AEIO',range(3),range(3)):
        require(target.evaluate(m,mode,q,s,p)==oracle(m,mode,q,s,p),'semantic mismatch')
    for (mode,name,place),counts in rows.items():
        a,b,c=target.MOODS[name]
        prem=oracle(m,mode if place=='major' else 'T',a,1,0) and oracle(m,mode if place=='minor' else 'T',b,2,1)
        require(target.premises(m,name,place,mode)==prem,'premise mismatch')
        if prem:
            counts[0]+=1;counts[1]+=not oracle(m,mode,c,2,0);counts[2]+=not oracle(m,'T',c,2,0)
            if mode=='N' and place=='major':
                route=target.witness_route(m,name)
                s=extension(m.worlds[0][2],2); mid=extension(m.worlds[0][1],2)
                expected=sorted(s) if b=='A' else sorted(s&mid)[:1]
                require(route==expected,'witness mismatch')
                for x in route:
                    require(x in s and x in mid,'not actual bridge')
                    require(all((x in extension(w[0],2))==(a=='A') for w in m.worlds),'predicate not permanent')
require(len(worlds_seen)==4096,'enumeration count')
require(set(m.worlds for m in target.models())==worlds_seen,'generator mismatch')
report=target.experiment()
for row in report['rows']:
    key=(row['semantics'],row['mood'],row['necessary_position'])
    require([row['premise_models'],row['necessary_failures'],row['actual_failures']]==rows[key],'summary counts')
    require(row['models']==4096,'summary model count')
    if row['first_countermodel']:
        x=row['first_countermodel'];m=target.Model(x['domain_size'],tuple(tuple(w) for w in x['worlds_P_M_S']))
        mode,name,place=key
        require(target.premises(m,name,place,mode) and not oracle(m,mode,target.MOODS[name][2],2,0),'reported countermodel')
for q,examples in report['semantic_differences'].items():
    require(set(examples)=={'N_not_D','D_not_N'},'incomparability coverage')
    for name,x in examples.items():
        m=target.Model(x['domain_size'],tuple(tuple(w) for w in x['worlds_P_M_S']))
        a,b=name.split('_not_')
        require(oracle(m,a,q,2,0) and not oracle(m,b,q,2,0),'incomparability witness')
# A smaller genuinely three-world, three-object collection adds boundary diversity.
for masks in itertools.product((0,1,3,7),repeat=3):
    m=target.Model(3,(tuple(masks),(7,3,1),(1,7,3)))
    for mode,q in itertools.product(('T','N','D'),'AEIO'):
        require(target.evaluate(m,mode,q,2,0)==oracle(m,mode,q,2,0),'three-world mismatch')
invalid=0
for args in [(0,((0,0,0),)),(-1,((0,0,0),)),(True,((0,0,0),)),(1,()),(1,[]),(1,((0,0),)),(1,([0,0,0],)),(1,((0,2,0),)),(1,((0,-1,0),)),(1,((0,True,0),)),(1,((0,0.0,0),))]:
    try:target.Model(*args)
    except ValueError:invalid+=1
    else:raise RuntimeError('invalid model accepted')
m=target.Model(1,((0,1,1),))
for args in [(m,'X','A',0,1),(m,'N','X',0,1),(m,'N','A',-1,1),(m,'N','A',0,3),(m,'N','A',True,1),(None,'N','A',0,1)]:
    try:target.evaluate(*args)
    except ValueError:invalid+=1
    else:raise RuntimeError('invalid evaluation accepted')
for name,place,mode in [('X','major','N'),('Barbara','X','N'),('Barbara','minor','X')]:
    try:target.premises(m,name,place,mode)
    except ValueError:invalid+=1
    else:raise RuntimeError('invalid premise argument accepted')
# Deliberately wrong evaluators; finding a distinguishing input is detection, not proof of test completeness.
mutants={
 'N_as_T':lambda m,q,s,p:oracle(m,'T',q,s,p),
 'N_as_D':lambda m,q,s,p:oracle(m,'D',q,s,p),
 'swap_terms':lambda m,q,s,p:oracle(m,'N',q,p,s),
 'negate_result':lambda m,q,s,p:not oracle(m,'N',q,s,p),
 'swap_A_I':lambda m,q,s,p:oracle(m,'N',{'A':'I','I':'A'}.get(q,q),s,p),
 'swap_E_O':lambda m,q,s,p:oracle(m,'N',{'E':'O','O':'E'}.get(q,q),s,p),
 'positive_for_negative':lambda m,q,s,p:oracle(m,'N',{'E':'A','O':'I'}.get(q,q),s,p),
 'last_world_only':lambda m,q,s,p:pair(q,extension(m.worlds[0][s],m.n),extension(m.worlds[-1][p],m.n)),
 'always_true':lambda m,q,s,p:True,
 'always_false':lambda m,q,s,p:False,
}
detected={}
for name,mut in mutants.items():
    for m in target.models():
        for q in 'AEIO':
            if mut(m,q,2,0)!=oracle(m,'N',q,2,0):
                detected[name]={'q':q,'model':target.encode(m)};break
        if name in detected:break
    require(name in detected,'undetected mutant')
output={'status':'PASS','checks':checks,'invalid_inputs_rejected':invalid,'detected_mutants':len(detected),'mutant_witnesses':detected,'rows':[{'semantics':k[0],'mood':k[1],'necessary_position':k[2],'premise_models':v[0],'necessary_failures':v[1],'actual_failures':v[2]} for k,v in rows.items()], 'bindings':{p:hashlib.sha256((BASE/p).read_bytes()).hexdigest() for p in ['modal.py','test_modal.py','results.json']}}
print(json.dumps(output,indent=2))
