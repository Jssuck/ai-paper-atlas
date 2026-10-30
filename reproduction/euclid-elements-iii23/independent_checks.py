"""Independent finite checks: arbitrary rational points determine circles.
No network, no external data. Explicit checks survive Python optimization.
"""
from fractions import Fraction as F
from itertools import combinations
import json
import geometry as g

def require(ok, message):
    if not ok: raise ArithmeticError(message)
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def norm2(a): return dot(a,a)
def angle(a,p,b):
    v,w=sub(a,p),sub(b,p)
    d=abs(det(v,w))
    if not d: raise ValueError('collinear angle')
    return dot(v,w)/d
A=(F(-1),F(0)); B=(F(1),F(0))
# Generate P independently, then infer centre from OA^2=OP^2.
points=0; mirrors=0
for nx in range(-7,8):
 for ny in range(-6,7):
  if not ny: continue
  p=(F(nx,3),F(ny,5))
  k=(norm2(p)-norm2(A))/(2*p[1])
  o=(F(0),k)
  require(norm2(sub(p,o))==norm2(sub(A,o))==norm2(sub(B,o)), 'equidistance')
  require(g.residual(k,p)==0,'production residual')
  require(g.cot(p)==angle(A,p,B),'general angle dot/det')
  require(g.segment_cot(k,1 if ny>0 else -1)==angle(A,p,B),'side angle')
  if p[0]!=-1:
   t=p[1]/(p[0]+1)
   require(g.point(k,t)==p,'inverse point reconstruction')
  q=(p[0],-p[1]); oq=(F(0),-k)
  require(angle(A,p,B)==angle(A,q,B),'mirror angle')
  require(norm2(sub(A,p))==norm2(sub(A,q)) and norm2(sub(B,p))==norm2(sub(B,q)), 'mirror preserves distances')
  require(p!=q and norm2(sub(p,o))==norm2(sub(q,oq)), 'mirror noncoincident and same radius')
  points+=1; mirrors+=1
# Independently check witness output using distances and arbitrary-angle vectors.
ks=[F(n,3) for n in range(-12,13)]
witnesses=0
for lo,hi in combinations(ks,2):
 z=g.ordered_witness(lo,hi); c,d=z['C'],z['D']
 ac,ad=sub(c,A),sub(d,A)
 require(det(ac,ad)==0 and 0<dot(ac,ad)<norm2(ad),'between on ray')
 require(norm2(sub(c,(0,lo)))==1+lo*lo,'inner circle distance')
 require(norm2(sub(d,(0,hi)))==1+hi*hi,'outer circle distance')
 require(norm2(sub(c,(0,hi)))<1+hi*hi,'C inside outer by distances')
 require(norm2(sub(d,(0,lo)))>1+lo*lo,'D outside inner by distances')
 require(det(sub(A,c),sub(d,c))==0 and dot(sub(A,c),sub(d,c))<0,'CA opposite CD')
 require(det(sub(A,d),sub(c,d))==0 and dot(sub(A,d),sub(c,d))>0,'DA same DC')
 require(angle(A,c,B)<angle(A,d,B)==angle(c,d,B),'cot order of exterior and remote interior')
 witnesses+=1
# Check containment at a Cartesian grid, not generated circle-ray boundary points.
containment=0
for lo,hi in ((F(-3),F(-2)),(F(-1),F(1)),(F(0),F(2)),(F(2),F(3))):
 for nx in range(-15,16):
  for ny in range(1,31):
   p=(F(nx,5),F(ny,5))
   low=norm2(sub(p,(0,lo)))<=1+lo*lo
   high=norm2(sub(p,(0,hi)))<=1+hi*hi
   require(g.inside(lo,p)==low and g.inside(hi,p)==high,'membership agrees with centre-distance')
   require(not low or high,'grid containment')
   containment+=1
invalid=[(g.point,(0,0)),(g.point,(-1,1)),(g.cot,(A,)),(g.cot,(B,)),(g.ordered_witness,(1,1)),(g.ordered_witness,(2,1)),(g.segment_cot,(1,0)),(g.inside,(1,(0,1),0))]
for fn,args in invalid:
 try: fn(*args)
 except ValueError: pass
 else: raise ArithmeticError('invalid input accepted: '+fn.__name__)
# Exact main-text example and exercise, independently numerical constants.
require(g.point(0,1)==(F(0),F(1)), 'article C')
require(g.point(F(3,4),1)==(F(3,4),F(7,4)), 'article D')
require(g.point(-2,F(1,4))==(F(-1,17),F(4,17)), 'exercise 4')
print(json.dumps(dict(arbitrary_rational_points=points,mirror_congruence_checks=mirrors,ordered_witnesses=witnesses,cartesian_membership_checks=containment,invalid_cases=len(invalid),main_text_exact_examples=3,result='PASS',scope='finite checks; not a general theorem proof'),indent=2))
