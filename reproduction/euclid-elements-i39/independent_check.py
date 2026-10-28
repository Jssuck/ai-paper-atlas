"""Independent I.39 reviewer: basis-vector oracle, no author case generator.
Finite regression evidence only. Run python [-O|-OO] independent_check.py.
"""
from fractions import Fraction as F
from copy import deepcopy
import json, sys
from geometry import make_certificate, construction_trace, verify_certificate

counts = {'checks':0,'positive_cases':0,'branch_cases':0,'invalid_geometry':0,'invalid_schema':0,'certificate_attacks':0,'binding_attacks':0}
def check(ok, label):
    counts['checks'] += 1
    if not ok: raise RuntimeError(label)
def reject(data, label):
    try: make_certificate(data)
    except ValueError: check(True,label)
    else: check(False,label)
def add(p,q): return tuple(x+y for x,y in zip(p,q))
def mul(t,p): return tuple(t*x for x in p)
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def enc(p): return [str(x) for x in p]
def fixture(u,v,h,j,k,shift):
    # BC=u, BA=h*u+k*v, BD=j*u+k*v.
    return {'B':enc(shift),'C':enc(add(shift,u)),
            'A':enc(add(shift,add(mul(h,u),mul(k,v)))),
            'D':enc(add(shift,add(mul(j,u),mul(k,v))))}
bases=[((2,1),(-1,3)),((0,3),(2,-1)),((-3,2),(1,2)),((F(2,3),F(1,7)),(F(3,5),-2)),((1,-2),(2,1)),((-2,-3),(-4,1))]
sample=None
for u,v in bases:
    u=tuple(map(F,u));v=tuple(map(F,v))
    for k in map(F,['1','-1','2/3','-5/7']):
      for h,j in [(0,1),(2,-3),(-2,4)]:
       for shift in [(F(0),F(0)),(F(5,2),F(-3,7)),(F(-6),F(4))]:
        data=fixture(u,v,F(h),F(j),k,shift);c=make_certificate(data);tr=c['trace'];sample=data
        counts['positive_cases']+=1
        expected_signed=k*det(u,v);expected_area=abs(expected_signed)/2
        check(verify_certificate(data,c),'positive verification')
        check(tr['signed_double_area']=={'ABC':str(expected_signed),'DBC':str(expected_signed)},'independent oriented area')
        check(tr['area']=={'ABC':str(expected_area),'DBC':str(expected_area),'EBC':str(expected_area),'EDC':'0'},'independent unsigned areas')
        check(tr['E']==data['D'] and tr['t']=='1' and tr['branch']=='equal','equal intersection')
        check(tr['cross']=={'BC_AE':'0','BC_AD':'0'},'parallel direction')
        altered=deepcopy(data);altered['D']=enc(add(tuple(map(F,data['D'])),u))
        check(not verify_certificate(altered,c),'full input binding D slide');counts['binding_attacks']+=1
        for factor in [F(2),F(1,3)]:
            other=deepcopy(data);other['D']=enc(add(shift,add(mul(F(j),u),mul(factor*k,v))))
            t=construction_trace(other);counts['branch_cases']+=1
            check(t['t']==str(1/factor),'independent intersection ratio')
            e=add(shift,add(mul(F(j)/factor,u),mul(k,v)))
            check(t['E']==enc(e),'independent intersection point')
            expected_branch='inner' if factor>1 else 'outer'
            check(t['branch']==expected_branch,'independent branch')
            ar={key:F(value) for key,value in t['area'].items()}
            check(ar['ABC']==expected_area and ar['EBC']==expected_area and ar['DBC']==factor*expected_area,'branch areas')
            check(ar['EDC']==abs(factor-1)*expected_area and ar[t['whole']]==ar[t['part']]+ar['EDC'] and ar['EDC']>0,'strict proper part')
            reject(other,'unequal geometry must fail maker');counts['invalid_geometry']+=1
# Direct invalid geometry, not merely empty certificate rejection.
base={'A':['1','2'],'B':['0','0'],'C':['4','0'],'D':['3','2']}
invalid=[dict(base,C=base['B']),dict(base,A=['1','0']),dict(base,D=['3','0']),dict(base,D=['3','-2']),dict(base,D=base['A']),dict(base,D=['3','4']),dict(base,D=['3','1'])]
for data in invalid:
    reject(data,'direct invalid geometry');counts['invalid_geometry']+=1
# Auxiliary E=A is allowed in the non-equal construction trace.
edge=dict(base,D=['2','4']);tr=construction_trace(edge)
check(tr['E']==edge['A'] and tr['branch']=='inner','A=E valid construction');reject(edge,'A=E unequal theorem rejected')
class IntSubclass(int): pass
class DictSubclass(dict): pass
class ListSubclass(list): pass
bads=[None,[],{},dict(base,X=[0,0]),DictSubclass(base),dict(base,A=(1,2)),dict(base,A=ListSubclass([1,2])),dict(base,A=[1]),dict(base,A=[1,2,3])]
for value in [True,False,0.0,float('nan'),float('inf'),None,F(1,2),IntSubclass(1),'01','+1','-0','2/4','1.0',' 1','1/0','nan']:
    bads.append(dict(base,A=[value,2]))
for data in bads:
    reject(data,'invalid schema/type');counts['invalid_schema']+=1
c=make_certificate(base)
def nodes(x,path=()):
    yield path
    if type(x) is dict:
        for key,value in x.items(): yield from nodes(value,path+(key,))
    elif type(x) is list:
        for key,value in enumerate(x): yield from nodes(value,path+(key,))
for path in nodes(c):
    for replacement in [None,True,False,0,1,0.0,float('nan'),float('inf'),{},[],'tampered']:
        if not path: bad=replacement
        else:
            bad=deepcopy(c);target=bad
            for key in path[:-1]:target=target[key]
            target[path[-1]]=replacement
        check(not verify_certificate(base,bad),'subtree/type tamper');counts['certificate_attacks']+=1
# No unrecorded fields, deleted fields, or cycles accepted.
for key in c:
    bad=deepcopy(c);del bad[key];check(not verify_certificate(base,bad),'missing key');counts['certificate_attacks']+=1
bad=deepcopy(c);bad['extra']='field';check(not verify_certificate(base,bad),'extra key');counts['certificate_attacks']+=1
bad=deepcopy(c);bad['loop']=bad;check(not verify_certificate(base,bad),'cyclic object');counts['certificate_attacks']+=1
check(verify_certificate({k:list(map(int,v)) for k,v in base.items()},c),'documented integer normalization')
check(verify_certificate(base,json.loads(json.dumps(c))),'JSON roundtrip')
print(json.dumps({'status':'PASS','optimize':sys.flags.optimize,**counts},sort_keys=True))
