"""Deterministic finite coverage, not a general proof."""
from geometry import construct,verify,ledger

def positives():
    for x in (-3,-1,0,2,5):
        for y in (-4,-1,1,3):
            for length in (1,3,7):
                for offset in (0,5):
                    yield {'A':[x+offset,y],'B':[offset,0],'C':[length+offset,0]}

def negatives():
    return [None,{}, {'A':[0,0],'B':[1,0],'C':[2,0]}, {'A':[0,0],'B':[0,0],'C':[1,1]},
      {'A':[True,1],'B':[0,0],'C':[2,0]}, {'A':[1.0,1],'B':[0,0],'C':[2,0]},
      {'A':['nan',1],'B':[0,0],'C':[2,0]}, {'A':['1/0',1],'B':[0,0],'C':[2,0]},
      {'A':[1,2,3],'B':[0,0],'C':[2,0]}, {'A':(1,2),'B':[0,0],'C':[2,0]},
      {'A':[1,2],'B':[0,0],'C':[2,0],'D':[3,0]}, {'A':['x',2],'B':[0,0],'C':[2,0]}]

def run_cases():
    count=0
    for p in positives():
        c=construct(p)
        if not verify(p,c): raise RuntimeError('certificate failure')
        count+=1
    neg=0
    for p in negatives():
        try: construct(p)
        except ValueError: neg+=1
        else: raise RuntimeError('invalid input accepted')
    ledgers=0
    for r in (1,2,5):
        for i in range(1,8):
            e=f'{i*r}/4'
            for j in range(1,i):
                ledger(f'{j*r}/4',f'{(8-i)*r}/4',e,r);ledgers+=1
    return {'positive_certificates':count,'pair_checks':3*count,'negative_inputs':neg,'angle_ledgers':ledgers}
