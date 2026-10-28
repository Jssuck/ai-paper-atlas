import json
from geometry import construct,verify
from cases import valid_cases,INVALID
rows=[]
for a in valid_cases():
 c=construct(*a)
 if not verify(*a,c):raise RuntimeError('valid rejected')
 rows.append({'vertices':[[str(x)for x in v]for v in a[0]],'h_p_q':list(map(str,a[1:])),'points':{k:list(map(str,v))for k,v in c['points'].items()},'areas':list(map(str,c['areas'])),'verified':True})
invalid=[]
for name,*a in INVALID:
 try:construct(*a)
 except ValueError as e:invalid.append({'name':name,'rejected':True,'reason':str(e)})
 else:raise RuntimeError(name+' was accepted')
r={'valid_count':len(rows),'invalid_count':len(invalid),'valid_cases':rows,'invalid_cases':invalid}
open('results.json','w').write(json.dumps(r,indent=2)+'\n')
print(json.dumps({'valid':len(rows),'invalid_rejected':len(invalid)}))
