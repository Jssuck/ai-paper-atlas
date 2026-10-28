import json
from collections import Counter
from geometry import make_certificate,verify_certificate
from cases import *
n=0;counts=Counter()
for d in positives():
 c=make_certificate(d)
 if not verify_certificate(d,c):raise RuntimeError('certificate failed')
 if c['area']['ABCD']!=c['area']['EBCF']:raise RuntimeError('area failed')
 if c['cut']['case']!='identical' and (c['cut']['first_reassembled']!=c['area']['ABCD'] or c['cut']['second_reassembled']!=c['area']['EBCF']):raise RuntimeError('cut failed')
 counts[c['cut']['case']]+=1;n+=1
m=0
for d in negatives():
 try:make_certificate(d)
 except ValueError:m+=1
 else:raise RuntimeError('negative accepted')
r={'positive_inputs':n,'negative_inputs':m,'branches':dict(counts),'example':make_certificate(EXAMPLE),'scope':'finite rational coordinate model, not a general proof'}
open('results.json','w').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
