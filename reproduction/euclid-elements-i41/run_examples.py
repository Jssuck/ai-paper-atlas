import json
from collections import Counter
from geometry import *
from cases import *
certs=[make_certificate(p) for p in valid_cases()]
rejected=[]
for label,p in invalid_cases():
    try: make_certificate(p)
    except ValueError as e: rejected.append({'label':label,'reason':str(e)})
    else: raise RuntimeError('invalid input accepted')
result={'scope':'finite rational teaching examples, not a general proof','valid_count':len(certs),'positions':dict(Counter(c['upper_position'] for c in certs)),'invalid_count':len(rejected),'rejected':rejected,'hand_examples':{str(t):make_certificate(example(t)) for t in [-2,0,F(1,2),1,3]}}
open('results.json','w').write(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:result[k] for k in ['scope','valid_count','positions','invalid_count']},ensure_ascii=False,indent=2))
