"""Finite translated/sheared/reflected rational input family."""
from fractions import Fraction as Q
from geometry import encode


def build(s=3, a=0, d=2, direction=1, u=(2,0), v=(0,3), origin=(0,0)):
    s,a,d = map(Q,(s,a,d))
    u,v,o = [tuple(map(Q,p)) for p in (u,v,origin)]
    def point(t,upper=False):
        return tuple(o[i]+t*u[i]+(v[i] if upper else 0) for i in range(2))
    return encode(dict(A=point(a,True), B=point(0), C=point(1),
                       D=point(d,True), E=point(s), F=point(s+direction)))


EXAMPLE=build()


def positives():
    frames=[((2,0),(0,3),(0,0)), ((0,2),(3,0),(4,-2)),
            ((2,1),(-1,3),(-2,5)), ((-2,1),(1,2),(0,0)),
            ((Q(1,2),Q(2,3)),(Q(-1,3),Q(3,2)),(Q(1,7),Q(-2,5)))]
    for u,v,o in frames:
        for s in [-2,Q(-1,2),0,Q(1,2),1,3]:
            for a,d in [(0,0),(0,2),(2,0),(-3,4),(Q(1,3),Q(-2,3)),(0,-2)]:
                for sign in [-1,1]:
                    yield build(s,a,d,sign,u,v,o)


def negatives():
    import copy
    modifications=[('C',['0','0']),('F',['6','0']),('E',['6','1']),
                   ('F',['9','0']),('A',['0','0']),('D',['4','-3']),
                   ('D',['4','4']),('D',['4','0'])]
    for key,point in modifications:
        data=copy.deepcopy(EXAMPLE);data[key]=point;yield data
