"""Finite rational configurations and explicitly invalid premises."""
from geometry import construct, verify

def positives():
    for x in (-4,-1,0,2,5):
        for y in (-3,-1,1,4):
            for length in (1,3,7):
                for extension in (1,2,5):
                    yield {'A':[x,y], 'B':[0,0], 'C':[length,0], 'D':[length+extension,0]}


def negatives():
    base={'A':[1,2], 'B':[0,0], 'C':[3,0], 'D':[4,0]}
    changes=[('A',[1,0]),('A',[0,0]),('A',[3,0]),('B',[3,0]),
             ('D',[3,0]),('D',[2,0]),('D',[-1,0]),('D',[4,1]),
             ('A',[True,2]),('A',[1.0,2]),('A',['1/0',2]),('A',[1]),
             ('A',(1,2)),('A',['no',2])]
    for key,value in changes:
        yield dict(base, **{key:value})
    yield {k:v for k,v in base.items() if k!='D'}
    yield dict(base, extra=1)


def run_cases():
    good=bad=0
    for p in positives():
        if not verify(p,construct(p)): raise RuntimeError('positive certificate failed')
        good+=1
    for p in negatives():
        try: construct(p)
        except ValueError: bad+=1
        else: raise RuntimeError('invalid premise accepted')
    return {'positive_certificates':good, 'negative_inputs':bad,
            'finite_only':True, 'arithmetic':'fractions.Fraction; no angle floating point'}
