"""Independent exact audit for I.41; finite checks, not a proof kernel.
Uses separate coordinate generation and shoelace arithmetic, not cases.py.
"""
from fractions import Fraction as F
import copy
import json
import sys
from geometry import make_certificate, verify_certificate

counts = {}
def check(condition, kind):
    counts[kind] = counts.get(kind, 0) + 1
    if not condition:
        raise RuntimeError('independent check failed: ' + kind)
def plus(p,q): return tuple(p[i]+q[i] for i in range(2))
def mul(t,p): return tuple(t*x for x in p)
def minus(p,q): return plus(p,mul(-1,q))
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def twice(poly):
    return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1] - poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))
def encode(p): return {k:[str(F(x)) for x in v] for k,v in p.items()}
def reject(p, kind):
    try:
        make_certificate(p)
    except ValueError:
        check(True,kind)
    else:
        check(False,kind)

def run():
    samples=[]
    for b in [(F(0),F(0)),(F(2,7),F(-5,3)),(F(-9,2),F(8,5))]:
      for u in [(F(0),F(3)),(F(2),F(1)),(F(-3),F(2)),(F(5),F(-2)),(F(1,3),F(2,5))]:
       for v in [(F(1),F(4)),(F(-2),F(1)),(F(3,7),F(-5,2)),(F(-1),F(-2))]:
        if cross(u,v)==0: continue
        for t in map(F,[-3,-1,0,'1/3',1,2,'7/2']):
            a=plus(b,v);c=plus(b,u);d=plus(a,u);e=plus(a,mul(t,u))
            p=dict(A=a,B=b,C=c,D=d,E=e);raw=encode(p)
            cert=make_certificate(raw); samples.append(raw)
            check(verify_certificate(raw,cert),'valid_certificate')
            check(cert['points']==raw,'canonical_binding')
            check(cert['upper_parameter']==str(t),'parameter')
            pos='E=A' if t==0 else 'E=D' if t==1 else 'inside AD' if 0<t<1 else 'outside AD'
            check(cert['upper_position']==pos,'position')
            for label,poly in [('ABC',[a,b,c]),('ACD',[a,c,d]),('EBC',[e,b,c]),('ABCD',[a,b,c,d])]:
                check(F(cert['double_areas'][label])==twice(poly),'independent_shoelace')
            check(twice([a,b,c,d])==2*twice([e,b,c]),'ratio')
            other=copy.deepcopy(raw);other['E']=[str(x) for x in plus(e,u)]
            check(not verify_certificate(other,cert),'equal_area_rebinding')
            for label,new in [('opposite_side',plus(minus(b,v),mul(t,u))),('off_line',plus(e,v))]:
                bad=copy.deepcopy(raw);bad['E']=[str(x) for x in new];reject(bad,label)
            bad=copy.deepcopy(raw);bad['D']=[str(x) for x in plus(d,v)];reject(bad,'wrong_fourth')
    base={'A':[1,3],'B':[0,0],'C':[4,0],'D':[5,3],'E':[9,3]}
    cert=make_certificate(base)
    check(twice([(1,3),(0,0),(4,0),(5,3)])==24,'article_numbers')
    for e,area2 in [((1,3),12),((3,3),12),((5,3),12),((9,3),12),((-7,3),12),((9,6),24),((9,-3),12)]:
        check(twice([e,(0,0),(4,0)])==area2,'article_numbers')
    check(twice([(0,3),(0,0),(4,0),(2,3)])==18,'article_numbers')
    check(twice([(9,3),(0,0),(2,0)])==6,'article_numbers')
    for b,d in [(4,2),(F(7,3),F(1,2)),(6,5)]:
      for h in [1,F(3,2),4]:
       for shear in [-2,0,F(1,3),3]:
        a=(shear*h,h);D=(d+shear*h,h);B=(0,0);C=(b,0)
        m=mul(F(1,2),plus(D,C));f=(b+d+shear*h,h)
        q=twice([a,B,C,D]);tri=twice([a,B,m])
        check(q==2*tri,'trapezoid_extension')
        check(twice([B,m,C])==twice([f,m,D]),'trapezoid_extension')
        check(minus(m,B)==minus(f,m),'trapezoid_extension')
        check(q==twice([a,B,f]),'trapezoid_extension')
        check(2*d*h < q < 2*b*h,'trapezoid_extension')
    bad_coords=[True,False,1.0,float('nan'),float('inf'),None,[],{},'1/0','NaN','inf','01','+1','1.0','2/4',' 1','1 ', '1_0']
    for value in bad_coords:
        p=copy.deepcopy(base);p['A'][0]=value;reject(p,'coordinate_type')
    for value in [(),(1,3),[],[1],[1,3,4],None,'1,3',{},False]:
        p=copy.deepcopy(base);p['A']=value;reject(p,'point_type')
    for value in [{},[],None,'',False]: reject(value,'top_schema')
    for name in base:
        p=copy.deepcopy(base);del p[name];reject(p,'top_schema')
    p=copy.deepcopy(base);p['F']=[0,0];reject(p,'top_schema')
    for key,value in [('C',[0,0]),('A',[1,0]),('E',[3,0])]:
        p=copy.deepcopy(base);p[key]=value;reject(p,'degenerate')
    def paths(obj,path=()):
        yield path
        if isinstance(obj,dict):
            for k,v in obj.items(): yield from paths(v,path+(k,))
        elif isinstance(obj,list):
            for k,v in enumerate(obj): yield from paths(v,path+(k,))
    replacements=[None,True,False,0,1,1.0,[],{},'tampered']
    for path in paths(cert):
      for value in replacements:
        changed=copy.deepcopy(cert)
        if not path: changed=value
        else:
            obj=changed
            for k in path[:-1]: obj=obj[k]
            obj[path[-1]]=value
        check(not verify_certificate(base,changed),'certificate_subtree')
    for path in paths(cert):
        obj=cert
        for k in path:obj=obj[k]
        if isinstance(obj,dict):
            for key in list(obj):
                changed=copy.deepcopy(cert);target=changed
                for k in path:target=target[k]
                del target[key]
                check(not verify_certificate(base,changed),'certificate_missing_key')
            changed=copy.deepcopy(cert);target=changed
            for k in path:target=target[k]
            target['extra']='x'
            check(not verify_certificate(base,changed),'certificate_extra_key')
    cycle=copy.deepcopy(cert);cycle['cycle']=cycle
    check(not verify_certificate(base,cycle),'certificate_cycle')
    shared=copy.deepcopy(cert);shared['points']['B']=shared['points']['A']
    check(not verify_certificate(base,shared),'certificate_alias_tamper')
    normal={k:[str(F(x)) for x in v] for k,v in base.items()}
    check(make_certificate(base)==make_certificate(normal),'normalization')
    print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'valid_geometries':len(samples),'trapezoid_geometries':36,'checks':sum(counts.values()),'categories':counts,'scope':'Independent finite audit, not a general theorem proof.'},indent=2))

if __name__=='__main__':run()
