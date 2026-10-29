"""Exact rational teaching model for III.6; not a classical proof checker."""
from fractions import Fraction as F
import json

def q(x):
    if isinstance(x,bool) or not isinstance(x,(int,str,F)): raise ValueError('rational input required')
    try:return F(x)
    except (ValueError,ZeroDivisionError):raise ValueError('invalid rational') from None

def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2:raise ValueError('two coordinates required')
    return tuple(q(x) for x in p)

def circle(o,r):
    o=point(o);r=q(r)
    if r<=0:raise ValueError('radius must be positive')
    return o,r

def d2(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def sp(p):return [str(x) for x in p]

def relation(o1,r1,o2,r2):
    o1,r1=circle(o1,r1);o2,r2=circle(o2,r2)
    d=d2(o1,o2)
    if d==0:return 'coincident' if r1==r2 else 'concentric_disjoint'
    if d==(r1+r2)**2:return 'external_tangent'
    if d==(r1-r2)**2:return 'internal_tangent'
    if d>(r1+r2)**2:return 'external_disjoint'
    if d<(r1-r2)**2:return 'strict_containment'
    return 'two_intersections'

def certificate(o1,r1,o2,r2):
    """Accepts only tangent pairs with rational centers and positive rational radii."""
    o1,r1=circle(o1,r1);o2,r2=circle(o2,r2)
    kind=relation(o1,r1,o2,r2)
    if kind not in ('external_tangent','internal_tangent'):raise ValueError('pair is not tangent')
    factor=r1/(r1+r2 if kind=='external_tangent' else r1-r2)
    t=tuple(a+factor*(b-a) for a,b in zip(o1,o2))
    # Square-distance subtraction yields the radical line. At tangency,
    # its distance from O1 is r1, so its only circle point is its foot T.
    n=tuple(b-a for a,b in zip(o1,o2))
    k=(sum(x*x for x in o2)-sum(x*x for x in o1)+r1*r1-r2*r2)/2
    return {'schema':'euclid-iii6-rational-v1','center1':sp(o1),'radius1':str(r1),
        'center2':sp(o2),'radius2':str(r2),'classification':kind,
        'center_distance_squared':str(d2(o1,o2)),'same_center':False,
        'contact':sp(t),'contact_distance1_squared':str(d2(o1,t)),
        'contact_distance2_squared':str(d2(o2,t)),
        'radical_normal':sp(n),'radical_offset':str(k),
        'unique_contact':True}

def verify(c):
    try:
        if type(c) is not dict:return False
        expected=certificate(c['center1'],c['radius1'],c['center2'],c['radius2'])
        return json.dumps(c,sort_keys=True,allow_nan=False)==json.dumps(expected,sort_keys=True,allow_nan=False)
    except (ValueError,TypeError,KeyError,OverflowError):return False

EXAMPLES={
 'external':((0,0),2,(5,0),3),
 'internal':((0,0),5,(3,0),2),
 'internal_swapped':((3,0),2,(0,0),5),
 'oblique_external':((1,-2),2,('14/5','2/5'),1),
 'oblique_internal':((1,-2),5,('14/5','2/5'),2)}

def grid():
    for tx in range(-2,3):
      for ty in range(-1,2):
       for scale in (F(1,2),F(1),F(2),F(3)):
        for mirror in (1,-1):
         for a in EXAMPLES.values():
          o,r,p,s=a
          transform=lambda v:(tx+scale*q(v[0]),ty+mirror*scale*q(v[1]))
          yield transform(o),scale*r,transform(p),scale*s
