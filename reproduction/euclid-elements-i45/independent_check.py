"""Independent reviewer checks; exact predicates separate from geometry helpers."""
from fractions import Fraction as F
from copy import deepcopy
import json
from geometry import construct,verify
checks=0

def ck(ok,label):
 global checks
 checks+=1
 if not ok: raise RuntimeError(label)
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def dif(a,b): return (a[0]-b[0],a[1]-b[1])
def orient(a,b,c): return det(dif(b,a),dif(c,a))
def ar(v): return abs(sum(v[i][0]*v[(i+1)%len(v)][1]-v[i][1]*v[(i+1)%len(v)][0] for i in range(len(v))))/F(2)
def oracle(v,h,p,q,c):
 A,B,C,D=v; P=c['points'];K,Fp,G,H,L,M=(P[k]for k in 'KFGHLM')
 s1=ar([A,B,D]);s2=ar([D,B,C]);total=ar(v)
 ck(s1+s2==total,'input partition');ck(orient(D,B,A)*orient(D,B,C)<0,'DB opposite sides')
 ck(c['areas']==(s1,s2,total),'reported areas')
 ck(ar([K,Fp,G,H])==s1,'first area');ck(ar([H,G,L,M])==s2,'second area');ck(ar([K,Fp,L,M])==total,'outer area')
 ck(orient(K,H,M)==0 and K[0]<H[0]<M[0],'lower order');ck(orient(Fp,G,L)==0 and Fp[0]<G[0]<L[0],'upper order')
 ck(dif(Fp,K)==dif(G,H)==dif(L,M),'shared cross-edge')
 ck(orient(H,G,K)*orient(H,G,M)<0,'non-overlap opposite halfplanes')
 ck(orient(H,G,Fp)*orient(H,G,L)<0,'both far vertices opposite')
 ck(det(dif(Fp,K),dif(M,L))==0 and det(dif(L,Fp),dif(K,M))==0,'outer parallels')
 ck(det(dif(Fp,K),(p,q))==0 and dif(Fp,K)[1]>0 and M[0]>0,'target angle ray')
 # Parameter strip inverse: x = X - (p/q)Y, y=Y/h.
 coords=lambda t:(t[0]-F(p,q)*t[1],t[1]/h)
 ck([coords(P[k]) for k in 'KFGH']==[(0,0),(0,1),(s1/h,1),(s1/h,0)],'first parameter rectangle')
 ck([coords(P[k]) for k in 'HGLM']==[(s1/h,0),(s1/h,1),(total/h,1),(total/h,0)],'second parameter rectangle')
 ck(verify(v,h,p,q,c),'accept valid')
 # Every coordinate mutation independently rejected, also point-name swaps.
 for k in 'KFGHLM':
  for j in (0,1):
   bad=deepcopy(c);z=list(bad['points'][k]);z[j]+=F(1,7);bad['points'][k]=tuple(z)
   ck(not verify(v,h,p,q,bad),'coordinate mutation')
 bad=deepcopy(c);bad['points']['F'],bad['points']['G']=bad['points']['G'],bad['points']['F'];ck(not verify(v,h,p,q,bad),'name swap')
 ck(construct(v,h,2*p,2*q)==c,'angle ray scale')

bases=[[(0,0),(3,0),(5,2),(-1,3)],[(0,0),(5,0),(4,4),(0,1)],[(0,0),(2,0),(2,3),(0,3)]]
count=0
for base in bases:
 for reverse in (False,True):
  for scale in (F(1,3),F(5,2)):
   v=[(F(x)*scale+F(2,7),F(y)*scale-F(4,9))for x,y in base]
   if reverse:v=v[::-1]
   for h in (F(1,2),F(3)):
    for p,q in ((-3,2),(0,3),(4,5)):
     oracle(v,h,p,q,construct(v,h,p,q));count+=1
base=[(0,0),(4,0),(5,3),(0,2)];ref=construct(base)
invalid=[([],2,1,2),(base[:3],2,1,2),(base+[base[0]],2,1,2),([(0,0),(2,2),(0,2),(2,0)],2,1,2),([(0,0),(4,0),(1,1),(0,3)],2,1,2),([(0,0),(4,0),(4,0),(0,3)],2,1,2),([(0,0),(2,0),(4,0),(0,3)],2,1,2)]
for h,p,q in [(0,1,2),(-1,1,2),(2,1,0),(2,1,-2),(True,1,2),(2,False,2),(2,1,True),(2.0,1,2),(2,1.0,2),(2,1,2.0)]:invalid.append((base,h,p,q))
for n in [True,False,0.0,'0',None]:invalid.append(([(n,0),(4,0),(5,3),(0,2)],2,1,2))
for args in invalid:
 try:construct(*args)
 except ValueError:ck(True,'direct reject')
 else:ck(False,'must reject invalid')
 ck(not verify(*args,ref),'reject invalid verify')
for key in ('points','areas'):
 bad=deepcopy(ref);del bad[key];ck(not verify(base,2,1,2,bad),'missing key')
for val in (None,[],1,True,'bad',{}, {'points':{},'areas':()}):ck(not verify(base,2,1,2,val),'schema')
for replacement in (0,False,0.0,'0',None):
 bad=deepcopy(ref);bad['points']['K']=(replacement,F(0));ck(not verify(base,2,1,2,bad),'point type')
for replacement in ((4,7,11),(True,F(7),F(11)),[F(4),F(7),F(11)],(F(4),F(7),F(12))):
 bad=deepcopy(ref);bad['areas']=replacement;ck(not verify(base,2,1,2,bad),'area schema')
bad=deepcopy(ref);bad['extra']=True;ck(not verify(base,2,1,2,bad),'extra key')
# Article example and h=1 answer.
ck(ref['areas']==(4,7,11),'article areas');ck(ref['points']['L']==(F(13,2),F(2)),'article L')
alt=construct(base,1,1,2);ck(alt['points']==dict(K=(F(0),F(0)),F=(F(1,2),F(1)),G=(F(9,2),F(1)),H=(F(4),F(0)),L=(F(23,2),F(1)),M=(F(11),F(0))),'exercise 8')
print(json.dumps({'checks':checks,'independent_valid_cases':count,'invalid_direct_cases':len(invalid),'status':'passed','arithmetic':'Fraction','scope':'strict convex quadrilaterals; not a general theorem proof'},sort_keys=True))
