from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
from itertools import product
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from euclid_i1 import Q3, construct, certificate
# Oracle uses coefficient tuples directly, never distance2/orientation/Q3 operators.
def minus(p,q):return (p[0]-q[0],p[1]-q[1])
def mul(p,q):return (p[0]*q[0]+3*p[1]*q[1],p[0]*q[1]+p[1]*q[0])
def plus(p,q):return (p[0]+q[0],p[1]+q[1])
def norm(c,p):
 d=[minus((c[i].a,c[i].b),(F(p[i]),F(0))) for i in range(2)]
 return plus(mul(d[0],d[0]),mul(d[1],d[1]))
def check(a,b):
 vs=construct(a,b); dx,dy=F(b[0])-a[0],F(b[1])-a[1]; r2=dx*dx+dy*dy
 for s,c in zip((1,-1),vs):
  if norm(c,a)!=(r2,0) or norm(c,b)!=(r2,0):raise RuntimeError('norm')
  # Determinant is independently calculated from returned coefficients.
  det=(dx*(c[1].a-a[1])-dy*(c[0].a-a[0]), dx*c[1].b-dy*c[0].b)
  if det!=(0,s*r2/2):raise RuntimeError('det')
  if not certificate(a,b,c)['accepted']:raise RuntimeError('certificate')
 return 2
stats={}
for label, pts in [('integer',list(product(range(-4,5),repeat=2))),('rational',[(F(i,3),F(j,5)) for i in range(-3,4) for j in range(-3,4)])]:
 n=0
 for a in pts:
  for b in pts:
   if a!=b:n+=check(a,b)
 stats[label]={'points':len(pts),'bases':len(pts)*(len(pts)-1),'triangles':n}
# A second test enumerates proposed vertices instead of using the constructor.
vals=[F(-1),F(-1,2),F(0),F(1,2),F(1)]; accepted=[]
for a,b,c,d in product(vals,repeat=4):
 p=(Q3(a,b),Q3(c,d)); oracle=(norm(p,(0,0))==(1,0) and norm(p,(1,0))==(1,0))
 actual=certificate((0,0),(1,0),p)['accepted']
 if oracle!=actual:raise RuntimeError('candidate mismatch')
 if actual:accepted.append([str(x) for x in (a,b,c,d)])
stats['candidate_grid']={'candidates':625,'accepted':accepted}
# Rational interval oracle, independent of sign() square-comparison branch.
coeffs=sorted({F(i,j) for i in range(-9,10) for j in range(1,6)})
lo,hi=F(1732050807568877,10**15),F(1732050807568878,10**15)
if not lo*lo<3<hi*hi:raise RuntimeError('sqrt bound')
n=0
for a,b in product(coeffs,repeat=2):
 lower,upper=sorted((a+b*lo,a+b*hi))
 expected=0 if a==b==0 else 1 if lower>0 else -1 if upper<0 else None
 if expected is None:raise RuntimeError('increase interval precision')
 if Q3(a,b).sign()!=expected:raise RuntimeError('sign mismatch')
 n+=1
stats['sign_oracle']={'distinct_coefficients':len(coeffs),'pairs':n,'mismatches':0}
stats['mismatches']=0
print(json.dumps(stats,indent=2))
