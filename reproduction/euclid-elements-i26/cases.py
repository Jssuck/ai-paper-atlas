"""Own finite cases; canonical rational coordinate strings."""
from fractions import Fraction as F

def encode(points): return [[str(F(x)), str(F(y))] for x, y in points]
def case(p, q, side_case='included'):
    return {'triangle_1': encode(p), 'triangle_2': encode(q), 'side_case': side_case}
def example(side_case='included'):
    return case([(0,3),(0,0),(4,0)], [(10,3),(10,0),(6,0)], side_case)
def positive_cases():
    # 36 shapes x 3 rational isometries x 2 branches = 216.
    for x in range(-2,4):
        for y in range(1,7):
            p=[(x,y),(0,0),(4,0)]
            images=[p,[(10-a,b-3) for a,b in p],
                    [(F(3*a-4*b,5)+F(1,7), F(4*a+3*b,5)-F(2,3)) for a,b in p]]
            for q in images:
                for branch in ('included','opposite'): yield case(p,q,branch)
def negative_cases():
    p=[(0,3),(0,0),(4,0)]
    return {
      'angles_without_equal_side':case(p,[(0,6),(0,0),(8,0)]),
      'wrong_correspondence':case(p,[(0,0),(0,3),(4,0)]),
      'degenerate':case([(0,0),(1,0),(2,0)],p),
      'ssa_not_two_angles':case([(0,0),(6,0),(F(9,5),F(12,5))],
        [(0,0),(6,0),(F(63,25),F(84,25))],'opposite')}
