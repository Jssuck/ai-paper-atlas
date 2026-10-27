import json
from pathlib import Path
from cases import positives,negative_cases,sample
from geometry import make_certificate,verify_certificate
accepted=0
for data in positives():
    if not verify_certificate(data,make_certificate(data)): raise RuntimeError('positive failed')
    accepted+=1
rejected=[]
for name,data in negative_cases().items():
    try: make_certificate(data)
    except ValueError: rejected.append(name)
    else: raise RuntimeError('negative accepted: '+name)
result={'positive_count':accepted,'negative_count':len(rejected),'negative_names':rejected,
        'hand_examples':{m:make_certificate(sample(m)) for m in ('corresponding','interior_sum')},
        'limitation':'Finite rational Euclidean-coordinate checks do not prove the general proposition.'}
Path('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
