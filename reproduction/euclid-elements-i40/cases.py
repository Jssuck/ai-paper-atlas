"""Deterministic finite examples of the explicitly generalized six-point model."""
def build(a=1,d=5,h=2,k=None,e=4,length=3,reverse=False,transform=0):
    if k is None:k=h
    p={'A':[a,h],'B':[0,0],'C':[length,0],'D':[d,k],'E':[e,0],'F':[e+length,0]}
    if reverse:p['E'],p['F']=p['F'],p['E']
    if transform==1:p={key:[-y+7,x-3] for key,(x,y) in p.items()}
    if transform==2:p={key:[x+2,-y+5] for key,(x,y) in p.items()}
    return p
EXAMPLE=build()

def positives():
    for e in [-5,-3,-1,0,2,3,6]:
        for reverse in [False,True]:
            for h in [-3,2]:
                for d in [1,5]:
                    for transform in [0,1,2]:yield build(e=e,reverse=reverse,h=h,d=d,transform=transform)

def negatives():
    p=build();p['C']=[0,0];yield 'zero BC',p
    p=build();p['F']=p['E'][:];yield 'zero EF',p
    p=build();p['F']=[8,0];yield 'unequal bases',p
    p=build();p['E'][1]=1;p['F'][1]=1;yield 'parallel but not collinear bases',p
    p=build();p['F'][1]=1;yield 'noncollinear endpoint',p
    yield 'opposite sides',build(k=-2)
    yield 'degenerate A',build(h=0,k=2)
    yield 'degenerate D',build(k=0)
    yield 'unequal areas',build(k=4)
