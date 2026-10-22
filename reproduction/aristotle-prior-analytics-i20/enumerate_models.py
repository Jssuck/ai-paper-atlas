"""Exhaustive finite checks; failures are intended witnesses, not hidden errors."""
import json
from model import models, examples

RANGES=((1,1),(1,2),(1,3),(2,1),(2,2))
def run():
    counts={k:0 for k in ('configurations','query_evaluations','polarity_checks','universal_bridge_premises','particular_bridge_premises','exact_witness_bridge_premises','conversion_candidates','conversion_failures','third_figure_candidates','third_figure_failures','first_figure_candidates','first_figure_failures','two_particular_candidates','two_particular_failures')}
    first_failures={}
    for n,w in RANGES:
        for m in models(n,w):
            counts['configurations']+=1
            for x in 'ABC':
                for y in 'ABC':
                    for q in ('a','i'):
                        qneg={'a':'e','i':'o'}[q]
                        if m.holds('C',q,x,y)!=m.holds('C',qneg,x,y):
                            raise RuntimeError('C polarity equivalence failed')
                        counts['polarity_checks']+=1
                    for mode in ('D','P','N','C','BOX'):
                        for q in 'aeio':
                            value=m.holds(mode,q,x,y)
                            if type(value) is not bool: raise RuntimeError('query not boolean')
                            counts['query_evaluations']+=1
            ca=m.holds('C','a','A','C'); cb=m.holds('C','a','B','C')
            ia=m.holds('C','i','A','C'); ib=m.holds('C','i','B','C')
            result=m.holds('C','i','A','B')
            c0=m.extension('C'); b0=m.extension('B')
            premises={
                'universal_bridge':ca and bool(c0&b0),
                'particular_bridge':ia and c0&~b0==0,
                'exact_witness_bridge':bool(c0&b0&m.varying('A')),
            }
            for label,premise in premises.items():
                if premise:
                    counts[label+'_premises']+=1
                    if not result: raise RuntimeError(label+' failed')
            candidates={
                'conversion':bool(c0) and cb,
                'third_figure':bool(c0) and ca and cb,
                'first_figure':ca and m.holds('C','i','C','B'),
                'two_particular':ia and ib,
            }
            for label,premise in candidates.items():
                if premise:
                    counts[label+'_candidates']+=1
                    target=m.holds('C','i','C','B') if label=='conversion' else result
                    if not target:
                        counts[label+'_failures']+=1
                        first_failures.setdefault(label,m.as_dict())
    ex={}
    for label,m in examples().items():
        ex[label]={**m.as_dict(), 'queries':{f'{mode}_{q}(A,B)':m.holds(mode,q,'A','B') for mode in ('D','P','N','C','BOX') for q in 'aeio'},'C_a(A,C)':m.holds('C','a','A','C'),'C_a(B,C)':m.holds('C','a','B','C'),'C_i(A,C)':m.holds('C','i','A','C'),'C_i(B,C)':m.holds('C','i','B','C'),'C_i(C,B)':m.holds('C','i','C','B')}
    return {'scope':'Finite author checks, not a general proof or ancient-semantics certification','ranges':[{'objects':n,'worlds':w} for n,w in RANGES], 'counts':counts,'first_failures':first_failures,'examples':ex}
if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
