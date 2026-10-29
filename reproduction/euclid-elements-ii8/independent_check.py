"""Independent II.8 certificates and area checks; finite evidence, not proof."""
from fractions import Fraction as F
from copy import deepcopy
import json
import geometry

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def external(a,b,o,u,v):
 xs=[0,a,a+b,a+2*b];ys=[0,b,2*b,a+2*b]
 names=['ACBD','MGKN','OQRP','EHLF']
 p={}
 for j,row in enumerate(names):
  for i,k in enumerate(row):p[k]=tuple(F(o[t])+xs[i]*u[t]+ys[j]*v[t] for t in range(2))
 return {'points':p}
def polygon(p,word):
 xy=[p[k] for k in word];total=F(0)
 for i,(x,y) in enumerate(xy):
  z,w=xy[(i+1)%len(xy)];total+=x*w-y*z
 return abs(total)/2

def rejected(c,**kwargs):
 try:geometry.verify(c,**kwargs)
 except ValueError:return
 raise RuntimeError('accepted invalid certificate')

def main():
 count=areas=tamp=invalid=0
 bases=[((1,0),(0,1)),((0,1),(-1,0)),((1,0),(0,-1)),((3,4),(-4,3)),((F(3,5),F(4,5)),(F(-4,5),F(3,5))),((2,0),(0,-2))]
 for i in range(1,41):
  a=F(i,7);b=F((i*7)%19+1,5)
  if i%8==0:b=a
  for u,v in bases:
   o=(F(i-20,3),F(9-i,4));c=external(a,b,o,u,v);kw=dict(a=a,b=b,origin=o,u=u,v=v)
   got=geometry.verify(c,**kw);p=c['points'];k=u[0]**2+u[1]**2;s=a+2*b
   expected={'CK':('CBKG',b*b*k),'KD':('BDNK',b*b*k),'GR':('GKRQ',b*b*k),'RN':('KNPR',b*b*k),'AG':('ACGM',a*b*k),'MQ':('MGQO',a*b*k),'QL':('QRLH',a*b*k),'RF':('RPFL',a*b*k),'OH':('OQHE',a*a*k),'AK':('ABKM',(a+b)*b*k),'whole':('ADFE',s*s*k),'gnomon':('ADFH QO'.replace(' ',''),4*(a+b)*b*k),'CP':('CDPQ',4*b*b*k),'ML':('MKLE',(a+b)**2*k)}
   for name,(word,value) in expected.items():
    need(polygon(p,word)==value==got[name],name);areas+=1
   need(polygon(p,'EQD')==polygon(p,'EKD')==0,'diagonal')
   need(sum(got[x] for x in ['CK','KD','GR','RN','AG','MQ','QL','RF','OH'])==got['whole'],'partition')
   for name in p:
    for axis in (0,1):
     bad=deepcopy(c);pt=list(bad['points'][name]);pt[axis]+=F(1,11);bad['points'][name]=pt;rejected(bad,**kw);tamp+=1
    bad=deepcopy(c);del bad['points'][name];rejected(bad,**kw);tamp+=1
    for badpt in [None,[],[0], [0,0,0],[False,0],[0.0,0],['0',0]]:
     bad=deepcopy(c);bad['points'][name]=badpt;rejected(bad,**kw);tamp+=1
   for bad in [None,[],{},dict(points=[]),dict(points=None),dict(points=p,extra=1),dict(points={**p,'Z':(0,0)})]:
    rejected(bad,**kw);tamp+=1
   count+=1
 c=external(F(3),F(2),(0,0),(1,0),(0,1))
 for field in ['a','b']:
  for val in [0,-1,F(-1,3),True,False,1.0,'1',None,[],{}]:
   rejected(c,**{field:val});invalid+=1
 for field in ['origin','u','v']:
  for val in [None,[],[0],[0,0,0],[False,0],[0.0,0],['0',0],{}]:
   rejected(c,**{field:val});invalid+=1
 for u,v in [((0,0),(0,0)),((1,0),(0,2)),((1,0),(1,1)),((1,0),(2,0)),((0,1),(0,-1))]:
  rejected(c,u=u,v=v);invalid+=1
 result={'external_certificates':count,'independent_region_area_comparisons':areas,'tampered_certificates_rejected':tamp,'invalid_parameters_rejected':invalid,'production_constructor_used_for_external_certificates':False,'status':'passed','scope':'finite exact rational teaching checks; not a general proof'}
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
