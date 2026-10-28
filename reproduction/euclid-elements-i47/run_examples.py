import json
from geometry import *
from cases import *
valid=list(valid_cases());invalid=invalid_cases()
for args in valid:
    if not verify(*args,construct(*args)):raise RuntimeError('valid case rejected')
for args in invalid:
    try:construct(*args)
    except ValueError:pass
    else:raise RuntimeError('invalid case accepted')
c=construct((0,0),(3,0),(0,4))
r={'valid_cases':len(valid),'invalid_direct_rejections':len(invalid),'example_points':{k:[str(x) for x in v] for k,v in c.items()},'example_areas':report(c),'scope':'finite rational-coordinate checks, not a general proof'}
open('results.json','w').write(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False))
