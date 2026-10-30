"""Independent III.18 regression oracle: solve line/normal equations by determinants.
Finite exact checks, not a proof over all real inputs. Python standard library only.
"""
from fractions import Fraction as Q
from itertools import product
from copy import deepcopy
import json
import geometry as g

def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def norm(a):return a[0]*a[0]+a[1]*a[1]
def solve(o,b,v):
    # H lies on line normal n through b and line direction v through o.
    n=(-v[1],v[0]); c1=n[0]*b[0]+n[1]*b[1];c2=v[0]*o[0]+v[1]*o[1]
    d=det(n,v)
    return ((c1*v[1]-n[1]*c2)/d,(n[0]*c2-c1*v[0])/d)
def run():
    count=powers=reverse=scales=mutations=second=tan=interior=0
    dirs=[(Q(i),Q(j)) for i,j in product(range(-2,3),repeat=2) if (i,j)!=(0,0)]
    units=[(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(5,13),Q(12,13)),(Q(7,25),Q(-24,25))]
    for o,r,u,v in product([(Q(0),Q(0)),(Q(3,7),Q(-4,9))],[Q(1),Q(7,3),Q(13,2)],units,dirs):
        b=(o[0]+r*u[0],o[1]+r*u[1]); h=solve(o,b,v)
        p=norm((h[0]-o[0],h[1]-o[1]))-r*r
        c=g.certify(o,b,r,v);require(g.verify(c),'legitimate certificate')
        require(c['h']==h and c['power']==p,'determinant oracle')
        require(p<=0,'boundary line must approach disk')
        expected='tangent' if h==b else 'interior_witness'
        require(c['kind']==expected,'classification by foot')
        if p==0:tan+=1
        else:interior+=1
        count+=1
        for t in [Q(-7,3),Q(-1,11),Q(0),Q(2,5),Q(9,2)]:
            x=(b[0]+t*v[0],b[1]+t*v[1]);direct=norm((x[0]-o[0],x[1]-o[1]))-r*r
            require(g.line_power(c,t)==direct,'direct power')
            require(direct==p+norm((x[0]-h[0],x[1]-h[1])),'orthogonal decomposition')
            powers+=1
        cr=g.certify(o,b,r,(-v[0],-v[1]));require(cr['h']==h and cr['power']==p and g.verify(cr),'reverse');reverse+=1
        for k in [Q(7,3),Q(-2,5)]:
            cs=g.certify(o,b,r,(k*v[0],k*v[1]));require(cs['h']==h and cs['power']==p and g.verify(cs),'scale');scales+=1
        if p<0:
            # Reflection of boundary point across the foot yields other boundary point.
            z=(2*h[0]-b[0],2*h[1]-b[1]);require(z!=b and norm((z[0]-o[0],z[1]-o[1]))==r*r,'second boundary');second+=1
        bad=[]
        for key in ['q','s','t','power']:
            z=deepcopy(c);z[key]+=Q(1,17);bad.append(z)
        z=deepcopy(c);z['h']=(h[0]+Q(1,19),h[1]);bad.append(z)
        z=deepcopy(c);z['kind']='interior_witness' if expected=='tangent' else 'tangent';bad.append(z)
        z=deepcopy(c);z['q']=False;bad.append(z)
        z=deepcopy(c);del z['power'];bad.append(z)
        z=deepcopy(c);z['unexpected']=0;bad.append(z)
        for z in bad:require(not g.verify(z),'tamper rejected');mutations+=1
    baseline=((0,0),(3,4),5,(1,2));invalid=[]
    for index,values in [(0,[(0,),None,(False,0),(0.0,0)]),(1,[(3,3),(0,0),(3,4,0)]),(2,[0,-5,True,5.0,'5']),(3,[(0,0),(1,),None,(True,2),(1,2.0)])]:
        for value in values:
            a=list(baseline);a[index]=value;invalid.append(a)
    for a in invalid:
        try:g.certify(*a)
        except ValueError:pass
        else:raise RuntimeError('invalid input accepted')
    print(json.dumps(dict(configurations=count,tangent=tan,interior=interior,power_decompositions=powers,reversal=reverse,scaling=scales,second_boundary=second,tamper_rejected=mutations,invalid_rejected=len(invalid)),sort_keys=True))
if __name__=='__main__':run()
