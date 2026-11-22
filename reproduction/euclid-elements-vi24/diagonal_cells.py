"""Exact coordinate reconstruction of the four cells in Euclid VI.24."""
from fractions import Fraction as Q

U,V=(6,0),(2,4)


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


def sub(a,b):
    return a[0]-b[0],a[1]-b[1]


def point(u,v,x,y):
    return x*u[0]+y*v[0],x*u[1]+y*v[1]


def polygon(u,v,l,r,b,t):
    return tuple(point(u,v,x,y) for x,y in ((l,b),(r,b),(r,t),(l,t)))


def partition(u,v,x,y=None):
    """Return full cell then four cells LL, UR, LR, UL; all vertices CCW in uv."""
    x=Q(x)
    y=x if y is None else Q(y)
    if cross(u,v)==0 or not (0<x<1 and 0<y<1):
        raise ValueError("independent directions and proper interior cut required")
    bounds=((0,1,0,1),(0,x,0,y),(x,1,y,1),(x,1,0,y),(0,x,y,1))
    return tuple(polygon(u,v,*b) for b in bounds)


def area(vertices):
    return Q(abs(sum(cross(a,b) for a,b in zip(vertices,vertices[1:]+vertices[:1]))),2)


def axis_square_ratios(cell,whole):
    return tuple(Q(sum(x*x for x in sub(cell[i],cell[0])),
                   sum(x*x for x in sub(whole[i],whole[0]))) for i in (1,3))


def scale_match(cell,whole):
    a,b=axis_square_ratios(cell,whole)
    return a==b


def det_area(cell):
    return abs(cross(sub(cell[1],cell[0]),sub(cell[3],cell[0])))
