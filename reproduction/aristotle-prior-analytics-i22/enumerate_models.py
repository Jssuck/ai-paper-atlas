"""Finite regression checks, not proofs of general modal laws."""
import json
from model import models, examples

def checks(m):
    h=m.holds
    intersection=bool(m.extension('B')&m.extension('C'))
    return {
        'universal_safe_bridge':(bool(m.extension('C')) and h('C','a','A','C') and h('N','a','B','C'),h('C','i','A','B')),
        'necessary_particular_bridge':(h('C','a','A','C') and h('N','i','B','C'),h('C','i','A','B')),
        'contingent_particular_bridge':(h('C','i','A','C') and h('N','a','B','C'),h('C','i','A','B')),
        'positive_intersection_bridge':(intersection and h('N','a','A','C'),h('N','i','A','B')),
        'negative_intersection_bridge':(intersection and h('N','e','A','C'),h('N','o','A','B')),
        'contingent_negative_rewrite':(True,h('C','a','A','C')==h('C','e','A','C')),
        'box_negative_conversion':(True,h('BOX','e','A','C')==h('BOX','e','C','A')),
    }

def main():
    counts={};dimensions=[];total=0
    for n,w in [(1,1),(1,2),(1,3),(2,1),(2,2)]:
        count=0
        for m in models(n,w):
            count+=1;total+=1
            for name,(premise,conclusion) in checks(m).items():
                counts[name]=counts.get(name,0)+int(premise)
                if premise and not conclusion:raise RuntimeError((name,m.as_dict()))
        dimensions.append({'objects':n,'worlds':w,'configurations':count})
    print(json.dumps({'configurations':total,'dimensions':dimensions,'rule_premise_counts':counts,'all_checks_passed':True,'examples':{k:v.as_dict() for k,v in examples().items()}},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
