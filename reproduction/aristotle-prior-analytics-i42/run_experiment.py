"""Exhaustive checks in the explicitly bounded canonical support models."""
import json
from itertools import product
from model import *


def require(value, message):
    if not value:
        raise RuntimeError(message)


def run():
    rows=[]
    total=0
    for policy in (False,True):
        models=list(canonical_models(policy))
        valid={1:[],2:[],3:[]}
        failures={1:{},2:{},3:{}}
        for f in (1,2,3):
            for chars in product(KINDS,repeat=3):
                mood=''.join(chars)
                bad=0
                for model in models:
                    a,b,c=evaluate(model,f,mood)
                    bad+=bool(a and b and not c)
                    total+=1
                if bad:failures[f][mood]=bad
                else:valid[f].append(mood)
        require([len(v) for v in valid.values()]==([6,6,6] if policy else [4,4,4]),'unexpected valid moods')
        expected={'A':[1], 'E':[1,2], 'I':[1,3], 'O':[1,2,3]}
        candidates={k:[f for f in (1,2,3) if any(m[-1]==k for m in valid[f])] for k in KINDS}
        require(candidates==expected,'unexpected candidate figures')
        rows.append(dict(nonempty_terms=policy,canonical_models=len(models),moods_checked=192,
                         model_mood_evaluations=len(models)*192,valid_moods=valid,
                         candidates=candidates,invalid_mood_counts={f:len(v) for f,v in failures.items()}))
    universe={0,1,2}
    subsets=[{i for i in universe if mask&(1<<i)} for mask in range(8)]
    mixed_cases=0; premises_true=0
    for s,m,p,q in product(subsets,repeat=4):
        mixed_cases+=1
        if s<=m and m<=p and not(p&q):
            premises_true+=1
            require(s<=p and not(s&q),'mixed proof conclusion failure')
    require([s['figure'] for s in mixed_proof()]==[1,2],'mixed figure label failure')
    result=dict(policies=rows,total_model_mood_evaluations=total,
                mixed_proof=mixed_proof(),mixed_model_assignments=mixed_cases,
                mixed_premises_satisfied=premises_true,mixed_failures=0)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':run()
