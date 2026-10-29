"""Independent finite audit. No author generators; not a proof of III.11."""
from fractions import Fraction as F
from itertools import product
import json
import sys
from geometry import Circle, relation, closed_disk_inside, verify_contact, contact_candidate

counts = {'radical_axis_pairs': 0, 'boundary_candidates': 0,
          'external_certificates': 0, 'point_mutations_rejected': 0,
          'radius_order_rejections': 0, 'invalid_inputs_rejected': 0,
          'tiny_gap_certificates': 0}

def require(value, message):
    if not value:
        raise RuntimeError(message)

def reject(fn, *args):
    try:
        fn(*args)
    except (ValueError, TypeError):
        return
    raise RuntimeError('expected rejection missing')

def sqdist(p,q):
    return (p[0]-q[0])**2+(p[1]-q[1])**2

def axis_oracle(R,r,x,y):
    """Eliminate circle equations: transverse height numerator K.
    K>0 gives two intersections; K=0 one; K<0 none.
    For no intersection, sign of q-(R²+r²) separates external/nested.
    This is a separately written radical-axis oracle, not imported helpers.
    """
    q=x*x+y*y
    if q==0:
        return 'coincident' if R==r else 'concentric_disjoint'
    k=4*q*R*R-(q+R*R-r*r)**2
    if k>0: return 'secant'
    if k==0:
        return 'external_tangent' if q>R*R+r*r else 'internal_tangent'
    return 'separate' if q>R*R+r*r else 'strictly_nested'

for R,r,x,y in product(range(1,7), range(1,7), range(-6,7), range(-6,7)):
    a=Circle((0,0),R); b=Circle((x,y),r)
    expect=axis_oracle(R,r,x,y)
    require(relation(a,b)==expect and relation(b,a)==expect,'radical-axis classification')
    counts['radical_axis_pairs']+=1
    # Direct integer boundary candidates are not generated using the asserted contact formula.
    for tx,ty in product(range(-R,R+1),repeat=2):
        if tx*tx+ty*ty != R*R: continue
        common=(tx-x)**2+(ty-y)**2==r*r
        # Independent input contract, not a conclusion test.
        inside=R>=r and x*x+y*y <= (R-r)*(R-r)
        eligible=R>r and common and inside
        t=(tx,ty)
        if eligible:
            out=verify_contact(a,b,t)
            require(out['cross']==0 and out['forward_dot']>0 and out['beyond_inner_center'],'report fields')
            require(contact_candidate(a,b)==t,'generated candidate compared with independently supplied point')
        else:
            reject(verify_contact,a,b,t)
        counts['boundary_candidates']+=1

# Rational directions from the unit-circle parametrization; quarter-turn and reflection
# are included by negative parameters and the separately supplied (-1,0) direction.
directions=[((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in [F(i,7) for i in range(-17,18)]]+[(-F(1),F(0))]
for u,r,gap,o in product(directions,[F(2,9),F(7,5),F(13,4)],[F(1,11),F(9,7),F(17,3)],[(F(-4,3),F(2,5)),(F(8),F(-9))]):
    R=r+gap
    c=(o[0]+gap*u[0],o[1]+gap*u[1]); t=(o[0]+R*u[0],o[1]+R*u[1])
    a,b=Circle(o,R),Circle(c,r)
    require(sqdist(o,t)==R*R and sqdist(c,t)==r*r,'external certificate construction')
    out=verify_contact(a,b,t)
    require(out['radius_gap2']==gap*gap and out['center_distance2']==gap*gap,'metric conclusion')
    require(contact_candidate(a,b)==t and closed_disk_inside(a,b),'API agreement')
    counts['external_certificates']+=1
    reject(verify_contact,b,a,t); reject(contact_candidate,b,a)
    counts['radius_order_rejections']+=2
    for dx,dy in [(F(1,101),0),(-F(1,101),0),(0,F(1,103)),(0,-F(1,103)),(F(2,107),F(3,109))]:
        reject(verify_contact,a,b,(t[0]+dx,t[1]+dy))
        counts['point_mutations_rejected']+=1

for k in [1,9,40,100]:
    gap=F(1,10**k); a=Circle((0,0),1+gap);b=Circle((gap,0),1)
    verify_contact(a,b,(1+gap,0)); counts['tiny_gap_certificates']+=1
    require(relation(a,Circle((gap+F(1,10**(k+5)),0),1))=='secant','exact outer perturbation')
    require(relation(a,Circle((gap-F(1,10**(k+5)),0),1))=='strictly_nested','exact inner perturbation')

for p,r in [((0,0),0),((0,0),-1),((0,0),True),((0,0),1.0),((0,),1),((0,0,0),1),((True,0),1),((0.0,0),1),(('0',0),1),(None,1)]:
    reject(Circle,p,r);counts['invalid_inputs_rejected']+=1
print(json.dumps({'python_optimization':sys.flags.optimize,'checks':counts,'result':'PASS','scope':'finite independent audit; not a general proof'},sort_keys=True,indent=2))
