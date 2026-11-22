"""Euclid VI.22 teaching model of exact base and area proportions."""
from fractions import Fraction as Q


def square(b):
    return ((0,0),(b,0),(b,b),(0,b))


def isosceles(b):
    return ((0,0),(b,0),(0,b))


def right_345(b):
    return ((0,0),(b,0),(0,Q(4,3)*b))


def area(vertices):
    determinants=(x*v-y*u for (x,y),(u,v) in zip(vertices,vertices[1:]+vertices[:1]))
    return Q(abs(sum(determinants)),2)


def side2(vertices,i):
    x,y=vertices[i]
    u,v=vertices[(i+1)%len(vertices)]
    return (u-x)**2+(v-y)**2


def third(a,b):
    if min(a,b)<=0:
        raise ValueError("positive lengths required")
    return Q(b*b,a)


def fourth(a,b,c):
    if min(a,b,c)<=0:
        raise ValueError("positive lengths required")
    return Q(b*c,a)


def compare(a,b,c,d):
    if min(a,b,c,d)<=0:
        raise ValueError("positive lengths or areas required")
    return a*d==b*c


def placed(vertices,rotation,shift,reflection=False):
    u,v=rotation
    if u*u+v*v!=1:
        raise ValueError("unit rotation required")
    s=-1 if reflection else 1
    return tuple((shift[0]+u*x-s*v*y,shift[1]+v*x+s*u*y) for x,y in vertices)


def grid():
    for family in (square,isosceles,right_345):
        for second in (square,isosceles,right_345):
            for a,c in ((Q(2),Q(4)),(Q(7,3),Q(5,2)),(Q(1,2),Q(9,5))):
                for ratio in (Q(1,2),Q(2,3),Q(1),Q(3,2),Q(5,2)):
                    b,d=a*ratio,c*ratio
                    for reflection in (False,True):
                        shapes=(family(a),placed(family(b),(0,1),(3,-2),reflection),
                                second(c),placed(second(d),(Q(3,5),Q(4,5)),(-1,5),reflection))
                        yield a,b,c,d,shapes
