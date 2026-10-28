from fractions import Fraction as Q
from geometry import example

def legal_cases():
    for A in [(0,0),(3,-2)]:
        for u,v in [((6,0),(0,3)),((4,1),(-1,3)),((-4,1),(2,5)),((2,3),(3,2)),((1,0),(0,-1))]:
            for t in [Q(1,5),Q(1,3),Q(1,2),Q(2,3),Q(4,5)]:
                yield example(A,u,v,t)

def illegal_cases():
    b=example()
    yield {**b,'K':(2,2)}
    yield example(t=Q(0)); yield example(t=Q(1)); yield example(t=Q(-1)); yield example(t=Q(2))
    yield example(u=(0,0)); yield example(u=(2,0),v=(3,0))
    yield {**b,'C':(9,9)}
    yield {**b,'K':(True,1)}; yield {**b,'K':(2.0,1)}; yield {**b,'K':('2',1)}
    yield {k:v for k,v in b.items() if k!='D'}
    yield {**b,'extra':0}
