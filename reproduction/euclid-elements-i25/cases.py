from fractions import Fraction as Q
from geometry import pair


def case(a=4,b=9,d=0,e=3):
    return {'ABC':{'a2':pair(Q(a)),'b2':pair(Q(b)),'dot':pair(Q(d))},
            'DEF':{'a2':pair(Q(a)),'b2':pair(Q(b)),'dot':pair(Q(e))}}


def positives():
    # |dot| <= ab/2, where adjacent squared lengths are a^2,b^2.
    return [case(a*a,b*b,Q(a*b*i,4),Q(a*b*j,4))
            for a in range(1,6) for b in range(1,6)
            for i in range(-2,3) for j in range(i+1,3)]
