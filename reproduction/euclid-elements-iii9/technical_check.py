import itertools,json
from fractions import Fraction as Q
from geometry import circumcenter,make_certificate,verify_certificate,certify_known_circle
count=0
for coords in [((5,0),(0,5),(-3,-4)),((5,0),(-5,0),(0,5))]:
 for pts in itertools.permutations(coords):
  for sx,sy in [(Q(2,3),Q(2,3)),(Q(-2,3),Q(2,3))]:
   p=[(x*sx+Q(7,11),y*sy-Q(2,7)) for x,y in pts]; o=(Q(7,11),-Q(2,7))
   got=circumcenter(p)
   if got!=o:raise RuntimeError('wrong center')
   cert=certify_known_circle(p,o,o,Q(100,9))
   if not verify_certificate(cert):raise RuntimeError('invalid certificate')
   for x,y in p:
    if (x-got[0])**2+(y-got[1])**2!=Q(100,9):raise RuntimeError('independent residual')
   count+=1
for eps in [Q(1,100),Q(1,2),Q(1),Q(3)]:
 p=[(-1,0),(1,0),(0,eps)]
 if circumcenter(p)!=(0,(eps*eps-1)/(2*eps)):raise RuntimeError('epsilon-family')
print(json.dumps({'permutation_similarity_certificates':count,'epsilon_family_cases':4,'result':'PASS'},indent=2))
