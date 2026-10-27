import json
from geometry import construct,accepted,point
from cases import positives,negatives

n=0;irr=0
for args in positives():
    k=construct(*args)
    if not accepted(*args,k):raise RuntimeError('certificate failure')
    n+=1;irr+=k['t']['b']!='0'
negative=0
for args in negatives():
    try:construct(*args)
    except (TypeError,ValueError):negative+=1
    else:raise RuntimeError('invalid input accepted')
print(json.dumps({'positive_certificates':n,'irrational_cuts':irr,'negative_inputs':negative,
                  'example':construct(point(0,0),point(1,1),point(4,0)),
                  'scope':'finite rational-input tests, not a general proof'},ensure_ascii=False,indent=2))
