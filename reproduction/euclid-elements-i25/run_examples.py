import json
from geometry import certify, classify, verify, triangle
from cases import case, positives
cs=positives()
result={'model':'exact rational Gram data; finite tests, not general theorem proof',
        'positive_cases':len(cs),'verified':sum(verify(d,certify(d)) for d in cs),
        'example':certify(case()),
        'equal_base':classify(case(d=3,e=3)),
        'reversed_base':classify(case(d=3,e=0)),
        'missing_second_equality':{
            'ABC':{'a2':[1,1],'b2':[100,1],'dot':[5,1]},
            'DEF':{'a2':[1,1],'b2':[1,1],'dot':[0,1]},
            'BC2':91,'EF2':2,'angle_BAC_degrees':60,'angle_EDF_degrees':90,
            'meaning':'larger base but smaller angle; I.25 hypotheses not satisfied'}}
if result['verified'] != len(cs):raise RuntimeError('grid failure')
print(json.dumps(result,ensure_ascii=False,indent=2))
