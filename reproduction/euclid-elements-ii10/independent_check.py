"""Independent rational oracle. Does not call production construct()."""
from fractions import Fraction as F
from itertools import product
import copy, json, sys
from geometry import verify, side_diagonal
COUNTS={}
def check(ok,kind):
    if not ok: raise RuntimeError('independent check failed: '+kind)
    COUNTS[kind]=COUNTS.get(kind,0)+1
def external(h,t,o,u,v):
    xy={'A':(0,0),'C':(h,0),'B':(2*h,0),'D':(2*h+t,0),'E':(h,h),'F':(2*h+t,h),'G':(2*h+t,-t)}
    return {'points':{n:tuple(o[i]+x*u[i]+y*v[i] for i in range(2)) for n,(x,y) in xy.items()}}
def delta(a,b):return (a[0]-b[0],a[1]-b[1])
def dp(a,b):return a[0]*b[0]+a[1]*b[1]
def reject(c,args):
    try: verify(c,*args)
    except ValueError:COUNTS['rejections']=COUNTS.get('rejections',0)+1
    else:raise RuntimeError('invalid certificate/parameter accepted')
bases=[((1,0),(0,1)),((0,1),(-1,0)),((1,0),(0,-1)),((2,0),(0,2)),((F(3,5),F(4,5)),(F(-4,5),F(3,5))),((F(2,3),F(1,3)),(F(1,3),F(-2,3)))]
for h,t,(u,v) in product([F(1,9),F(1,2),F(1),F(3),F(17,3)],[F(1,10000),F(1,7),F(1,2),F(1),F(2),F(5),F(31),F(10000)],bases):
    o=(F(5,7),F(-11,13));args=(h,t,o,u,v);c=external(*args);p=c['points'];r=verify(c,*args)
    k=dp(u,u)
    expected={'AC':h*h*k,'CE':h*h*k,'AE':2*h*h*k,'EF':(h+t)**2*k,'FG':(h+t)**2*k,'CD':(h+t)**2*k,'EG':2*(h+t)**2*k,'AG':((2*h+t)**2+t*t)*k,'AD':(2*h+t)**2*k,'DG':t*t*k,'DB':t*t*k}
    squares={n:dp(delta(p[n[0]],p[n[1]]),delta(p[n[0]],p[n[1]])) for n in expected}
    for n,x in expected.items():check(squares[n]==x,'squared_lengths')
    for a,b,d in [('A','C','E'),('E','C','B'),('E','F','G'),('B','D','G'),('A','E','G'),('A','D','G')]:check(dp(delta(p[a],p[b]),delta(p[d],p[b]))==0,'right_angles')
    for a,b in [('AC','CE'),('CE','CB'),('EF','FG'),('DG','DB'),('EF','CD')]:
        def length(n):return dp(delta(p[n[0]],p[n[1]]),delta(p[n[0]],p[n[1]]))
        check(length(a)==length(b),'equal_length_bridges')
    for x,y,z in [('AE','AC','CE'),('EG','EF','FG'),('AG','AE','EG'),('AG','AD','DG')]:check(squares[x]==squares[y]+squares[z],'pythagorean_routes')
    check(r['lhs']==r['rhs']==squares['AG']==2*(squares['AC']+squares['CD']),'target')
    lam=1+t/h
    check(lam>1 and all(p['G'][i]==p['E'][i]+lam*(p['B'][i]-p['E'][i]) for i in range(2)),'EB_extension')
    check(all(p['G'][i]==p['F'][i]+(1+t/h)*(p['D'][i]-p['F'][i]) for i in range(2)),'FD_extension')
    check(dp(delta(p['C'],p['A']),u)>0 and dp(delta(p['B'],p['C']),u)>0 and dp(delta(p['D'],p['B']),u)>0,'point_order')
    COUNTS['configurations']=COUNTS.get('configurations',0)+1
    for n in p:
        for i in range(2):
            bad=copy.deepcopy(c);pt=list(bad['points'][n]);pt[i]+=F(1,19);bad['points'][n]=pt;reject(bad,args)
args=(F(3),F(2),(0,0),(1,0),(0,1));c=external(*args)
for n in c['points']:
    bad=copy.deepcopy(c);del bad['points'][n];reject(bad,args)
for bad in [None,[],{}, {'points':[]},{'points':c['points'],'extra':0},{'points':dict(c['points'],H=(0,0))}]:reject(bad,args)
for val in [True,1.0,'1',None,(),(1,), (1,2,3),(False,0),(0.0,1)]:
    bad=copy.deepcopy(c);bad['points']['G']=val;reject(bad,args)
for i in [0,1]:
    for val in [0,-1,True,1.0,'1',None,[],{}]:
        a=list(args);a[i]=val;reject(c,a)
for i in [2,3,4]:
    for val in [None,(),(1,),(1,2,3),(True,0),(1.0,0)]:
        a=list(args);a[i]=val;reject(c,a)
for u,v in [((0,0),(0,0)),((1,0),(1,0)),((2,0),(0,3)),((1,1),(1,0))]:reject(c,(3,2,(0,0),u,v))
s=d=1
rows=side_diagonal(64)
for row in rows:
    sn,dn=s+d,2*s+d
    check(row=={'s':s,'d':d,'difference':d*d-2*s*s,'next_s':sn,'next_d':dn,'next_difference':dn*dn-2*sn*sn},'recurrence_rows')
    check(dn*dn-2*sn*sn==-(d*d-2*s*s) and abs(d*d-2*s*s)==1,'recurrence_invariant')
    verify(external(s,d,(0,0),(1,0),(0,1)),s,d)
    s,d=sn,dn
check([(r['s'],r['d']) for r in rows[:8]]==[(1,1),(2,3),(5,7),(12,17),(29,41),(70,99),(169,239),(408,577)],'first_eight')
print(json.dumps({'status':'passed','optimization':sys.flags.optimize,'counts':COUNTS,'scope':'finite rational certificates; not a general theorem proof'},sort_keys=True,indent=2))
