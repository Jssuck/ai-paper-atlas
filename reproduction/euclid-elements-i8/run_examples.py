"""Bounded exact enumeration; finite testing is not a proof of SSS."""
import json
from itertools import product
from geometry import *

def run():
    points=list(product(range(-1,2),repeat=2)); origin=(0,0)
    triangles=[(origin,u,v) for u in points for v in points if det(u,v)!=0]
    accepted=reflected=direct=rejected=0
    for s in triangles:
        if gram(s)!=gram_from_sides(sides_squared(s)): raise RuntimeError('polarization')
        for t in triangles:
            match=sides_squared(s)==sides_squared(t)
            try: m,tr=certificate(s,t)
            except CorrespondenceMismatch:
                if match: raise RuntimeError('false negative')
                rejected+=1; continue
            if not match or not verify_certificate(s,t,m,tr): raise RuntimeError('invalid acceptance')
            if angle_signature(s)!=angle_signature(t): raise RuntimeError('angle mismatch')
            accepted+=1
            if determinant(m)==1: direct+=1
            elif determinant(m)==-1: reflected+=1
            else: raise RuntimeError('orientation')
    p=((0,0),(3,0),(0,4)); q=((0,0),(3,0),(F(12,5),F(16,5)))
    return {'grid':'integer coordinates -1..1; first vertex (0,0)',
            'nondegenerate_ordered_triangles':len(triangles),'ordered_pairs':len(triangles)**2,
            'accepted_equal_ordered_sides':accepted,'det_plus_one':direct,'det_minus_one':reflected,
            'rejected_side_mismatch':rejected,'two_side_counterexample':{
                'source_squares':list(map(str,sides_squared(p))),'target_squares':list(map(str,sides_squared(q))),
                'source_angle_signature':list(map(str,angle_signature(p))),
                'target_angle_signature':list(map(str,angle_signature(q)))},
            'scope':'finite rational teaching checks, not a general proof or historical superposition implementation'}
if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
