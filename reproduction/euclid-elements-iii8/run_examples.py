"""Exact examples and finite branch-order checks, not general proofs."""
import json
from fractions import Fraction as F
from geometry import *

def report():
    orders={};pairs=0
    for r,d in ((F(5),F(13)),(F(5),F(6)),(F(3),F(5))):
        for branch in ('near','far'):
            rows=[]
            for i in range(81):
                p=sample(r,F(i,20));c=certificate(r,d,p)
                if c['branch']==branch:
                    rows.append((p[1]**2/c['squared_distance'],c['squared_distance']))
            rows=sorted(set(rows))
            for (v,a),(w,b) in zip(rows,rows[1:]):
                if not (v<w and (a<b if branch=='near' else a>b)):raise ValueError('branch order failure')
                pairs+=1
            orders[f'r={r},d={d},{branch}']=len(rows)
    s=secant(5,13,(3,4));a,b=s['points']
    return {'finite_configurations':sum(verify(certificate(*g)) for g in grid()),
            'branch_samples':orders,'adjacent_branch_comparisons':pairs,
            'near_example':certificate(5,13,(3,4)),
            'far_positive_x_counterexample':certificate(5,6,(3,4)),
            'same_ray_secant':s,'same_ray_slope':a[1]/(13-a[0]),
            'equal_shell_116':equal_shell(5,13,116),
            'tangent':certificate(3,5,(F(9,5),F(12,5))),
            'scope':'finite exact rational checks; not a general theorem proof'}
if __name__=='__main__': print(json.dumps(report(),default=str,ensure_ascii=False,indent=2))
