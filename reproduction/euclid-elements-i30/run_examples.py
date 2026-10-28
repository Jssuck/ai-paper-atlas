import json
from pathlib import Path
from geometry import make_certificate,verify_certificate
from cases import example,positives,negatives
n=0
for d in positives():
 if not verify_certificate(d,make_certificate(d)): raise RuntimeError('positive failed')
 n+=1
m=0
for d in negatives():
 try: make_certificate(d)
 except ValueError: m+=1
 else: raise RuntimeError('invalid geometry accepted')
r={'positive_inputs':n,'negative_inputs_directly_rejected':m,'sample':make_certificate(example()),'scope':'finite rational Euclidean coordinate cases, not an axiomatic proof'}
Path('results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False))
