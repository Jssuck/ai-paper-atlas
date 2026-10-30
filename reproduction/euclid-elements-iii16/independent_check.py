"""Independent exact checks: raw coordinates and determinant distances.
Finite tests verify implementation, not the real-number theorem.
"""
from fractions import Fraction as F
import copy,json
import geometry as g

def ck(v,msg):
 if not v:raise RuntimeError(msg)
def norm(p):return p[0]*p[0]+p[1]*p[1]
def power(c,p):return (p[0]-c.center[0])**2+(p[1]-c.center[1])**2-c.radius2
count=reverse=projection=tamper=sample=second=local=0
for o in [(F(0),F(0)),(F(2,3),F(-7,4)),(F(-5),F(6))]:
 for rad in [(F(1),F(0)),(F(2),F(3)),(F(-3,5),F(7,4)),(F(0),F(-4))]:
  p=(o[0]+rad[0],o[1]+rad[1]);c=g.Circle(o,norm(rad))
  for x in range(-5,6):
   for y in range(-4,5):
    if x==y==0:continue
    u=(F(x,3),F(y,2));q=norm(u);a=g.analyze(c,p,u);count+=1
    deriv=2*(rad[0]*u[0]+rad[1]*u[1])
    expected='tangent' if deriv==0 else ('inward' if deriv<0 else 'outward')
    ck(a['kind']==expected,'direction classification')
    determinant=rad[0]*u[1]-rad[1]*u[0]
    ck(a['distance2']==determinant**2/q,'determinant distance')
    foot=a['foot'];ck((foot[0]-o[0])*u[0]+(foot[1]-o[1])*u[1]==0,'foot orthogonality')
    projection+=1
    for t in [F(0),F(1,101),F(2,7),F(9)]:
     point=(p[0]+t*u[0],p[1]+t*u[1]);pv=power(c,point)
     ck(g.ray_power(c,p,u,t)==pv,'direct ray power');sample+=1
     ck(pv==q*t*t+deriv*t,'polynomial')
    b=g.analyze(c,p,(-u[0],-u[1]));reverse+=1
    ck(a['foot']==b['foot'] and a['second_point']==b['second_point'],'reverse geometry')
    if deriv!=0:
     t=-deriv/q;ck(a['second_parameter']==t,'root parameter')
     pt=(p[0]+t*u[0],p[1]+t*u[1]);ck(a['second_point']==pt and power(c,pt)==0,'second root');second+=1
    if deriv<0:
     ck(power(c,a['interior_point'])<0,'strict interior')
     # A rational parameter below both entry interval and epsilon/(|ux|+|uy|).
     for eps in [F(1),F(1,1000000)]:
      t=min(-deriv/(2*q),eps/(2*(abs(u[0])+abs(u[1]))))
      point=(p[0]+t*u[0],p[1]+t*u[1]);ck(power(c,point)<0,'local inside')
      ck(t*t*q<eps*eps,'local epsilon');local+=1
    ck(g.verify(c,p,u,a),'valid certificate')
    for key in ['q','k','distance2','foot_parameter']:
     z=copy.deepcopy(a);z[key]+=1;ck(not g.verify(c,p,u,z),'numeric tamper');tamper+=1
    for z in [{},None,dict(a,extra=1),dict(a,q=True)]:ck(not g.verify(c,p,u,z),'malformed cert');tamper+=1
narrow=0
for n in [1,7,101,10**6,10**30]:
 a=g.narrow_example(n);ck(a['interior_power']==-F(1,n*n+1),'narrow exact');narrow+=1
bad=[lambda:g.Circle((0,0),0),lambda:g.Circle((0,0),-1),lambda:g.Circle((0,0),True),lambda:g.Circle((0.,0),1),lambda:g.Circle((0,),1),lambda:g.analyze(None,(0,0),(1,0)),lambda:g.analyze(g.Circle((0,0),1),(0,0),(1,0)),lambda:g.analyze(g.Circle((0,0),1),(1,0),(0,0)),lambda:g.analyze(g.Circle((0,0),1),(True,0),(1,0)),lambda:g.analyze(g.Circle((0,0),1),(1,0),(1.,0)),lambda:g.ray_power(g.Circle((0,0),1),(1,0),(1,0),-1),lambda:g.narrow_example(0),lambda:g.narrow_example(-1),lambda:g.narrow_example(True),lambda:g.narrow_example(1.)]
for f in bad:
 try:f()
 except (ValueError,TypeError):pass
 else:raise RuntimeError('invalid accepted')
print(json.dumps(dict(configurations=count,reversals=reverse,determinant_projection=projection,ray_samples=sample,second_roots=second,local_epsilon_witnesses=local,tamper_rejected=tamper,narrow_cases=narrow,invalid_rejected=len(bad)),sort_keys=True))
