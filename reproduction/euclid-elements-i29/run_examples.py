import json
from pathlib import Path
from geometry import make_certificate,verify_certificate
from cases import EXAMPLE,positives,negatives
n=0
for x in positives():
    if not verify_certificate(x,make_certificate(x)):raise RuntimeError('positive rejected')
    n+=1
m=0
for x in negatives():
    try:make_certificate(x)
    except ValueError:m+=1
    else:raise RuntimeError('negative accepted')
r={'positive_inputs':n,'negative_inputs_directly_rejected':m,'example':make_certificate(EXAMPLE),'scope':'finite rational Euclidean examples, not a proof or independence test'}
Path('results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
