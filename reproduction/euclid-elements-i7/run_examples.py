"""Deterministic finite checks. No finite count proves the universal theorem."""
import json
from itertools import product
from fractions import Fraction as F
from geometry import certificate,reflect,verify_claim,distance2

def main():
    points=list(product(range(-2,3), repeat=2))
    baselines=[((0,0),(2,0)),((1,-1),(1,2)),((-1,-1),(2,1)),((F(1,2),F(-1,3)),(F(5,3),F(2,7)))]
    count=valid=equal=mirrors=violations=0
    keys=('distance_difference_identity','norm_cross_identity_c','norm_cross_identity_d','reconstruction_c','reconstruction_d')
    for A,B in baselines:
        for C,D in product(points,repeat=2):
            r=certificate(A,B,C,D);count+=1
            equal+=r['equal_a'] and r['equal_b'];valid+=r['premises']
            mirrors+=r['equal_a'] and r['equal_b'] and r['distinct']
            violations+=not r['implication'] or not all(r[k] for k in keys)
            if r['premises'] and not all(r[k] for k in ('projection_equal','height_square_equal','signed_height_equal','conclusion')):violations+=1
    reflection_count=reflection_errors=0
    for A,B in baselines:
        for C in points:
            D=reflect(A,B,C); r=certificate(A,B,C,D); reflection_count+=1
            reflection_errors+=not (r['equal_a'] and r['equal_b'] and r['cross_c']==-r['cross_d'] and reflect(A,B,D)==C)
    negatives={}
    A=(0,0);B=(4,0);C=(1,2)
    for label,D in [('mirror',(1,-2)),('wrong_a',(4,2)),('wrong_b',(-1,2)),('swapped_correspondence',(3,2)),('on_baseline',(1,0))]:
        r=certificate(A,B,C,D);negatives[label]={k:r[k] for k in ('equal_a','equal_b','same_side','premises','conclusion','implication')}
        if verify_claim(A,B,C,D):raise RuntimeError('negative accepted')
    result=dict(candidate_pairs=count,equal_distance_pairs=equal,strict_same_side_premise_pairs=valid,distinct_equal_distance_pairs=mirrors,identity_or_implication_violations=violations,reflection_checks=reflection_count,reflection_errors=reflection_errors,negative_examples=negatives)
    if violations or reflection_errors:raise RuntimeError('finite verification failed')
    return result
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
