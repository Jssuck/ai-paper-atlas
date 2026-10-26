"""Normalized exact I.2 teaching family, not a universal straightedge/compass engine."""
from fractions import Fraction as F
from itertools import product
import json
from exact import Q3, rational, point, require_point, distance2, orientation


def add(p,q):
    return tuple(x+y for x,y in zip(p,q))


def scale(p,k):
    return tuple(x.scale(k) for x in p)


def delta(p,q):
    return tuple(x-y for x,y in zip(p,q))


def dot(p,q):
    return p[0]*q[0]+p[1]*q[1]


def beyond(origin,through,target):
    """target lies strictly beyond through on the origin-through ray."""
    v=delta(through,origin); w=delta(target,through)
    return origin!=through and orientation(origin,through,target).sign()==0 and dot(v,w).sign()>0


def construct(s,r,side=1,offset=(0,0)):
    """Input family: positive rational s,r; reflected equilateral frame + translation.

    C is an input endpoint with BC=r; this function analytically generates a
    witness. It is NOT an implementation that derives coordinates by primitive
    compass operations. The separate certificate checks the relevant constraints.
    """
    s,r=rational(s),rational(r)
    if s<=0 or r<=0:
        raise ValueError('s and r must be positive')
    if isinstance(side,bool) or not isinstance(side,int) or side not in (-1,1):
        raise ValueError('side must be +1 or -1')
    o=point(offset)
    d=(Q3(),Q3()); a=(Q3(s),Q3()); b=(Q3(s/2),Q3(0,side*s/2))
    c=add(b,(Q3(r),Q3()))
    g=scale(b,1+r/s); l=(Q3(s+r),Q3())
    return {key:add(p,o) for key,p in dict(A=a,B=b,C=c,D=d,G=g,L=l).items()}


def certificate(points):
    """Verify constraints without using input parameters or construction formula.

    Checks are geometric obligations, not a provenance/operation-history proof.
    Circle B through C needs no transfer of a remote radius; circle D through G
    likewise uses existing local endpoints. Historical existence is not certified.
    """
    a,b,c,d,g,l=(require_point(points[k]) for k in ('A','B','C','D','G','L'))
    ab=distance2(a,b); bc=distance2(b,c)
    checks={
        'nonzero_input':bc.sign()>0,
        'distinct_anchor':a!=b,
        'equilateral_frame':ab==distance2(d,a)==distance2(d,b) and orientation(d,a,b).sign()!=0,
        'circle_B_through_C':distance2(b,g)==bc,
        'D_B_G_order':beyond(d,b,g),
        'circle_D_through_G':distance2(d,l)==distance2(d,g),
        'D_A_L_order':beyond(d,a,l),
        'output_length':distance2(a,l)==bc,
    }
    checks['accepted']=all(checks.values())
    return checks


def coincident_anchor(a,b,c):
    """If the requested anchor A already equals B, segment AC is BC itself."""
    a,b,c=map(require_point,(a,b,c))
    if a!=b:
        raise ValueError('This direct case requires A=B')
    if b==c:
        raise ValueError('The given segment must be nonzero')
    return c


def record(points):
    return {key:[x.record() for x in p] for key,p in points.items()}


def run():
    values=[F(1,3),F(1,2),F(1),F(2),F(3)]
    offsets=[(0,0),(F(1,2),F(-2,3)),(-2,3)]
    cases=bad=0
    for s,r,side,o in product(values,values,(-1,1),offsets):
        cases+=1
        if not certificate(construct(s,r,side,o))['accepted']:bad+=1
    p=construct(2,1)
    near=dict(p); near['G']=scale(p['B'],F(1,2))
    wrong_l=dict(p); wrong_l['L']=(Q3(-3),Q3())
    return {
      'scope':'normalized rational s,r, two reflected frames, three rational translations; not all planar inputs',
      'enumeration':{'cases':cases,'violations':bad},
      'example_s2_r1':{'points':record(p),'certificate':certificate(p),
          'squared_lengths':{k:distance2(p[x],p[y]).record() for k,x,y in [('AB2','A','B'),('BC2','B','C'),('DG2','D','G'),('AL2','A','L')]}},
      'near_G_counterexample':certificate(near),
      'wrong_ray_L_counterexample':certificate(wrong_l),
      'coincident_anchor':{'A':[0,0],'B':[0,0],'C':[3,4],'returned_C':record({'L':coincident_anchor(point((0,0)),point((0,0)),point((3,4)))})}
    }

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
