"""Independent rational radical-axis oracle and adversarial candidate checks.
Run from the reproduction directory: python independent-review/check.py.
No random data, files changed, network, or third-party dependencies.
"""
import sys,json
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from geometry import Circle,relation,verify_contact,contact_candidate,interiors_disjoint

def check(condition,message):
    if not condition:raise RuntimeError(message)
def oracle(x,y,R,r):
    # Radical-axis foot F+t(G-F), independent of radius-sum comparison.
    q=x*x+y*y
    if q==0:return ('coincident' if R==r else 'concentric_disjoint'),None
    t=Q(q+R*R-r*r,2*q)
    h2=R*R-t*t*q
    if h2>0:return 'secant',None
    if h2==0:return ('external_tangent' if 0<t<1 else 'internal_tangent'),(t*x,t*y)
    return ('strictly_nested' if t<0 or t>1 else 'separate'),None

classes={};candidates=0;accepted=0;mutations=0;swaps=0
for x in range(-5,6):
 for y in range(-5,6):
  for R in range(1,5):
   for r in range(1,5):
    a=Circle((0,0),R);b=Circle((x,y),r);name,t=oracle(x,y,R,r)
    check(relation(a,b)==name,'classification mismatch')
    classes[name]=classes.get(name,0)+1
    check(interiors_disjoint(a,b)==(name in ('separate','external_tangent')),'interior mismatch')
    for u in range(-3,4):
     for v in range(-3,4):
      candidates+=1;should=name=='external_tangent' and (Q(u),Q(v))==t
      try:c=verify_contact(a,b,(u,v))
      except ValueError:check(not should,'valid candidate rejected')
      else:
       check(should,'bad candidate accepted');accepted+=1
       check(c['cross']==0 and c['strictly_between'],'certificate conclusion wrong')
    if name=='external_tangent':
     check(contact_candidate(a,b)==t,'constructor mismatch')
     check(contact_candidate(b,a)==t,'swap mismatch');verify_contact(b,a,t);swaps+=1
     for du,dv in [(Q(1,10**20),0),(0,Q(-1,10**20)),(1,1)]:
      try:verify_contact(a,b,(t[0]+du,t[1]+dv))
      except ValueError:mutations+=1
      else:raise RuntimeError('mutated contact accepted')
    else:
     try:contact_candidate(a,b)
     except ValueError:pass
     else:raise RuntimeError('nonexternal constructor accepted')
# The exact numbers from the prose, independently checked.
a=Circle((0,0),2);b=Circle((3,4),3);t=(Q(6,5),Q(8,5))
check(contact_candidate(a,b)==t,'prose contact wrong');verify_contact(a,b,t)
for x,y,R,r,t in [(6,0,5,5,(3,4)),(3,0,5,2,(5,0)),(6,0,2,2,(2,0))]:
 try:verify_contact(Circle((0,0),R),Circle((x,y),r),t)
 except ValueError:pass
 else:raise RuntimeError('prose counterexample accepted')
# Exact scalar restrictions are part of the declared domain.
invalid=0
for value in [0,-1,Q(-1,2),True,False,1.0,'1',None,complex(1,0)]:
 try:Circle((0,0),value)
 except (ValueError,TypeError):invalid+=1
 else:raise RuntimeError('invalid radius accepted')
for p in [(1,), (1,2,3), (True,0), (0,1.0), ('1',0), None]:
 try:Circle(p,1)
 except (ValueError,TypeError):invalid+=1
 else:raise RuntimeError('invalid point accepted')
print(json.dumps({'classification_pairs':sum(classes.values()),'classes':classes,'candidate_checks':candidates,'accepted_integer_candidates':accepted,'swapped_external_contacts':swaps,'mutated_contacts_rejected':mutations,'invalid_inputs_rejected':invalid,'prose_examples_checked':4,'result':'PASS','scope':'finite exact rational checks, not a proof'},sort_keys=True,indent=2))
