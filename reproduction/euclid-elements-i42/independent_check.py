"""Independent finite audit; does not prove Euclid's theorem."""
from fractions import Fraction as R
from itertools import product
from copy import deepcopy
import json, sys
from geometry import make_certificate, verify_certificate
n=0

def require(v):
 global n
 n+=1
 if not v: raise RuntimeError('independent audit failed at check '+str(n))
def minus(a,b):return (a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area2(ps):
 return abs(sum(ps[i][0]*ps[(i+1)%len(ps)][1]-ps[(i+1)%len(ps)][0]*ps[i][1] for i in range(len(ps))))
def readpoint(p):return tuple(R(x) for x in p)
count=0
for vx,vy,h,k,s in product([1,3,-2],[0,2,-3],[R(1,3),-2],[R(-3,2),0,5],[-4,0,2]):
 B=(R(2,7),R(-4,5));v=(R(vx),R(vy)); C=(B[0]+v[0],B[1]+v[1]);perp=(-v[1],v[0])
 A=(B[0]+k*v[0]+h*perp[0],B[1]+k*v[1]+h*perp[1]);u=(s*v[0]+h*perp[0],s*v[1]+h*perp[1])
 p={'A':A,'B':B,'C':C,'u':u};c=make_certificate(p);E,F,G=(readpoint(c['points'][x]) for x in ['E','F','G'])
 require(E==((B[0]+C[0])/2,(B[1]+C[1])/2))
 require(det(minus(F,A),v)==0 and det(minus(G,A),v)==0)
 require(minus(G,F)==minus(C,E) and minus(G,C)==minus(F,E))
 require(det(minus(F,E),u)==0 and sum(x*y for x,y in zip(minus(F,E),u))>0)
 require(area2([F,E,C,G])==area2([A,B,C]))
 require(area2([A,B,E])==area2([A,E,C]))
 require(area2([A,B,C])==area2([A,B,E])+area2([A,E,C]))
 require(R(c['double_areas']['FECG'])==area2([F,E,C,G]))
 require(verify_certificate(p,c))
 for key in ['parameter_t','kind','scope']:
  tamper=deepcopy(c);tamper[key]='invalid';require(not verify_certificate(p,tamper))
 for label in ['E','F','G']:
  tamper=deepcopy(c);tamper['points'][label][0]=str(R(tamper['points'][label][0])+1);require(not verify_certificate(p,tamper))
 for label in ['ABC','ABE','AEC','FECG']:
  tamper=deepcopy(c);tamper['double_areas'][label]='0';require(not verify_certificate(p,tamper))
 q=deepcopy(p);q['u']=tuple(3*x for x in u);other=make_certificate(q)
 require(other['points']==c['points']);require(not verify_certificate(q,c))
 q=deepcopy(p);q['u']=tuple(-x for x in u)
 try: make_certificate(q)
 except ValueError:require(True)
 else:require(False)
 count+=1
base={'A':(1,4),'B':(0,0),'C':(6,0),'u':(1,1)}
for u,F,G in [((1,1),(7,4),(10,4)),((-1,1),(-1,4),(2,4)),((0,1),(3,4),(6,4)),((-1,2),(1,4),(4,4)),((-5,4),(-2,4),(1,4)),((100,1),(403,4),(406,4)),((2,1),(11,4),(14,4))]:
 p=dict(base,u=u);c=make_certificate(p);require(readpoint(c['points']['F'])==F);require(readpoint(c['points']['G'])==G);require(R(c['double_areas']['ABC'])==24)
for key,val in [('A',(0,0)),('C',(0,0)),('u',(0,0)),('u',(1,0)),('u',(-1,0)),('u',(1,-1)),('A',(True,4)),('A',(1.,4)),('A',('1',4)),('u',(1,)),('u',None)]:
 p=dict(base);p[key]=val
 try:make_certificate(p)
 except ValueError:require(True)
 else:require(False)
 require(not verify_certificate(p,{}))
c=make_certificate(base)
for bad in [None,True,3,[],{}, {'x':float('nan')},{'x':set()}]:require(not verify_certificate(base,bad))
circular={};circular['x']=circular;require(not verify_certificate(base,circular))
tamper=deepcopy(c);tamper['parameter_t']=True;require(not verify_certificate(base,tamper))
tamper=deepcopy(c);tamper['extra']=1;require(not verify_certificate(base,tamper))
tamper=deepcopy(c);tamper['chain'].reverse();require(not verify_certificate(base,tamper))
print(json.dumps({'checks':n,'generated_valid_cases':count,'optimization':sys.flags.optimize,'passed':True,'scope':'finite independent coordinate and certificate audit; no general theorem proof'},sort_keys=True))
