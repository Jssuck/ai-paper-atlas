"""Finite exact families, not an exhaustive geometry search."""
from fractions import Fraction as Q
from itertools import product

def sample(case='corresponding'):
    return {'E':['0','0'],'F':['2','0'],'B':['1','1'],'D':['3','1'],'case':case}

def positives():
    for mode,x,y,scale,turn,shift in product(('corresponding','interior_sum'),range(-3,4),(-2,-1,1,2),(Q(1,2),Q(1),Q(3)),(0,1),(0,3)):
        def transform(a,b):
            if turn: a,b=-b,a
            return [str(a+shift),str(b-shift)]
        yield {'E':transform(0,0),'F':transform(2,0),'B':transform(x,y),
               'D':transform(2+scale*x,scale*y),'case':mode}

def negative_cases():
    cases={}
    for mode in ('corresponding','interior_sum'):
        for name,changes in {
            'wrong_side_equal_angles':{'D':['3','-1']},
            'supplement_not_equal':{'D':['1','1']},
            'near_parallel':{'D':['3000001/1000000','1']},
            'same_intersection':{'F':['0','0']},
            'zero_ray':{'B':['0','0']},
            'ray_on_transversal':{'D':['3','0']},
        }.items():
            d=sample(mode);d.update(changes);cases[mode+':'+name]=d
    return cases
