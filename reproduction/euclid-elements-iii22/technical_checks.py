"""Independent finite reviewer checks, not a proof of the general theorem."""
from fractions import Fraction as F
from itertools import combinations, permutations
import math,json
from geometry import certificate

def require(ok):
    if not ok: raise RuntimeError('independent check failed')
def sq(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def angle(a,b,c):
    ab,bc,ac=map(float,(sq(a,b),sq(b,c),sq(a,c)))
    return math.acos(max(-1,min(1,(ab+bc-ac)/(2*math.sqrt(ab*bc)))))
def ratio(a,b,c):
    area=abs((a[0]-b[0])*(c[1]-b[1])-(a[1]-b[1])*(c[0]-b[0]))
    return (sq(a,b)+sq(b,c)-sq(a,c))/(2*area)
def reject(q,o=(0,0),r=1):
    try:certificate(q,o,r)
    except (ValueError,TypeError):return
    raise RuntimeError('invalid input accepted')
params=[F(-7,3),F(-5,4),F(-1,7),F(2,7),F(4,3),F(7,2)]
pts=[((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in params]+[(F(-1),F(0))]
pts.sort(key=lambda p:math.atan2(float(p[1]),float(p[0])))
accepted=rejected=0; error=0.0
for quad in combinations(pts,4):
    legal={tuple((start+direction*i)%4 for i in range(4)) for start in range(4) for direction in (-1,1)}
    for perm in permutations(range(4)):
        q=tuple(quad[i] for i in perm)
        for mode in range(3):
            # Identity, rotated/scaled/translated, reflected/scaled/translated.
            if mode==0:p=q;o=(0,0);r=F(1)
            elif mode==1:p=tuple((F(2)+3*x-4*y,F(-7)+4*x+3*y) for x,y in q);o=(2,-7);r=F(25)
            else:p=tuple((F(-3)+2*x,F(8)-2*y) for x,y in q);o=(-3,8);r=F(4)
            if perm not in legal:reject(p,o,r);rejected+=1;continue
            z=certificate(p,o,r);accepted+=1
            c=tuple(ratio(p[(i-1)%4],p[i],p[(i+1)%4]) for i in range(4))
            require(z['cots']==c and z['opposite_sums']==(0,0))
            require(z['same_segment']==(True,True) and z['split_matches_D'] and z['triangle_sum']==0)
            a=[angle(p[(i-1)%4],p[i],p[(i+1)%4]) for i in range(4)]
            for i in (0,1):error=max(error,abs(a[i]+a[i+2]-math.pi))
require(accepted==840 and rejected==1680 and error<1e-12)
q=((-3,4),(0,5),(3,4),(0,-5))
require(certificate(q,(0,0),25)['cots']==(0,F(-4,3),0,F(4,3)))
# The body's noncyclic convex example has the exact stated cotangents.
require(ratio((-1,0),(0,1),(1,0))==0)
require(ratio((-1,0),(0,-2),(1,0))==F(3,4))
# Converse algebra, without assuming the fourth point lies on a circle.
converse=0
for a in (F(1),F(2),F(5,3)):
 for b in (F(-2),F(0),F(3,2)):
  for s in (F(1),F(2),F(4,3)):
   h=(b*b+s*s-a*a)/(2*s)
   for d in (F(-1),F(0),F(2)):
    for t in (F(-1),F(-2),F(-3,2)):
     cb=ratio((-a,0),(b,s),(a,0));cd=ratio((-a,0),(d,t),(a,0))
     require((cb+cd==0)==(d*d+t*t-a*a==2*h*t));converse+=1
Q=((1,0),(0,1),(-1,0),(0,-1));invalid=0
for q in (Q[:3],Q+(Q[0],),(Q[0],Q[0],Q[2],Q[3]),(Q[0],Q[1],Q[2],(0,0)),((True,0),*Q[1:]),((1.0,0),*Q[1:])):
 reject(q);invalid+=1
for r in (0,-1,True,1.0):reject(Q,r=r);invalid+=1
print(json.dumps(dict(accepted_ordered_configurations=accepted,rejected_crossed_orders=rejected,independent_acos_max_error=error,converse_algebra_cases=converse,additional_invalid_inputs=invalid,body_examples='pass',scope='finite independent review checks; not a general proof'),indent=2))
