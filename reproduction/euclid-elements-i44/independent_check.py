"""Independent rational audit; finite tests, not a general proof."""
from fractions import Fraction as Q
from itertools import product
from copy import deepcopy
import json
from geometry import construct, verify

count=0

def check(ok, label):
    global count
    count+=1
    if not ok: raise RuntimeError(label)

def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def minus(u,v):return (u[0]-v[0],u[1]-v[1])
def plus(u,v):return (u[0]+v[0],u[1]+v[1])
def times(k,u):return (k*u[0],k*u[1])
def signed(P):return sum(cross(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def mag(P):return abs(signed(P))
def dot(u,v):return sum(x*y for x,y in zip(u,v))

valid=0
for a,b,S,p,q in product([Q(1,7),Q(2),Q(11,3)],[Q(1,9),Q(3),Q(13,2)],[Q(1,5),Q(12),Q(101,7)],[-7,-1,0,2,13],[Q(1,3),Q(5)]):
    valid+=1;c=construct(a,b,S,p,q);P=c['points'];poly=lambda names:mag([P[n] for n in names])
    check(verify(c),'generated certificate')
    check(P['A']==(-a,0) and P['B']==(0,0) and P['E']==(b,0),'prescribed baseline')
    # Solve H+t(B-H)=F+s(E-F) with independent 2x2 determinant algebra.
    u=minus(P['B'],P['H']);w=minus(P['E'],P['F']);rhs=minus(P['F'],P['H'])
    den=cross(u,w);check(den!=0,'unique intersection')
    t=cross(rhs,w)/den;s=cross(rhs,u)/den
    check(t>1 and s>1,'directed extensions')
    check(plus(P['H'],times(t,u))==P['K']==plus(P['F'],times(s,w)),'intersection solution')
    check(t==s==1+b/a,'derived parameters')
    check(P['H'][1]>0 and P['K'][1]<0,'opposite half planes')
    check(poly('BEFG')==S and poly('ABML')==S,'target area')
    check(cross(minus(P['B'],P['A']),minus(P['M'],P['L']))==0,'output parallel one')
    check(cross(minus(P['L'],P['A']),minus(P['M'],P['B']))==0,'output parallel two')
    check(poly('HLK')==poly('HKF'),'large diagonal split')
    check(poly('HAB')==poly('HGB'),'near H split')
    check(poly('BEK')==poly('BMK'),'near K split')
    check(poly('HLK')==poly('HAB')+poly('ABML')+poly('BMK'),'left dissection')
    check(poly('HKF')==poly('HGB')+poly('BEFG')+poly('BEK'),'right dissection')
    x=minus(P['E'],P['B']);y=minus(P['G'],P['B']);z=minus(P['A'],P['B']);w=minus(P['M'],P['B'])
    check(dot(x,y)*dot(z,w)>=0,'angle cosine sign')
    check(dot(x,y)**2*dot(z,z)*dot(w,w)==dot(z,w)**2*dot(x,x)*dot(y,y),'angle cosine squared')
    check(cross(x,z)==0 and dot(x,z)<0 and cross(y,w)==0 and dot(y,w)<0,'both rays reversed')
    c2=construct(a,b+1,S,p,q)
    check(all(c2['points'][k]==P[k] for k in 'ABML'),'seed width independence')
    for k in P:
        bad=deepcopy(c);bad['points'][k]=(P[k][0]+Q(1,103),P[k][1])
        check(not verify(bad),'tampered coordinate '+k)

bad_inputs=0
base=[2,3,5,1,2]
for ix in [0,1,2,4]:
    for value in [0,-1,Q(-1,7)]:
        args=base.copy();args[ix]=value;bad_inputs+=1
        try:construct(*args)
        except (TypeError,ValueError):check(True,'bad geometry rejected')
        else:check(False,'bad geometry accepted')
for ix in range(5):
    for value in [True,False,1.0,'1',None,[],{},complex(1,0)]:
        args=base.copy();args[ix]=value;bad_inputs+=1
        try:construct(*args)
        except (TypeError,ValueError):check(True,'bad type rejected')
        else:check(False,'bad type accepted')
c=construct(2,3,5,1,2)
for k,P in c['points'].items():
    bad=deepcopy(c);bad['points'][k]=(bool(P[0]),P[1]);check(not verify(bad),'bool coordinate rejected')
bad=deepcopy(c);bad['v']=(True,c['v'][1]);check(not verify(bad),'bool vector rejected')
# Article's two worked examples and exercises 9/10.
for args,expected in [((4,6,12,0,1),{'K':(6,-3),'M':(0,-3),'L':(-4,-3),'H':(-4,2)}),((3,4,12,-1,2),{'H':(Q(-9,2),3),'K':(6,-4),'M':(2,-4),'L':(-1,-4)}),((5,10,20,0,1),{'M':(0,-4),'K':(10,-4),'H':(-5,2)})]:
    P=construct(*args)['points']
    for k,expected_point in expected.items():check(P[k]==expected_point,'article '+k)
check(Q(6)*Q(2)*(Q(2,3)**2)==Q(16,3),'uniform scaling counterexample')
# One-ray reversal can retain area but changes the non-right angle.
c=construct(3,4,12,-1,2);P=c['points'];v=P['G'];badM=times(Q(4,3),v)
check(abs(cross((3,0),badM))==12,'false candidate area coincidence')
check(dot(minus(P['A'],P['B']),badM)>0 and dot(P['E'],P['G'])<0,'false candidate angle mismatch')
print(json.dumps({'independent_checks':count,'valid_cases':valid,'invalid_inputs':bad_inputs,'result':'PASS','scope':'finite rational coordinate, directed ray, angle, dissection and rejection audit'},sort_keys=True))
