"""Independent exact checks; finite evidence, not a general geometric proof."""
from fractions import Fraction as F
from itertools import combinations
from math import atan2
from copy import deepcopy
import json
import geometry as g

def need(x,msg):
    if not x: raise RuntimeError(msg)
def minus(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sq(a): return dot(a,a)
def midpoint(a,b): return tuple((x+y)/2 for x,y in zip(a,b))
def line(a,b):
    return (a[1]-b[1],b[0]-a[0],a[0]*b[1]-b[0]*a[1])
def intersection(a,c,b,d):
    p,q,r=line(a,c);u,v,w=line(b,d);den=p*v-u*q
    need(den!=0,'nonparallel test input')
    return ((q*w-v*r)/den,(r*u-w*p)/den)
def parameter(a,c,e):
    j=0 if c[0]!=a[0] else 1
    return (e[j]-a[j])/(c[j]-a[j])
def canon(x):
    if type(x) is F:return str(x)
    if type(x) is tuple:return [canon(y) for y in x]
    return x

ts=[F(-3),F(-2),F(-1),F(-1,2),F(0),F(1,2),F(1),F(2),F(3)]
pts=[((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in ts]+[(F(-1),F(0))]
# atan2 orders already exact rational test points only; expectations stay rational.
pts.sort(key=lambda p:atan2(float(p[1]),float(p[0])))
count=bad=both=app=0
for quad in combinations(pts,4):
    for scale,shift,reflect in [(F(1),(F(0),F(0)),False),(F(5,2),(F(3),F(-7)),True),(F(-3),(F(-2),F(4)),False)]:
        def tf(p):return (shift[0]+scale*(-p[0] if reflect else p[0]),shift[1]+scale*p[1])
        a,b,c,d=map(tf,quad);o=shift;r2=scale*scale
        e=intersection(a,c,b,d);v=minus(c,a);w=minus(d,b);t=parameter(a,c,e);u=parameter(b,d,e)
        need(0<t<1 and 0<u<1,'strict crossing')
        out=g.certificate(o,r2,a,c,b,d);need(g.verify(out),'self verification')
        ma=midpoint(a,c)==e;mb=midpoint(b,d)==e
        da=midpoint(a,c)==o;db=midpoint(b,d)==o
        expected={'E':canon(e),'t':str(t),'u':str(u),'det':str(v[0]*w[1]-v[1]*w[0]),'dot_v':str(dot(minus(e,o),v)),'dot_w':str(dot(minus(e,o),w)),
                  'midpoint_AC':ma,'midpoint_BD':mb,'diameter_AC':da,'diameter_BD':db,'theorem_applies':not da and not db,'both_midpoints':ma and mb,'at_center':e==o}
        for k,val in expected.items():need(type(out[k]) is type(val) and out[k]==val,'independent field '+k)
        need(not(ma and mb) or e==o,'center implication')
        for k in out:
            altered=deepcopy(out);altered[k]=None;need(g.verify(altered) is False,'field tamper '+k);bad+=1
        for k in ('midpoint_AC','midpoint_BD','diameter_AC','diameter_BD','theorem_applies','both_midpoints','at_center'):
            altered=deepcopy(out);altered[k]=int(altered[k]);need(g.verify(altered) is False,'boolean/int confusion');bad+=1
        count+=1;both+=ma and mb;app+=not da and not db
# Independent hand arithmetic checks matching all numerical body examples.
a=(F(-4),F(3));c=(F(4),F(3));b=(F(3),F(4));d=(F(-24,5),F(7,5));e=(F(0),F(3))
need(sq(d)==25,'D on circle');need(parameter(b,d,e)==F(5,13),'5/13')
need(sq(minus(b,e))==10 and sq(minus(d,e))==F(128,5),'squared distances')
need(midpoint(b,d)==(F(-9,10),F(27,10)),'BD midpoint')
need(intersection(a,c,(F(3),F(4)),(F(3),F(-4)))==(F(3),F(3)),'neither example')
need(intersection(a,c,(F(0),F(5)),(F(0),F(-5)))==e,'one diameter example')
need(g.certificate((0,0),25,(-5,0),(5,0),(0,5),(0,-5))['both_midpoints'] is True,'body two diameters')
base=g.examples()['only_AC_midpoint'];invalid=0
for key in ('O','A','B','C','D'):
    for value in (None,True,0,[],[0],[0,0,0],[True,0],[0.0,0],['2/2',0],['1/0',0],['nan',0]):
        z=deepcopy(base['input']);z[key]=value
        try:g.certificate(**z)
        except ValueError:invalid+=1
        else:raise RuntimeError('invalid point accepted')
for value in (0,-1,True,25.0,None,'2/2','1/0','nan'):
    z=deepcopy(base['input']);z['r2']=value
    try:g.certificate(**z)
    except ValueError:invalid+=1
    else:raise RuntimeError('invalid radius accepted')
for a,c,b,d in [((-4,3),(-4,3),(3,4),(3,-4)),((-4,3),(4,3),(-4,-3),(4,-3)),((-4,3),(4,3),(-4,3),(4,3)),((-4,3),(4,3),(4,3),(3,-4)),((-4,3),(4,3),(2,2),(3,-4))]:
    try:g.certificate((0,0),25,a,c,b,d)
    except ValueError:invalid+=1
    else:raise RuntimeError('invalid geometry accepted')
malformed=0
for z in (None,True,0,[],{}, {'input':None},{'input':[]},{'input':{}}):need(g.verify(z) is False,'malformed root');malformed+=1
for k in base:
    z=deepcopy(base);del z[k];need(g.verify(z) is False,'missing key');malformed+=1
z=deepcopy(base);z['extra']=0;need(g.verify(z) is False,'extra key');malformed+=1
for field in base['input']:
    z=deepcopy(base);z['input'][field]=None;need(g.verify(z) is False,'input tamper');malformed+=1
print(json.dumps({'method':'independent exact line-equation intersection and midpoint arithmetic; finite checks only','valid_certificates':count,'theorem_scope':app,'both_midpoints':both,'tampered_rejected':bad,'invalid_inputs_rejected':invalid,'malformed_certificates_rejected':malformed,'manual_checks':7,'passed':True},indent=2))
