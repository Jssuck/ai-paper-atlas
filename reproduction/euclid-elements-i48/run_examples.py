import json
from geometry import construct,verify,report
from cases import valid_cases,invalid_cases
rows=[]
for a in valid_cases():
    p=construct(*a)
    if not verify(*a,p):raise RuntimeError('valid case rejected')
    rows.append(report(p))
n=0
for a in invalid_cases():
    try: construct(*a)
    except ValueError:n+=1
    else:raise RuntimeError('invalid case admitted')
r={'valid_cases':len(rows),'invalid_directly_rejected':n,'example_3_4':report(construct((0,0),(3,0),(0,4))),'finite_tests_are_not_general_proof':True}
open('results.json','w').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
