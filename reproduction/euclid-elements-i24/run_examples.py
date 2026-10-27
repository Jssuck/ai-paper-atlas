import json
from fractions import Fraction as Q
from geometry import certify,verify
from cases import positives,negatives,case
certificates=[certify(d) for d in positives()]
for d,c in zip(positives(),certificates):
    if not verify(d,c):raise RuntimeError('positive failed')
for d in negatives():
    try:certify(d)
    except ValueError:pass
    else:raise RuntimeError('invalid input accepted')
print(json.dumps({'positive_certificates':len(certificates),'negative_inputs':len(negatives()),
 'orientation_counts':{str(k):sum(c['EFG_orientation']==k for c in certificates) for k in (-1,0,1)},
 'configuration_examples':[certify(case(a=a)) for a in (1,2,3)],
 'article_examples':[certify(case(a=a,b=2,s=Q(1,2),t=1)) for a in (2,6,8)],
 'scope':'finite exact tests of modern coordinate reconstruction; not proof of general theorem'},indent=2))
