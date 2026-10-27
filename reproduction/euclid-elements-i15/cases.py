"""Finite explicit fixtures; neither exhaustive geometry nor general proof."""
from fractions import Fraction as F
from geometry import certificate,verify,angle_ledger,cross
from copy import deepcopy


def positives():
    for e in [(0,0),(3,-2),(F(1,2),F(-2,3))]:
        for u in [(1,0),(1,2),(-2,1),(F(1,2),-1)]:
            for v in [(0,1),(2,1),(-1,2),(1,-3)]:
                if cross(u,v)==0: continue
                for k,l in [(1,1),(2,3),(F(2,3),F(5,4))]:
                    def p(w,s=1): return [str(e[i]+s*w[i]) for i in range(2)]
                    yield {'E':list(map(str,e)),'A':p(u),'B':p(u,-k),'C':p(v),'D':p(v,-l)}


def negative_inputs():
    base=next(positives())
    cases=[]
    for key,val in [('A',['0','0']),('B',['1','0']),('C',['1','0']),('D',['0','1']),
                    ('D',['2','3']),('A',[True,0]),('A',[1.0,0]),('A',['NaN',0]),
                    ('A',['1/0',0]),('E',[0]),('B',[None,0])]:
        d=deepcopy(base);d[key]=val;cases.append(d)
    d=deepcopy(base);del d['A'];cases.append(d)
    d=deepcopy(base);d['extra']=[0,0];cases.append(d)
    return cases


def run():
    n=0
    for data in positives():
        c=certificate(data)
        if not verify(data,c): raise RuntimeError('positive rejected')
        n+=1
    negatives=negative_inputs()
    for data in negatives:
        if verify(data,{}): raise RuntimeError('negative accepted')
        try: certificate(data)
        except (ValueError,TypeError): pass
        else: raise RuntimeError('invalid input certified')
    ledgers=0
    for den in range(2,14):
        for num in range(1,2*den):
            x=F(num,den);angle_ledger(str(x),str(2-x),str(x));ledgers+=1
    return {'positive_certificates':n,'negative_inputs':len(negatives),'angle_ledgers':ledgers,
            'finite_checks_are_not_general_proofs':True}
