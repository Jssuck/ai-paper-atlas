from fractions import Fraction as Q
from geometry import *

def valid_cases():
    for A in [(0,0),(2,-3),(Q(1,3),Q(-2,5))]:
        for u in [(3,0),(1,2),(-2,3),(Q(2,3),Q(-4,5))]:
            for k in [Q(1,2),Q(4,3),Q(3)]:
                for sign in [-1,1]:
                    yield A,add(A,u),add(A,mul(sign*k,rot(u)))

def invalid_cases():
    return [((0,0),(0,0),(0,1)),((0,0),(1,0),(0,0)),((0,0),(1,0),(1,1)),((0,0),(1,0),(2,0)),((True,0),(1,0),(0,1)),((0,0),(1.0,0),(0,1)),((0,0),(1,0),(0,float('nan'))),((0,),(1,0),(0,1)),(('0',0),(1,0),(0,1)),(None,(1,0),(0,1)),((0,0),(1,0),[0,True]),((0,0),(1,0),(0,1,2))]
