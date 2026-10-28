import json
from geometry import construct,verify,area
from cases import VALID,INVALID
rows=[]
for args in VALID:
 c=construct(*args)
 rows.append({'parameters':list(map(str,args)),'points':{k:list(map(str,v)) for k,v in c['points'].items()},'verified':verify(c)})
invalid=[]
for args in INVALID:
 try:construct(*args)
 except (TypeError,ValueError) as e:invalid.append({'parameters':list(map(str,args)),'rejected':type(e).__name__})
 else:raise RuntimeError('invalid accepted')
r={'valid_count':len(rows),'invalid_count':len(invalid),'valid':rows,'invalid':invalid,'scope':'exact rational canonical I.44 teaching model, finite checks are not a proof'}
open('results.json','w').write(json.dumps(r,indent=2)+'\n');print(json.dumps({'valid':len(rows),'invalid':len(invalid),'all_verified':all(x['verified'] for x in rows)}))
