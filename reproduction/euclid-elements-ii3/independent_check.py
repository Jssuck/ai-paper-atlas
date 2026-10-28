"""Independent II.3 checks: analytic area oracle and adversarial binding cases.
Finite testing is not a proof of the general proposition or a Python sandbox.
Run with python3, python3 -O, and python3 -OO.
"""
from fractions import Fraction as F
from copy import deepcopy
import json, sys
from geometry import construct, verify, area

counts={'valid':0,'rejected':0,'oracle_comparisons':0}
def require(ok,message):
    if not ok: raise RuntimeError(message)
def reject(args,cert,label):
    require(verify(*args,cert) is False,'accepted invalid '+label)
    counts['rejected']+=1

for A in [(0,0),(F(2,3),F(-4,7)),(-19,23)]:
    for u in [(7,0),(0,-3),(3,4),(-5,12),(F(2,7),F(-3,11))]:
        for t in [F(1,13),F(1,3),F(1,2),F(11,13)]:
            for sign in [-1,1]:
                v=(-sign*(1-t)*u[1],sign*(1-t)*u[0]);args=(A,u,v,t)
                cert=construct(*args)
                require(verify(*args,cert) is True,'valid certificate rejected')
                counts['valid']+=1
                n=u[0]*u[0]+u[1]*u[1]
                expected={'AE':n*(1-t),'AD':n*t*(1-t),'CE':n*(1-t)*(1-t)}
                for name,want in expected.items():
                    require(area(cert[name])==want,'analytic area mismatch '+name)
                    counts['oracle_comparisons']+=1
                # Disturb each label but retain the originally correct region cycles.
                for name in 'ABCDEF':
                    c=deepcopy(cert);x,y=c['points'][name];c['points'][name]=(x+F(1,17),y-F(1,19))
                    reject(args,c,'label '+name)
                for name in ['AE','AD','CE']:
                    c=deepcopy(cert);c[name]=tuple(reversed(c[name]));reject(args,c,'reversed '+name)
                    c=deepcopy(cert);c[name]=tuple((x+1,y) for x,y in c[name])
                    # Translation leaves area unchanged, so sum-only validation fails here.
                    require(area(c[name])==area(cert[name]),'translation area oracle')
                    reject(args,c,'translated '+name)
                c=deepcopy(cert);c['AD']=c['CE'];reject(args,c,'duplicated square')
                reject((A,u,(2*v[0],2*v[1]),t),cert,'incorrect height')
                reject((A,u,v,1-t if t!=F(1,2) else F(1,3)),cert,'different cut')
                c=deepcopy(cert);c['points']['C'],c['points']['D']=c['points']['D'],c['points']['C'];reject(args,c,'swap C D')
                c=deepcopy(cert);del c['points']['F'];reject(args,c,'missing F')
                c=deepcopy(cert);c['points']['G']=(0,0);reject(args,c,'extra G')

args=((0,0),(6,0),(0,4),F(1,3));cert=construct(*args)
for bad in [None,False,2,'points',[],(),set(),{'points':{}},dict(cert,extra=0)]:reject(args,bad,'certificate container')
for bad in [None,'ABCDEF',list('ABCDEF'),tuple('ABCDEF'),set('ABCDEF'),1]:
    c=deepcopy(cert);c['points']=bad;reject(args,c,'point-map container')
for name in ['AE','AD','CE']:
    for bad in [None,4,'ABCD',{},[],cert[name][:3],cert[name]+cert[name][:1]]:
        c=deepcopy(cert);c[name]=bad;reject(args,c,'region container')
for name in 'ABCDEF':
    for bad in [None,0,'00',(0,), (0,0,0),(False,0),(0.0,0),(complex(0),0)]:
        c=deepcopy(cert);c['points'][name]=bad;reject(args,c,'coordinate type')
for i in range(4):
    for bad in [None,True,'x',.5,complex(1)]:
        wrong=list(args);wrong[i]=bad;reject(wrong,cert,'input type')
for t in [F(-1),F(0),F(1),F(2)]:reject((args[0],args[1],args[2],t),cert,'noninternal cut')
for v in [(0,6),(0,2),(3,4),(0,0)]:reject((args[0],args[1],v,args[3]),cert,'wrong geometric height')
reject((args[0],(0,0),args[2],args[3]),cert,'zero baseline')
print(json.dumps({'paper':'euclid-elements-ii3','optimization':sys.flags.optimize,**counts,'result':'PASS','scope':'finite rational instances; not a general proof'},sort_keys=True))
