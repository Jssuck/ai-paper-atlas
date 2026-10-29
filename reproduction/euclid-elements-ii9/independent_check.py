"""Independent finite audit: external certificates, no production construct call."""
from fractions import Fraction as F
from copy import deepcopy
import json,sys
from geometry import verify, normalized_segments
counts=dict(certificates=0,square_comparisons=0,route_comparisons=0,right_angles=0,normalized_cases=0,tamper_rejections=0,invalid_rejections=0)
def check(ok,msg):
 if not ok:raise RuntimeError(msg)
def reject(call,key):
 try:call()
 except ValueError:counts[key]+=1
 else:raise RuntimeError('invalid input accepted')
def squared(p,a,b):return sum((p[a][j]-p[b][j])**2 for j in range(2))
bases=[((1,0),(0,1)),((0,1),(-1,0)),((1,0),(0,-1)),((3,4),(-4,3)),((F(3,5),F(4,5)),(F(-4,5),F(3,5))),((F(2,3),0),(0,F(-2,3)))]
for h in [F(1,2),F(3,2),F(5),F(13,3),F(100)]:
 for k in range(1,9):
  d=h*F(k,9)
  for bi,(u,v) in enumerate(bases):
   origin=(F(bi-2,3),F(7-bi,5));norm=sum(z*z for z in u)
   # Form D at distance h+d and intersect EB with its perpendicular.
   def point(x,y):return tuple(origin[j]+x*u[j]+y*v[j] for j in range(2))
   p={'A':point(0,0),'B':point(2*h,0),'C':point(h,0),'D':point(h+d,0),'E':point(h,h)}
   fraction_on_EB=d/h
   p['F']=tuple(p['E'][j]+fraction_on_EB*(p['B'][j]-p['E'][j]) for j in range(2))
   p['G']=point(h,h-d)
   cert={'points':p};r=verify(cert,h,d,origin,u,v);counts['certificates']+=1
   targets={'AC':h*h,'CE':h*h,'AE':2*h*h,'EG':d*d,'GF':d*d,'EF':2*d*d,'AF':2*(h*h+d*d),'AD':(h+d)**2,'DF':(h-d)**2,'DB':(h-d)**2,'CD':d*d}
   for edge,value in targets.items():
    check(r['squares'][edge]==squared(p,*edge)==value*norm,'square '+edge);counts['square_comparisons']+=1
   for triangle,right in [('ACE','C'),('ECB','C'),('EGF','G'),('FDB','D'),('AEF','E'),('ADF','D')]:
    a,b=[z for z in triangle if z!=right]
    check(sum((p[a][j]-p[right][j])*(p[b][j]-p[right][j]) for j in range(2))==0,'angle');counts['right_angles']+=1
   for route,(left,right) in r['routes'].items():check(left==right,'route');counts['route_comparisons']+=1
   check(r['lhs']==r['rhs']==2*(h*h+d*d)*norm,'conclusion')
   for sign in [-1,1]:
    n=normalized_segments(h,sign*d);check(n['AD_original']==h+sign*d and n['DB_original']==h-sign*d and n['swap_endpoints']==(sign==-1),'normalization');counts['normalized_cases']+=1
   for label in p:
    for axis in range(2):
     for delta in [F(1,7),F(-2,9)]:
      c=deepcopy(cert);v2=list(c['points'][label]);v2[axis]+=delta;c['points'][label]=tuple(v2)
      reject(lambda:verify(c,h,d,origin,u,v),'tamper_rejections')
    c=deepcopy(cert);del c['points'][label];reject(lambda:verify(c,h,d,origin,u,v),'tamper_rejections')
   c=deepcopy(cert);c['points']['Z']=point(0,0);reject(lambda:verify(c,h,d,origin,u,v),'tamper_rejections')
   c=deepcopy(cert);c['extra']=0;reject(lambda:verify(c,h,d,origin,u,v),'tamper_rejections')
# Invalid parameter and certificate channels, including bool equals int traps.
p={'A':(0,0),'B':(10,0),'C':(5,0),'D':(7,0),'E':(5,5),'F':(7,3),'G':(5,3)};base={'points':p}
for h,d in [(0,1),(-5,2),(5,0),(5,5),(5,6),(5,-2),(True,1),(5,True),(5.0,2),(5,2.0),('5',2),(5,'2'),(None,2),(5,None)]:reject(lambda:verify(base,h,d),'invalid_rejections')
for field in ['origin','u','v']:
 for value in [None,1,'ab',(1,),[1,2,3],[True,0],[0,False],[1.0,0]]:
  reject(lambda:verify(base,**{field:value}),'invalid_rejections')
for u,v in [((0,0),(0,0)),((1,0),(1,1)),((1,0),(0,2)),((1,1),(1,1))]:reject(lambda:verify(base,u=u,v=v),'invalid_rejections')
for cert in [None,[],{}, {'points':None},{'points':[]}]:reject(lambda:verify(cert),'invalid_rejections')
for label in p:
 for value in [None,(1,),[True,0],[1.0,0]]:
  c=deepcopy(base);c['points'][label]=value;reject(lambda:verify(c),'invalid_rejections')
for h,t in [(5,0),(5,5),(5,-5),(5,6),(-5,2),(True,1),(5,True),(5,1.0),(5,None)]:reject(lambda:normalized_segments(h,t),'invalid_rejections')
report={'mode':('normal' if sys.flags.optimize==0 else '-O' if sys.flags.optimize==1 else '-OO'),'counts':counts,'status':'passed','external_certificate_generation':'independent intersection and affine map; no construct call','limits':'finite rational checks, not general proof; no Jupyter kernel'}
print(json.dumps(report,sort_keys=True))
