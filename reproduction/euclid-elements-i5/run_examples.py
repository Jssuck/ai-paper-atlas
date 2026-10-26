"""Run a finite rational family and deliberate invalid certificate variants."""
import json
from fractions import Fraction as Q
from itertools import product
from geometry import certificate, family, transform, squared


def run():
    values=[Q(1,2),Q(1),Q(3,2),Q(2),Q(3)]
    ts=[Q(5,4),Q(3,2),Q(2),Q(3)]
    rotations=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5))]
    offsets=[(0,0),(Q(2,3),Q(-5,7))]
    accepted=rejected=total=0
    for b,h,t,(u,v),ori,offset in product(values,values,ts,rotations,(-1,1),offsets):
        p=transform(family(b,h,t),u,v,ori,offset)
        total+=1
        if not certificate(*p)['accepted']: raise RuntimeError('Valid family rejected')
        accepted+=1
        a,left,right,f,g=p
        variants=[(a,left,right,left,g),(a,left,right,f,right),
                  (a,left,right,g,f),(a,left,right,a,g)]
        for variant in variants:
            if certificate(*variant)['accepted']: raise RuntimeError('Invalid order accepted')
            rejected+=1
    example=family(3,4,2)
    a,b,c,f,g=example
    return {'scope':'finite rational teaching family, not a general theorem proof',
            'base_parameter_triples':100,'orthogonal_maps_per_triple':6,
            'translations_per_map':2,'valid_certificates':accepted,
            'invalid_variants_rejected':rejected,'violations':0,
            'example_points':[[str(x) for x in p] for p in example],
            'example_squared_lengths':{label:str(squared(p,q)) for label,p,q in
                 [('AB',a,b),('AC',a,c),('AF',a,f),('AG',a,g),('BF',b,f),('CG',c,g),('FC',f,c),('GB',g,b)]},
            'example_certificate':certificate(*example)}

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
