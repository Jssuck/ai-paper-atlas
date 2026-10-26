import json
from fractions import Fraction as F
from itertools import product
from geometry import *

def main():
    a=(0,0); pts=list(product(range(-3,4),repeat=2))
    counts=dict(non_degenerate=0,equal_base_angles=0,equal_opposite_sides=0,violations=0)
    for b,c in product(pts,repeat=2):
        if not signed_double_area(a,b,c):continue
        q=triangle_certificate(a,b,c);counts['non_degenerate']+=1
        counts['equal_base_angles']+=q['base_angles_equal']; counts['equal_opposite_sides']+=q['opposite_sides_equal']
        counts['violations']+=not q['implication_holds']
    cuts=0; bad=0; impossible=0
    for length in range(2,12):
        for height in range(1,length):
            for sx,sy in product((-1,1),repeat=2):
                b=(sx*length,0);c=(0,sy*height)
                d=cut_from_rational_ratio(a,b,c,F(height,length))
                q=strict_cut_certificate(a,b,c,d); cuts+=1
                bad+=not(q['valid_cut'] and q['proper_area'] and q['area_ratio']==F(height,length))
                impossible+=q['contradiction_premises']
    factors=0;factor_bad=0
    for x,y,z in product(range(1,11),repeat=3):
        if x+y<=z or x+z<=y or y+z<=x:continue
        q=factor_certificate(x,y,z);factors+=1
        factor_bad+=not(q['identity_holds'] and q['strict_factor_positive'] and q['implication_holds'])
    result=dict(triangles=counts,strict_cuts=dict(cases=cuts,violations=bad,contradiction_premises_realized=impossible),side_factor=dict(cases=factors,violations=factor_bad),examples=dict(isosceles=triangle_certificate((0,3),(-2,0),(2,0)),strict_cut=strict_cut_certificate((0,0),(5,0),(0,3),(2,0)),supplementary_angles_equal=angle_equal((1,0),(1,1),(1,0),(-1,1))))
    if counts['violations'] or bad or impossible or factor_bad:raise RuntimeError('finite check failed')
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
if __name__=='__main__':main()
