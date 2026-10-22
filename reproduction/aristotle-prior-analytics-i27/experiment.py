"""Finite soundness/certificate checks, not a proof of general soundness."""
import json
from itertools import product
from model import KnowledgeBase, model_holds

def run():
    names=('a','b','c')
    total_models=0; bases=0; positive=negative=verified=0
    # Every nonempty subset of 8 membership types is one representative universe.
    # Empty term extensions are permitted. Repeated identical types are omitted.
    for mask in range(1,256):
        universe={t for t in range(8) if mask & (1<<t)}
        ext={name:{t for t in universe if t & (1<<i)} for i,name in enumerate(names)}
        pos=[(a,b) for a,b in product(names,repeat=2) if ext[a]<=ext[b]]
        neg=[(a,b) for a,b in product(names,repeat=2) if ext[a].isdisjoint(ext[b])]
        total_models+=1
        # Four explicitly specified premise selections, not every possible sub-base.
        for policy in range(4):
            pp=[e for i,e in enumerate(pos) if policy==0 or i%3==policy-1]
            nn=[e for i,e in enumerate(neg) if policy==0 or i%3==policy-1]
            kb=KnowledgeBase(names,pp,nn);bases+=1
            if not model_holds(kb,ext):raise RuntimeError('input truth mismatch')
            for a,b in product(names,repeat=2):
                p=kb.inclusion(a,b)
                if p is not None:
                    positive+=1
                    if not ext[a]<=ext[b]:raise RuntimeError('unsound positive')
                    if not kb.verify(a,b,p):raise RuntimeError('bad positive certificate')
                    verified+=1
                q=kb.exclusion(a,b)
                if q is not None:
                    negative+=1
                    if not ext[a].isdisjoint(ext[b]):raise RuntimeError('unsound negative')
                    if not kb.verify(a,b,q):raise RuntimeError('bad negative certificate')
                    verified+=1
    demo=KnowledgeBase(('human','animal','stone','student'),(('human','animal'),('student','human')),(('animal','stone'),))
    return {'representative_models':total_models,'premise_selections':bases,
            'positive_certificates':positive,'negative_certificates':negative,'verified_certificates':verified,
            'demo_human':demo.catalog('human'),
            'demo_student_animal_path':demo.inclusion('student','animal').path,
            'demo_student_stone':vars(demo.exclusion('student','stone')),
            'missing_relation_is_unknown':demo.inclusion('animal','human') is None,
            'limits':'255 finite type models; four selections each; no general proof, no completeness claim, no existential/probabilistic inference'}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
