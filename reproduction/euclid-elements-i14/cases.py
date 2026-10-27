"""Deterministic inputs; all records are generated, not random samples."""
from fractions import Fraction as F
from copy import deepcopy
from geometry import *


def positives():
    for b in [(0,0),(2,-3),(F(1,3),F(-2,5))]:
        for u in [(1,0),(0,1),(2,-1),(-3,2)]:
            p=(-u[1],u[0])
            for x,y in [(1,1),(-1,1),(0,2),(2,-1),(-2,-3)]:
                v=(x*u[0]+y*p[0],x*u[1]+y*p[1])
                for scale in [F(1,2),F(1),F(3)]:
                    a=tuple(b[i]+u[i] for i in range(2))
                    c=tuple(b[i]+v[i] for i in range(2))
                    d=tuple(b[i]-scale*v[i] for i in range(2))
                    yield (b,a,c,d)


def negatives():
    args=((0,0),(1,0),(1,1),(-1,-1))
    cert=build_certificate(*args)
    bad=[]
    for key in ['positive_scale','opposite_sides','supplementary','opposite_rays','conclusion_cross','conclusion_dot','angle_product','angle_pairs','side_crosses','inputs','conclusion']:
        c=deepcopy(cert);c[key]='tampered';bad.append((key,c,args))
    c=deepcopy(cert);del c['positive_scale'];bad.append(('missing',c,args))
    c=deepcopy(cert);c['unexpected']=True;bad.append(('extra',c,args))
    for idx,new in [(1,(2,0)),(2,(2,2)),(3,(-2,-2))]:
        altered=list(args);altered[idx]=new;bad.append(('input-binding',cert,tuple(altered)))
    return bad


def run_cases():
    pos=list(positives()); neg=negatives()
    for args in pos:
        c=build_certificate(*args)
        if not verify_certificate(c,*args):raise RuntimeError('positive replay failed')
    for name,c,args in neg:
        if verify_certificate(c,*args):raise RuntimeError('negative accepted: '+name)
    turns=[]
    for denominator in [8,12,20,32]:
        for numerator in range(1,denominator//2):
            alpha=F(numerator,denominator);beta=F(1,2)-alpha
            for signs in [(1,-1),(-1,1),(1,1),(-1,-1)]:
                d=angle_model(alpha,beta,*signs)
                if d['opposite_sides'] and not d['opposite_rays']:raise RuntimeError('turn model failed')
                turns.append(d)
    same=inspect_configuration((0,0),(1,0),(1,1),(-1,1))
    right=inspect_configuration((0,0),(1,0),(0,1),(0,2))
    if not same['supplementary'] or same['opposite_rays']:raise RuntimeError('same-side counterexample failed')
    if not right['supplementary'] or right['opposite_rays']:raise RuntimeError('coincident counterexample failed')
    return {'positive_certificates':len(pos),'negative_certificates':len(neg),
            'rational_turn_inputs':len(turns),'positive_replay':'passed','negative_rejection':'passed',
            'same_side_counterexample':encode(same),'coincident_right_counterexample':encode(right),
            'limitations':'finite teaching checks, not a general theorem proof or historical formalization'}
