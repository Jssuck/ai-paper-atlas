"""Independent audit, with hand-built certificates and mutation tests (stdlib only)."""
from fractions import Fraction as F
import copy, json, sys
import geometry as g
checks=0

def check(v,label):
 global checks
 checks+=1
 if not v: raise RuntimeError(label)

def manual(A,B,s,k=3):
 x,y=B[0]-A[0],B[1]-A[1]
 dx,dy=-s*y,s*x
 return {'points':{'A':A,'B':B,'C':(A[0]+k*dx,A[1]+k*dy),
                  'D':(A[0]+dx,A[1]+dy),'E':(B[0]+dx,B[1]+dy)},
         'side':s,'side_squared':x*x+y*y}
# Check accepted certificates without allowing the production generator to run.
original=g.construct
g.construct=lambda *args,**kwargs: (_ for _ in ()).throw(RuntimeError('generator called by verifier'))
valid=0
for A in [(F(2,7),F(-3,11)),(-9,8),(0,0)]:
 for x,y in [(F(a,3),F(b,5)) for a in range(-2,3) for b in range(-2,3) if a or b]:
  B=(A[0]+x,A[1]+y)
  for s in (-1,1):
   c=manual(A,B,s);valid+=1
   check(g.verify(A,B,s,c),'manual valid')
   p=c['points'];poly=[p[t] for t in 'ADEB']
   signed=sum(poly[i][0]*poly[(i+1)%4][1]-poly[i][1]*poly[(i+1)%4][0] for i in range(4))/F(2)
   check(signed==-s*(x*x+y*y),'orientation')
   check(g.area(poly)==x*x+y*y,'area')
   check(not g.verify(A,B,-s,c),'wrong requested side')
   for key in 'ABCDE':
    for dim in (0,1):
     bad=copy.deepcopy(c);q=list(bad['points'][key]);q[dim]+=F(1,13);bad['points'][key]=q
     if key=='C':
      # C may move along its same ray; independently test collinearity and beyond-D.
      wx,wy=p['D'][0]-A[0],p['D'][1]-A[1]
      cx,cy=q[0]-A[0],q[1]-A[1]
      expected=(cx*wy-cy*wx==0 and cx*wx+cy*wy>x*x+y*y)
      check(g.verify(A,B,s,bad)==expected,'perturbed auxiliary C')
     else:check(not g.verify(A,B,s,bad),'perturbed '+key)
   for k in (0,-1,1,F(1,2)):
    check(not g.verify(A,B,s,manual(A,B,s,k)),'invalid C position')
   check(g.verify(A,B,s,manual(A,B,s,F(101,100))),'any C beyond D')
   for key,value in [('side',True),('side',F(s)),('side_squared',float(x*x+y*y)),('side_squared',True)]:
    bad=copy.deepcopy(c);bad[key]=value
    check(not g.verify(A,B,s,bad),'metadata type')
   bad=copy.deepcopy(c);bad['points']['D'],bad['points']['E']=bad['points']['E'],bad['points']['D']
   check(not g.verify(A,B,s,bad),'crossed order')
   for key in ['unexpected','points']:
    bad=copy.deepcopy(c)
    if key=='unexpected':bad[key]=0
    else:bad[key]['unexpected']=(0,0)
    check(not g.verify(A,B,s,bad),'extra key')
g.construct=original
# Direct illegal-input rejection by both entry points.
invalid=0
for bad in [True,False,0.0,float('inf'),float('nan'),'0',None,complex(0)]:
 for location in (0,1):
  A=[0,0];A[location]=bad
  for fn in [lambda:g.construct(A,(1,0)),lambda:g.verify(A,(1,0),1,manual((0,0),(1,0),1))]:
   invalid+=1
   try:fn()
   except ValueError:check(True,'invalid coordinate')
   else:check(False,'accepted invalid coordinate')
for s in [True,False,F(1),F(-1),1.0,0,2,-2,None,'1']:
 for fn in [lambda:g.construct((0,0),(1,0),s),lambda:g.verify((0,0),(1,0),s,manual((0,0),(1,0),1))]:
  invalid+=1
  try:fn()
  except ValueError:check(True,'invalid side')
  else:check(False,'accepted side')
# Article examples plus coherent non-square counterexamples.
for A,B,s,D,E in [((1,2),(4,6),1,(-3,5),(0,9)),((1,2),(4,6),-1,(5,-1),(8,3)),((0,0),(2,1),1,(-1,2),(1,3)),((0,0),(2,1),-1,(1,-2),(3,-1))]:
 c=g.construct(A,B,s);check(c['points']['D']==D and c['points']['E']==E,'article example')
for B,D,E,C in [((5,0),(3,4),(8,4),(6,8)),((2,0),(0,1),(2,1),(0,2))]:
 c={'points':{'A':(0,0),'B':B,'C':C,'D':D,'E':E},'side':1,'side_squared':B[0]*B[0]}
 check(not g.verify((0,0),B,1,c),'coherent non-square')
print(json.dumps({'checks':checks,'independent_valid_cases':valid,'illegal_entrypoint_calls':invalid,'mode_optimize':sys.flags.optimize,'result':'PASS'}))
