import json
from geometry import *
from cases import *
n=0;branches={}
for d in positives():
 c=make_certificate(d)
 if not verify_certificate(d,c):raise RuntimeError('certificate failure')
 a=c['area'];hs=c['halves']
 if a['ABC']!=a['DBC'] or F(a['EBCA'])!=2*F(a['ABC']) or F(a['DBCF'])!=2*F(a['DBC']) or len(set(hs.values()))!=1:raise RuntimeError('area failure')
 n+=1;branches[c['top_case']]=branches.get(c['top_case'],0)+1
m=0
for d in negatives():
 try:make_certificate(d)
 except ValueError:m+=1
 else:raise RuntimeError('illegal geometry accepted')
r={'positive_inputs':n,'negative_inputs_directly_rejected':m,'branches':branches,'example':make_certificate(EXAMPLE),'scope':'finite rational coordinate teaching checks; not general proof'}
open('results.json','w').write(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
