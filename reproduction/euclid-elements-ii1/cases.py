from fractions import Fraction as Q
from geometry import add,mul

def valid_cases():
    for B in [(0,0),(2,-3),(Q(1,3),Q(-2,5))]:
        for u in [(6,0),(0,6),(3,4),(-2,5)]:
            for k in [Q(1,2),Q(-2,3)]:
                v=mul(k,(-u[1],u[0]))
                for cuts in [[],[Q(1,2)],[Q(1,6),Q(1,2)],[Q(1,5),Q(2,5),Q(4,5)]]:
                    yield B,add(B,u),add(B,v),cuts

def invalid_cases():
    yield (0,0),(0,0),(0,2),[]
    yield (0,0),(6,0),(0,0),[]
    yield (0,0),(6,0),(1,2),[]
    for cuts in [[0],[1],[-1],[2],[Q(1,2),Q(1,2)],[Q(2,3),Q(1,3)],[True],[0.5],['1/2'],None]:
        yield (0,0),(6,0),(0,2),cuts
    yield (False,0),(6,0),(0,2),[]
    yield (0,0),(6.0,0),(0,2),[]
    yield (0,0),(6,0),(0,2,3),[]
