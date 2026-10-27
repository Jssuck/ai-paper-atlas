import json
from geometry import *
from cases import positive_cases,rejected_cases
rows=list(positive_cases());bad=list(rejected_cases())
if not all(accepted(*row) for row in rows):raise RuntimeError('positive certificate rejected')
if any(accepted(*row) for name,*row in bad):raise RuntimeError('negative certificate accepted')
a,b,c,d=point(0,0),point(1,0),point(2,3),point(4,-1)
k=construct(a,b,c,d)
print(json.dumps({'positive_certificates':len(rows),'negative_certificates':len(bad),
 'negative_names':[row[0] for row in bad],
 'example':{'E':list(map(str,k.e)),'G':list(map(str,k.g)),'H':list(map(str,k.h)),
 'radius_squared':str(k.radius_squared),'foot_line_parameter':str(foot_parameter(a,b,k.h)),
 'facts':check_certificate(a,b,c,d,k)},
 'scope':'Rational input families only; finite execution does not prove the general theorem.'},ensure_ascii=False,indent=2))
