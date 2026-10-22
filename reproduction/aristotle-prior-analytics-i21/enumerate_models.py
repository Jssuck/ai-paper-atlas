"""Bounded checks of teaching semantics; no finite run proves general validity."""
import json
from model import models, examples

def need(value,message):
    if not value: raise RuntimeError(message)

def main():
    counts={k:0 for k in ['c_witness_transfer','p_negative_transfer','n_positive_transfer','c_implies_p_negative','weak_necessary_duality']}
    failures={k:0 for k in ['affirmative_actual_subject','negative_background','different_particular_witnesses']}
    first={}
    total=0
    for n,w in [(1,1),(1,2),(1,3),(2,1),(2,2)]:
        for m in models(n,w):
            total+=1
            h=m.holds
            rules={
              'c_witness_transfer':(h('D','a','B','C') and h('C','i','A','C'),h('C','i','A','B')),
              'p_negative_transfer':(h('D','a','B','C') and h('P','o','A','C'),h('P','o','A','B')),
              'n_positive_transfer':(h('N','a','A','B') and h('D','a','B','C'),h('N','a','A','C')),
              'c_implies_p_negative':(h('C','o','A','C'),h('P','o','A','C')),
              'weak_necessary_duality':(True,h('P','o','A','B') == (not h('N','a','A','B'))),
            }
            for k,(premise,result) in rules.items():
                if premise:
                    counts[k]+=1
                    need(result,k+' failed')
            invalid={
              'affirmative_actual_subject':(h('D','a','A','C') and h('C','a','B','C'),h('P','i','A','B')),
              'negative_background':(h('D','e','A','C') and h('C','a','B','C'),h('P','o','A','B')),
              'different_particular_witnesses':(h('D','i','A','C') and h('C','i','B','C'),h('C','i','A','B')),
            }
            if all(m.extension(t) for t in 'ABC'):
                for k,(premise,result) in invalid.items():
                    if premise and not result:
                        failures[k]+=1
                        first.setdefault(k,m.as_dict())
    need(all(failures.values()),'counterexample family missing')
    report={'scope':'Finite teaching configurations, not general proof or unique ancient semantics','configurations':total,'dimensions':[[1,1],[1,2],[1,3],[2,1],[2,2]],'rule_premise_counts':counts,'nonempty_counterexample_counts':failures,'first_nonempty_counterexamples':first,'examples':{k:m.as_dict() for k,m in examples().items()}}
    print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True))
if __name__=='__main__': main()
