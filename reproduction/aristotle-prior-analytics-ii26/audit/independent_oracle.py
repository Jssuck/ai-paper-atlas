"""Independent reviewer oracle: per-object boolean valuations, not bit algebra.

The production module is loaded only for differential comparison; no predicate,
route formula, or enumeration helper is reused in computing expected answers.
"""
from itertools import product
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import objections

ROUTES=('upper_negative','lower_negative','upper_positive','lower_positive','second_negative','first_particular')

def oracle(rows, route):
    a_all_b=all(not b or a for a,b,c in rows)
    no_b_a=all(not(b and a) for a,b,c in rows)
    some_b_a=any(b and a for a,b,c in rows)
    some_b_not_a=any(b and not a for a,b,c in rows)
    exists_b=any(b for a,b,c in rows)
    if route=='upper_negative':
        premises=[all(not b or c for a,b,c in rows),all(not(c and a) for a,b,c in rows)]
        conclusion,target,ct,tt='E','A',no_b_a,a_all_b
    elif route=='lower_negative':
        premises=[all(not c or b for a,b,c in rows),all(not(c and a) for a,b,c in rows),any(c for a,b,c in rows)]
        conclusion,target,ct,tt='O','A',some_b_not_a,a_all_b
    elif route=='upper_positive':
        premises=[all(not b or c for a,b,c in rows),all(not c or a for a,b,c in rows)]
        conclusion,target,ct,tt='A','E',a_all_b,no_b_a
    elif route=='lower_positive':
        premises=[all(not c or b for a,b,c in rows),all(not c or a for a,b,c in rows),any(c for a,b,c in rows)]
        conclusion,target,ct,tt='I','E',some_b_a,no_b_a
    elif route=='second_negative':
        premises=[all(not a or c for a,b,c in rows),all(not(b and c) for a,b,c in rows)]
        conclusion,target,ct,tt='E','A',no_b_a,a_all_b
    elif route=='first_particular':
        premises=[any(b and c for a,b,c in rows),all(not c or a for a,b,c in rows)]
        conclusion,target,ct,tt='I','E',some_b_a,no_b_a
    else:raise ValueError('unknown oracle route')
    accepted=all(premises)
    return dict(route=route,premises=premises,accepted=accepted,conclusion=conclusion,conclusion_true=ct,target=target,target_true=tt,rejects_target=accepted and not tt,subject_nonempty=exists_b)

def run():
    counts={r:dict(premises_hold=0,conclusion_failures=0,genuine_rejections=0,empty_subject_nonrejections=0) for r in ROUTES}
    worlds=comparisons=0
    valuations=list(product((False,True),repeat=3))
    for n in range(5):
        for rows in product(valuations,repeat=n):
            worlds+=1
            masks=[sum(2**i for i,row in enumerate(rows) if row[k]) for k in range(3)]
            a_all_b=all(not b or a for a,b,c in rows)
            some_b_not_a=any(b and not a for a,b,c in rows)
            no_b_a=all(not(b and a) for a,b,c in rows)
            some_b_a=any(b and a for a,b,c in rows)
            if a_all_b==some_b_not_a or no_b_a==some_b_a:raise RuntimeError('square failure')
            for route in ROUTES:
                expected=oracle(rows,route)
                actual=objections.certificate(n,*masks,route)
                comparisons+=1
                if actual!=expected:raise RuntimeError((rows,route,expected,actual))
                if expected['accepted']:
                    q=counts[route];q['premises_hold']+=1
                    if not expected['conclusion_true']:q['conclusion_failures']+=1
                    if expected['rejects_target']:q['genuine_rejections']+=1
                    elif not expected['subject_nonempty']:q['empty_subject_nonrejections']+=1
                    else:raise RuntimeError('nonempty route failed to reject')
    aggregate=objections.enumerate_models(4)
    if aggregate['routes']!=counts or aggregate['worlds']!=worlds:raise RuntimeError('aggregate mismatch')
    if any(v['conclusion_failures'] for v in counts.values()):raise RuntimeError('invalid route')
    return dict(method='independent objectwise boolean valuations; every certificate field compared',worlds=worlds,certificate_comparisons=comparisons,mismatches=0,routes=counts)
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
