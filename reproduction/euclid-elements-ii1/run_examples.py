import json
from geometry import construct,verify,summary
from cases import valid_cases,invalid_cases
from fractions import Fraction as Q
valid=invalid=0
for a in valid_cases():
    if not verify(*a,construct(*a)):raise RuntimeError('valid case failed')
    valid+=1
for a in invalid_cases():
    try:construct(*a)
    except ValueError:invalid+=1
    else:raise RuntimeError('invalid case accepted')
r={'valid_cases':valid,'invalid_cases_rejected':invalid,'original_three_parts':summary((0,0),(6,0),(0,2),[Q(1,6),Q(1,2)]),'slanted_example':summary((1,-2),(4,2),(-3,1),[Q(1,5),Q(3,5)]),'scope':'finite rational geometry; no proof of universal theorem'}
open('results.json','w').write(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False))
