"""Independent finite adversarial review; not a general geometric proof."""
from fractions import Fraction as Q
from copy import deepcopy
from itertools import product
import json
from geometry import make_certificate, verify_certificate

def need(ok,msg):
 if not ok: raise RuntimeError(msg)
def pack(a,u,w):
 return {k:[str(x) for x in p] for k,p in zip('ABCD',(a,(a[0]+u[0],a[1]+u[1]),(a[0]+w[0],a[1]+w[1]),(a[0]+u[0]+w[0],a[1]+u[1]+w[1])))}
def reject(d):
 try: make_certificate(d)
 except ValueError:return
 raise RuntimeError('invalid geometry accepted')
def cross(x,y):return x[0]*y[1]-x[1]*y[0]
counts={'positive':0,'invalid_geometry':0,'certificate_attacks':0,'invalid_inputs':0}
for ux,uy,wx,wy in product(range(-2,3),repeat=4):
 u=(Q(ux,2),Q(uy,3));w=(Q(wx,5),Q(wy,7));det=cross(u,w)
 if not det:continue
 for a in [(Q(0),Q(0)),(Q(-2,3),Q(7,4)),(Q(3),Q(-2))]:
  d=pack(a,u,w);c=make_certificate(d)
  need(verify_certificate(d,c),'valid certificate rejected')
  C=c['conclusion']; need(C['AC_vector']==[str(x) for x in w] and C['BD_vector']==[str(x) for x in w],'wrong vectors')
  need(Q(C['AC_squared'])==sum(x*x for x in w) and C['AC_squared']==C['BD_squared'],'wrong lengths')
  need(Q(C['connector_cross'])==0 and Q(C['connector_support_cross'])==-det,'wrong line separation')
  need(c['sas']['included_dot_ABC']==c['sas']['included_dot_DCB'],'wrong SAS')
  counts['positive']+=1
  bad=[]
  z=deepcopy(d);z['C'],z['D']=z['D'],z['C'];bad.append(z)
  z=pack(a,u,w);z['D']=[str(a[i]+w[i]+2*u[i]) for i in range(2)];bad.append(z)
  z=pack(a,u,w);z['D']=[str(a[i]+w[i]+u[i]+w[i]) for i in range(2)];bad.append(z)
  z=pack(a,u,u);bad.append(z)
  z=deepcopy(d);z['B']=z['A'];bad.append(z)
  z=deepcopy(d);z['D']=z['C'];bad.append(z)
  for b in bad:
   reject(b);need(not verify_certificate(b,c),'invalid accepts valid cert');counts['invalid_geometry']+=1
  translated={k:[str(Q(v[0])+1),v[1]] for k,v in d.items()}
  need(not verify_certificate(translated,c),'not input bound')

base={'A':[0,0],'B':[4,0],'C':[1,3],'D':[5,3]};cert=make_certificate(base)
def paths(x,p=()):
 yield p
 if type(x) is dict:
  for k,v in x.items():yield from paths(v,p+(k,))
 if type(x) is list:
  for k,v in enumerate(x):yield from paths(v,p+(k,))
def get(x,p):
 for k in p:x=x[k]
 return x
def setval(x,p,v):
 if not p:return v
 get(x,p[:-1])[p[-1]]=v;return x
for p in paths(cert):
 old=get(cert,p)
 for v in [True,False,None,0,1,0.0,float('nan'),[],{},'forged','0/1']:
  if type(old)==type(v) and old==v:continue
  z=setval(deepcopy(cert),p,v)
  need(not verify_certificate(base,z),'mutation accepted '+str(p));counts['certificate_attacks']+=1
 if type(old) is dict:
  for k in old:
   z=deepcopy(cert);del get(z,p)[k];need(not verify_certificate(base,z),'missing key accepted');counts['certificate_attacks']+=1
  z=deepcopy(cert);get(z,p)['extra']='x';need(not verify_certificate(base,z),'extra accepted');counts['certificate_attacks']+=1
 if type(old) is list:
  z=setval(deepcopy(cert),p,tuple(old));need(not verify_certificate(base,z),'tuple accepted');counts['certificate_attacks']+=1
for k in 'ABCD':
 for i in range(2):
  for value in [True,False,None,0.0,1.0,float('inf'),float('nan'),[],{},'1/0','0/1','01','1.0','+1',' 1','1 ','NaN']:
   d=deepcopy(base);d[k][i]=value;reject(d);counts['invalid_inputs']+=1
 for value in [[],[0],[0,0,0],(0,0),None,{}]:
  d=deepcopy(base);d[k]=value;reject(d);counts['invalid_inputs']+=1
for d in [None,[],(),True,1,'ABCD',dict(base,extra=0)]:reject(d);counts['invalid_inputs']+=1
# Article hand calculations and exercise 4, independently evaluated.
u=(4,0);v=(1,3);need(cross((v[0]-u[0],v[1]-u[1]),(-u[0],-u[1]))==12,'side formula')
need(cross((5,3),(-3,3))==24,'crossed example')
need((5*Q(1,2),3*Q(1,2))==(4-3*Q(1,2),3*Q(1,2)),'intersection')
e=make_certificate({'A':[2,1],'B':[5,3],'C':[-1,4],'D':[2,6]});need(e['conclusion']['AC_squared']=='18','exercise')
print(json.dumps({'passed':True,**counts,'scope':'finite independent exact tests, not general proof'},sort_keys=True))
