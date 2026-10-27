"""Deterministic finite examples, not an exhaustive theorem proof."""
from fractions import Fraction as F
from copy import deepcopy
from geometry import build_certificate, verify_certificate, angle_partition


def positive_cases():
    for bx,by in ((0,0),(3,-2),(F(1,3),F(-2,5))):
        for ux,uy in ((1,0),(0,1),(2,3),(-3,2)):
            for scale in (F(1,3),F(1),F(5,2)):
                for along in (-3,-1,0,1,3):
                    for side in (-2,1):
                        b=(bx,by); c=(bx+ux,by+uy)
                        d=(bx-scale*ux,by-scale*uy)
                        a=(bx+along*ux-side*uy,by+along*uy+side*ux)
                        yield b,c,d,a


def negative_cases():
    inputs=((0,0),(1,0),(-2,0),(1,2))
    cert=build_certificate(*inputs)
    variants=[]
    for field in ('orientation','first_rotation','second_rotation','rotation_product',
                  'expected_product','auxiliary_ray','perpendicular_dot',
                  'ray_order_case','conclusion','base_opposition','inputs'):
        bad=deepcopy(cert);bad[field]='tampered';variants.append((field,bad,inputs))
    bad=deepcopy(cert);bad['extra']='unbound';variants.append(('extra field',bad,inputs))
    bad=deepcopy(cert);del bad['conclusion'];variants.append(('missing field',bad,inputs))
    variants.append(('changed independent input',cert,((0,0),(1,0),(-2,0),(2,2))))
    variants.append(('same-direction base',cert,((0,0),(1,0),(2,0),(1,2))))
    variants.append(('collinear standing ray',cert,((0,0),(1,0),(-2,0),(3,0))))
    return variants


def evaluate():
    counts={};n=0
    for inputs in positive_cases():
        cert=build_certificate(*inputs)
        if not verify_certificate(cert,*inputs):raise RuntimeError('positive certificate rejected')
        counts[cert['ray_order_case']]=counts.get(cert['ray_order_case'],0)+1;n+=1
    rejected=[]
    for label,cert,inputs in negative_cases():
        if verify_certificate(cert,*inputs):raise RuntimeError('negative certificate accepted: '+label)
        rejected.append(label)
    angles=0
    for denominator in (8,12,20,100):
        for numerator in range(1,denominator//2):
            p=angle_partition(F(numerator,denominator))
            if p['sum']!=F(1,2):raise RuntimeError('bad angle partition')
            angles+=1
    return {'positive_certificates':n,'negative_certificates':len(rejected),
            'ray_order_counts':counts,'angle_partition_cases':angles,
            'negative_labels':rejected,
            'boundary':'Finite rational examples; algebra and angle axioms provide the general reasoning, not this count.'}
