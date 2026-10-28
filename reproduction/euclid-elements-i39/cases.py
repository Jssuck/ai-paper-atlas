"""Finite teaching cases; an affine map preserves the incidence/area comparisons."""
from fractions import Fraction as Q
from geometry import encode


def build(a=1,d=3,h=2,k=None,matrix=(1,0,0,1),shift=(0,0)):
    h=Q(h);k=h if k is None else Q(k)
    p={'A':(Q(a),h),'B':(Q(0),Q(0)),'C':(Q(4),Q(0)),'D':(Q(d),k)}
    r,s,t,u=map(Q,matrix);x,y=map(Q,shift)
    return encode({key:(r*v[0]+s*v[1]+x,t*v[0]+u*v[1]+y) for key,v in p.items()})

EXAMPLE=build()
MATRICES=[(1,0,0,1),(0,-1,1,0),(2,1,1,1),(-1,2,0,1),(1,0,0,-1)]

def positives():
    for m in MATRICES:
        for h in [1,2,'1/3',-2]:
            for a,d in [(-4,0),(0,1),(5,-2)]:
                for shift in [(0,0),(3,-2),('1/2','-1/3')]:
                    yield build(a=a,d=d,h=h,matrix=m,shift=shift)

def negatives():
    return [('zero base',dict(EXAMPLE,C=EXAMPLE['B'])),
            ('degenerate A',build(h=0,k=2)),('degenerate D',build(k=0)),
            ('opposite side',build(k=-2)),('coincident apex',build(a=3)),
            ('unequal inner',build(k=4)),('unequal outer',build(k=1))]
