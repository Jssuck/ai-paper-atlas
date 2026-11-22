"""VI.27 teaching model: maxima with a fixed shape for the defect."""
from fractions import Fraction as Q


def area(polygon):
    return Q(abs(sum(x*v-y*u for (x,y),(u,v) in
                     zip(polygon,polygon[1:]+polygon[:1]))),2)


def shape(width, height, shear, left, rotation=(1,0)):
    u,v=rotation
    if u*u+v*v!=1:
        raise ValueError("unit rotation required")
    raw=((left,0),(left+width,0),(left+width+shear,height),(left+shear,height))
    return tuple((u*x-v*y,v*x+u*y) for x,y in raw)


def construct(length, t, r, skew=Q(1,3), rotation=(1,0)):
    length,t,r,skew=map(Q,(length,t,r,skew))
    if min(length,r,t,length-t)<=0:
        raise ValueError("positive lengths and strictly internal defect required")
    h=r*t
    return (shape(length-t,h,skew*t,0,rotation),
            shape(t,h,skew*t,length-t,rotation))


def loss_pieces(length,t,r,skew=Q(1,3)):
    """Equal-area rearrangement after applying a common shear, not original diagram."""
    length,t,r,skew=map(Q,(length,t,r,skew))
    if min(length,r,t,length-t)<=0:
        raise ValueError("positive lengths and strictly internal defect required")
    half=length/2
    gap=abs(t-half)
    if not gap:
        return (0,0,0)
    narrow=half-gap
    # In coordinates with x shear skew/r times y, the regions are rectangles.
    above=shape(half,r*gap,skew*gap,0)
    beside=shape(gap,r*narrow,skew*narrow,0)
    gap_cell=shape(gap,r*gap,skew*gap,0)
    return tuple(map(area,(above,beside,gap_cell)))
