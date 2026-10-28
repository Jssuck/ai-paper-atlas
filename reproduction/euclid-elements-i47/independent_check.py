"""Independent finite adversarial checks; standard library only, no assert."""
from fractions import Fraction as F
from itertools import product
import json
import geometry as g
checks=0
valid=0
mutants=0
def need(ok,label):
    global checks
    checks+=1
    if not ok: raise RuntimeError(label)
def area(ps):
    return abs(sum(ps[i][0]*ps[(i+1)%len(ps)][1]-ps[(i+1)%len(ps)][0]*ps[i][1] for i in range(len(ps))))/2
def poly(c,labels):return area([c[x] for x in labels])
for origin,uv,scale,sign in product([(F(0),F(0)),(F(-7,11),F(13,17)),(F(100),F(-200))],[(F(1),F(0)),(F(2),F(7)),(F(-5,13),F(8,19)),(F(1,1000),F(-2000))],[F(1,7),F(7,3),F(1001,999)],[-1,1]):
    A=origin;B=(A[0]+uv[0],A[1]+uv[1]);C=(A[0]-sign*scale*uv[1],A[1]+sign*scale*uv[0])
    c=g.construct(A,B,C);need(g.verify(A,B,C,c),'valid rejected');valid+=1
    ab=sum((B[i]-A[i])**2 for i in (0,1));ac=sum((C[i]-A[i])**2 for i in (0,1))
    need(poly(c,'ABFG')==ab and poly(c,'ACKH')==ac,'leg squares')
    need(poly(c,'BDLM')==ab and poly(c,'MLEC')==ac,'block transfer')
    need(poly(c,'ABD')==poly(c,'FBC')==ab/2,'left triangle chain')
    need(poly(c,'ACE')==poly(c,'KCB')==ac/2,'right triangle chain')
    need(poly(c,'BDEC')==ab+ac,'partition')
    for name,axis in product(c,(0,1)):
        d=dict(c);p=list(c[name]);p[axis]+=F(2,7);d[name]=tuple(p)
        need(not g.verify(A,B,C,d),'accepted shifted '+name);mutants+=1
    for x,y in [('F','G'),('H','K'),('D','E'),('M','L')]:
        d=dict(c);d[x],d[y]=d[y],d[x];need(not g.verify(A,B,C,d),'accepted swapped '+x+y);mutants+=1
    for endpoint,edge in [('B','D'),('C','E')]:
        d=dict(c);d['M']=c[endpoint];d['L']=c[edge];need(not g.verify(A,B,C,d),'endpoint foot');mutants+=1
    for name in c:
        d=dict(c);del d[name];need(not g.verify(A,B,C,d),'missing key');mutants+=1
A=(0,0);B=(3,0);C=(0,4);c=g.construct(A,B,C)
need(c['M']==(F(48,25),F(36,25)) and c['L']==(F(148,25),F(111,25)),'sample coordinates')
original=g.construct
def forbidden(*args):raise RuntimeError('verify must not regenerate certificate')
g.construct=forbidden
need(g.verify(A,B,C,c),'verify independently of constructor')
g.construct=original
for bad in [None,[],{},dict(c,Z=(0,0))]:need(not g.verify(A,B,C,bad),'malformed certificate')
for value in [(True,0),(0.0,0),('0',0),(0,),None]:
    d=dict(c);d['L']=value;need(not g.verify(A,B,C,d),'malformed point');mutants+=1
for bad in [((0,0),(3,0),(1,4)),((0,0),(0,0),(0,4)),((0,0),(3,0),(0,0)),((0,0),(3,0),(6,0)),((False,0),(3,0),(0,4)),((0.0,0),(3,0),(0,4))]:
    rejected=False
    try:g.construct(*bad)
    except ValueError:rejected=True
    need(rejected,'invalid construction accepted');need(not g.verify(*bad,c),'invalid request accepted')
print(json.dumps({'independent_checks':checks,'valid_configurations':valid,'mutated_certificates':mutants,'result':'PASS','arithmetic':'exact fractions; independent shoelace expectations','general_theorem_proved_by_tests':False},sort_keys=True))
