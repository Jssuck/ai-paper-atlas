import json
from geometry import make_certificate,verify_certificate
from cases import positives,negatives,EXAMPLE
n=0
for d in positives():
 c=make_certificate(d)
 if not verify_certificate(d,c):raise RuntimeError('positive failed')
 if c['triangles']['ABC_squared']!=c['triangles']['DCB_squared']:raise RuntimeError('congruence failed')
 if c['triangles']['ABC_twice_area']!=c['triangles']['DCB_twice_area']:raise RuntimeError('area failed')
 n+=1
m=0
for d in negatives():
 try:make_certificate(d)
 except ValueError:m+=1
 else:raise RuntimeError('invalid geometry accepted')
r={'positive_cases':n,'negative_cases':m,'example':make_certificate(EXAMPLE),'scope':'finite exact rational Euclidean model, not a general theorem proof'}
open('results.json','w').write(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'positive_cases':n,'negative_cases':m}))
