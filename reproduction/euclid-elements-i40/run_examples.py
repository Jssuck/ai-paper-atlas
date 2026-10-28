import json
from geometry import make_certificate,verify_certificate,construction_trace
from cases import positives,negatives,build,EXAMPLE
count=0;coincident=0
for p in positives():
    c=make_certificate(p)
    if not verify_certificate(p,c):raise RuntimeError('verification failed')
    count+=1;coincident+=c['trace']['apex_relation']=='coincident'
rejected=[]
for label,p in negatives():
    try:make_certificate(p)
    except ValueError as e:rejected.append({'case':label,'reason':str(e)})
    else:raise RuntimeError('invalid geometry accepted')
result={'legal_cases':count,'coincident_apex_cases':coincident,'illegal_cases_rejected':len(rejected),'rejections':rejected,
'example':make_certificate(EXAMPLE),'construction_only_branches':[construction_trace(build(k=k)) for k in [4,1]],
'limitation':'Finite rational-coordinate examples do not prove the general proposition or reproduce its synthetic proof.'}
open('results.json','w').write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'legal_cases':count,'coincident_apex_cases':coincident,'illegal_cases_rejected':len(rejected)},ensure_ascii=False))
