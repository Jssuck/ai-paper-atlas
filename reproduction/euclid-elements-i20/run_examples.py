import json
from geometry import construct,accepted,point,sum_greater
from cases import positive_cases,invalid_cases
cases=positive_cases()
certificates=[construct(*case) for case in cases]
if not all(accepted(*case,cert) for case,cert in zip(cases,certificates)):raise RuntimeError('replay failed')
rejected=0
for case in invalid_cases():
    try:construct(*case)
    except ValueError:rejected+=1
if rejected!=len(invalid_cases()):raise RuntimeError('negative gate failed')
print(json.dumps({'positive_certificates':len(cases),'negative_inputs':rejected,
 'nonrational_extension_parameters':sum(c['t']['b']!='0' for c in certificates),
 'sample':construct(point(0,0),point(3,0),point(0,4)),
 'degenerate_equality_1_plus_2_gt_3':sum_greater(1,4,9)},indent=2))
