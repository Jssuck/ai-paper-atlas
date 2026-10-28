from fractions import Fraction as Q
from geometry import add,mul,rotate

def valid_cases():
    # A deliberately generated test family, not the public constructor's admission rule.
    for a in [(0,0),(2,-3),(Q(1,3),Q(-2,5))]:
        for u in [(1,0),(2,1),(Q(3,2),Q(-1,3)),(-1,2)]:
            for t in [Q(1,2),Q(1),Q(4,3)]:
                for sign in [-1,1]:
                    yield a,add(a,u),add(a,mul(sign*t,rotate(u)))

def invalid_cases():
    return [((0,0),(0,0),(0,1)),((0,0),(1,0),(0,0)),((0,0),(1,0),(2,0)),
      ((0,0),(1,0),(1,1)),((0,0),(3,0),(1,4)),((0,0),(1,0),(Q(1,10**20),1)),
      ((False,0),(1,0),(0,1)),((0.,0),(1,0),(0,1)),((0,),(1,0),(0,1)),
      ('00',(1,0),(0,1)),(None,(1,0),(0,1)),((0,0),('1',0),(0,1))]
