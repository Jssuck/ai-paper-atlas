"""VI.23 in rational coordinates: stepped side replacement and ratio chain."""
from fractions import Fraction as Q

SLOPE=(Q(3,5),Q(4,5))


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


def parallelogram(a,b,direction,origin=(0,0)):
    u,v=direction
    if min(a,b)<=0 or u*u+v*v!=1 or v==0:
        raise ValueError("positive sides and nonparallel unit direction required")
    x,y=origin
    return ((x,y),(x+a,y),(x+a+b*u,y+b*v),(x+b*u,y+b*v))


def area(vertices):
    return Q(abs(sum(cross(p,q) for p,q in zip(vertices,vertices[1:]+vertices[:1]))),2)


def determinant_area(vertices):
    o,p,_,q=vertices
    return abs(cross((p[0]-o[0],p[1]-o[1]),(q[0]-o[0],q[1]-o[1])))


def three_areas(a,b,c,d,direction=SLOPE):
    polys=tuple(parallelogram(m,n,direction,(3,-7)) for m,n in ((a,b),(c,b),(c,d)))
    return tuple(map(area,polys))


def ratio_chain(a,b,c,d,k):
    if min(a,b,c,d,k)<=0:
        raise ValueError("positive lengths required")
    l=Q(k*c,a)
    m=Q(l*d,b)
    return (k,l,m)


def grid():
    for a,c in ((1,2),(6,4),(Q(3,2),Q(5,3)),(3,3)):
        for b,d in ((2,5),(Q(2,7),1),(Q(5,2),Q(3,4)),(7,7)):
            for direction in (SLOPE,(0,1),(Q(-3,5),Q(4,5)),(Q(5,13),Q(-12,13))):
                for sign in (-1,1):
                    yield a,b,c,d,(direction[0],direction[1]*sign)
