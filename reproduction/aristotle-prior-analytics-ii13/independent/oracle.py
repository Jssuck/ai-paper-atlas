#!/usr/bin/env python3
"""Independent explicit-set oracle for Prior Analytics II.13.

Uses occupied Boolean types as distinct objects; never imports the production
truth evaluator. Production results are read as data only when available.
"""
from itertools import combinations, product
from pathlib import Path
import json

FORMS = ('U', 'E', 'I', 'O')
NEG = {'U':'O', 'O':'U', 'E':'I', 'I':'E'}

def model(types):
    return {name: frozenset(i for i, t in enumerate(types) if t & bit)
            for name, bit in (('A',1),('B',2),('C',4))}

def truth(m, f, p, s):
    pred, subj = m[p], m[s]
    if f == 'U': return subj <= pred
    if f == 'E': return not (subj & pred)
    if f == 'I': return bool(subj & pred)
    if f == 'O': return bool(subj - pred)
    raise ValueError(f)

def check(ok, label):
    if not ok: raise RuntimeError(label)

def universe(nonempty):
    return [t for n in range(1,9) for t in combinations(range(8),n)
            if not nonempty or all(model(t).values())]

def run():
    output = {'oracle': 'explicit sets; independent of production evaluator', 'policies': {}}
    for policy, ne in [('allow_empty',False),('all_terms_nonempty',True)]:
        ts = universe(ne)
        rows=[]
        for h,r,k in product(FORMS, repeat=3):
            intern=[]; outer=[]; premise_count=0; background_count=0
            for t in ts:
                m=model(t)
                H=truth(m,h,'A','B'); R=truth(m,r,'C','B'); K=truth(m,k,'A','C')
                if H and R:
                    premise_count+=1
                    if not K: intern.append(t)
                if R and not K:
                    background_count+=1
                    if H: outer.append(t)
            check(intern==outer,'contraposition countermodels differ')
            rows.append({'h':h,'r':r,'k':k,'valid':not intern,
                         'premise_models':premise_count,'background_models':background_count,
                         'countermodels':len(intern), 'countermodel':list(intern[0]) if intern else None})
        valid=[r for r in rows if r['valid']]
        check(len(ts)==(218 if ne else 255),'model count')
        check(all(r['k'] in 'IO' for r in valid),'internal universal unexpectedly valid')
        for h,r,k in [('O','U','O'),('E','I','O'),('I','U','I'),('U','I','I')]:
            check(any(v['h']==h and v['r']==r and v['k']==k for v in valid),'original route')
        wrong = next(r for r in rows if (r['h'],r['r'],r['k'])==('E','U','O'))
        check(wrong['valid']==ne,'empty-B boundary for wrong contrary')
        output['policies'][policy]={'models':len(ts),'rows':rows,'valid_routes':len(valid),
            'by_discharged_goal':{g:sum(v['h']==NEG[g] for v in valid) for g in FORMS}}
    # Structural independence checks: mixed B supports I and O simultaneously.
    m=model((2,3))
    check(truth(m,'I','A','B') and truth(m,'O','A','B'),'I/O coexistence')
    check(not truth(m,'U','A','B') and not truth(m,'E','A','B'),'false universal contraries')
    # U(C,B), U(A,C) prove U(A,B), even for empty B; no fake background countermodel.
    for t in universe(False):
        m=model(t)
        check(not(truth(m,'U','C','B') and truth(m,'U','A','C')) or truth(m,'U','A','B'),'full positive background')
        check(not(truth(m,'U','C','B') and truth(m,'E','A','C')) or truth(m,'E','A','B'),'full negative background')
    output['checks']='four original routes, every countermodel, exact contradictory discharge, internal universal absence, empty-B boundary, mixed I/O and full-background distinction'
    production_path = Path(__file__).parent.parent / 'evidence/results-normal.json'
    if production_path.exists():
        production = json.loads(production_path.read_text())
        aliases={'empty_allowed':'allow_empty','all_nonempty':'all_terms_nonempty'}
        compared=0
        for sec in production['policies']:
            expected=output['policies'][aliases[sec['policy']]]
            check(sec['models']==expected['models'],'production model count')
            check(sec['certificate_counts']==expected['by_discharged_goal'],'production certificate counts')
            for row in sec['rows']:
                h,r,k=row['hypothesis'][0],row['other'][0],row['result'][0]
                e=next(x for x in expected['rows'] if (x['h'],x['r'],x['k'])==(h,r,k))
                check(row['target']==[NEG[h],'A','B'] and row['known']==[NEG[k],'A','C'],'production discharge fields')
                for key,count in [('internal','premise_models'),('external','background_models')]:
                    actual=row[key]
                    check(actual=={'valid':e['valid'],'premise_models':e[count],
                        'countermodels':e['countermodels'],'minimal_countermodel':e['countermodel']}, 'production record '+key+str((h,r,k)))
                    compared+=1
                check(row['certificate']==(e['valid'] and e['premise_models']>0 and e['background_models']>0),'certificate')
        named=[]
        for case in production['named_checks']:
            ts=universe(case['policy']=='all_nonempty')
            if case['policy']=='B_nonempty': ts=[t for t in ts if model(t)['B']]
            positive=[t for t in ts if all(truth(model(t),*p) for p in case['premises'])]
            counter=[t for t in positive if not truth(model(t),*case['conclusion'])]
            e={'valid':not counter,'premise_models':len(positive),'countermodels':len(counter),
                'minimal_countermodel':list(counter[0]) if counter else None}
            check(all(case[k]==v for k,v in e.items()),'named case '+case['name'])
            named.append(case['name'])
        output['production_comparison']={'records':compared,'named_checks':len(named),'status':'PASS'}
        print('PASS: production JSON exact fields, '+str(compared)+' records and '+str(len(named))+' named checks.')
    else:
        output['production_comparison']={'status':'NOT YET AVAILABLE'}
    path=Path(__file__).with_name('oracle-results.json')
    path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({p:{k:v for k,v in d.items() if k!='rows'} for p,d in output['policies'].items()},ensure_ascii=False,sort_keys=True))
    print('PASS: 128 independently evaluated route records; 256 internal/outer validity comparisons.')
    return output

if __name__=='__main__': run()
