"""Deterministic finite cases. They are regression evidence, not a theorem."""
from dataclasses import replace
from fractions import Fraction as R
from geometry import *


def positive_cases():
    vectors=[(1,0),(0,1),(2,3),(-3,2),(R(2,3),R(-5,7)),(-1,-1)]
    for origin in [(0,0),(7,-4),(R(1,3),R(2,5))]:
        for vx,vy in vectors:
            for factor in [R(1),R(1,10**80),R(10**80)]:
                a=point(*origin); b=add(a,point(factor*vx,factor*vy))
                for t in [R(0),R(1,4),R(1,2),R(1)]:
                    c=add(a,scale(t,sub(b,a)))
                    for h in [R(1,8),R(2)]:
                        for branch in [-1,1]:
                            yield a,b,c,h,construct(a,b,c,h,branch)


def rejected_cases():
    a,b,c=point(0,0),point(4,0),point(2,0); h=R(1,4)
    k=construct(a,b,c,h)
    for name,cert in [
      ('D_at_C',replace(k,d=c)),('E_on_D',replace(k,e=k.d)),
      ('unequal_cuts',replace(k,e=point(4,0))),
      ('F_at_C',replace(k,f=c)),('F_on_baseline',replace(k,f=point(3,0))),
      ('wrong_branch',replace(k,branch=-1)),('invalid_branch',replace(k,branch=True)),
      ('apex_shift',replace(k,f=add(k.f,point(1,0)))),
      ('perpendicular_but_not_equilateral',replace(k,f=point(2,1))),
      ('swapped_cut_labels',replace(k,d=k.e,e=k.d))]:
        yield name,a,b,c,h,cert
    yield 'input_rebinding',a,b,point(1,0),h,k
    yield 'cut_parameter_rebinding',a,b,c,R(1,2),k


def example_report():
    out={}
    for name,a,b,c,h in [
       ('interior',point(0,0),point(6,0),point(3,0),R(1,6)),
       ('endpoint',point(0,0),point(6,0),point(0,0),R(1,6)),
       ('oblique',point(-2,1),point(4,9),point(1,5),R(1,2))]:
        out[name]=[record(a,b,c,h,construct(a,b,c,h,s)) for s in (-1,1)]
    return out
