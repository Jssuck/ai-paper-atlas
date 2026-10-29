"""Independent technical audit: solve axis-circle equations before calling model.
Finite exact checks; no claim to prove the general theorem.
"""
from fractions import Fraction as F
from geometry import Circle,relation,contains,interiors_disjoint,contact_certificate,same_contact,chord_midpoint_certificate
import json

def check(condition,label):
 if not condition:raise RuntimeError(label)
def reject(call):
 try:call()
 except (ValueError,TypeError):return
 raise RuntimeError('invalid input was accepted')

stats={'circle_pairs':0,'candidate_tests':0,'contact_order_checks':0,'tamper_rejections':0,'chord_checks':0,'invalid_inputs':0}
radii=[F(1,3),F(1,2),F(1),F(3,2),F(2),F(3),F(4),F(5)]
distances=[F(k,6) for k in range(0,61)]
for R in radii:
 for r in radii:
  for d in distances:
   a,b=Circle((0,0),R),Circle((d,0),r)
   # Independent radical-axis elimination x=(R^2-r^2+d^2)/(2d).
   # For d>0, y^2=R^2-x^2 decides 0/1/2 real intersections.
   if not d:
    expected='coincident' if R==r else 'concentric_distinct'
    yy=None
   else:
    x=(R*R-r*r+d*d)/(2*d);yy=R*R-x*x
    if yy>0:expected='two_intersections'
    elif yy==0:expected='external_contact' if 0<x<d else 'internal_contact'
    else:expected='separate' if d>R+r else 'strict_containment'
   check(relation(a,b)==expected,'classification')
   check(contains(a,b)==(d+r<=R),'containment')
   check(interiors_disjoint(a,b)==(d>=R+r),'separation')
   stats['circle_pairs']+=1
   # Independent candidates are rational lattice points, not candidate formula outputs.
   for px,py in [(F(k,2),F(j,2)) for k in range(-2,13) for j in (-2,0,2)]:
    common=px*px+py*py==R*R and (px-d)**2+py*py==r*r
    for kind,pre in [('external',d>=R+r),('internal',d+min(R,r)<=max(R,r) and not(d==0 and R==r))]:
     valid=common and pre
     if valid:
      result=contact_certificate(a,b,(px,py),kind)
      check(result['point']==(px,py),'candidate')
     else:reject(lambda:contact_certificate(a,b,(px,py),kind))
     stats['candidate_tests']+=1
   if yy==0 and d:
    p=(x,F(0));kind='external' if expected=='external_contact' else 'internal'
    for aa,bb in [(a,b),(b,a)]:
     check(same_contact(aa,bb,p,p,kind),'swapped witness')
     stats['contact_order_checks']+=1
     for q in [(x,F(1,10**40)),(x+F(1,10**40),F(0)),(-x,F(1))]:
      reject(lambda:contact_certificate(aa,bb,q,kind));stats['tamper_rejections']+=1

# Exact common chords under independent similarities; unequal radii use 5 and 17/2.
for scale in [F(1,7),F(1),F(3,2),F(5)]:
 for u,v in [(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))]:
  for ox,oy in [(F(0),F(0)),(F(2,3),F(-4,7))]:
   def transform(x,y):return (ox+scale*(u*x-v*y),oy+scale*(v*x+u*y))
   for d,r in [(F(6),F(5)),(F(21,2),F(17,2))]:
    a,b=Circle(transform(0,0),5*scale),Circle(transform(d,0),r*scale)
    p,q=transform(3,4),transform(3,-4);m=transform(3,0)
    for aa,bb in [(a,b),(b,a)]:
     cert=chord_midpoint_certificate(aa,bb,p,q)
     check(cert=={'midpoint':m,'strict_squared_gap':16*scale*scale},'chord identity')
     for kind in ('external','internal'):reject(lambda:contact_certificate(aa,bb,p,kind))
     stats['chord_checks']+=1
bad=[lambda:Circle((0,0),0),lambda:Circle((0,0),-1),lambda:Circle((0,0),True),lambda:Circle((0,0),1.0),lambda:Circle((False,0),1),lambda:Circle((0.0,0),1),lambda:Circle((0,),1),lambda:Circle((0,0,0),1),lambda:Circle('00',1),lambda:Circle(None,1),lambda:relation(None,Circle((0,0),1)),lambda:contact_certificate(Circle((0,0),1),Circle((2,0),1),(1,False),'external'),lambda:contact_certificate(Circle((0,0),1),Circle((2,0),1),(1,0),'unknown'),lambda:chord_midpoint_certificate(Circle((0,0),1),Circle((0,0),1),(1,0),(1,0)),lambda:contact_certificate(Circle((0,0),1),Circle((0,0),1),(1,0),'internal')]
for f in bad:reject(f);stats['invalid_inputs']+=1
print(json.dumps(stats,sort_keys=True))
print('independent finite exact audit passed')
