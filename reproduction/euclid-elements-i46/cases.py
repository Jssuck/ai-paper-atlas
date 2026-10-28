from fractions import Fraction as Q

def valid_cases():
    for A in [(0,0),(2,-3),(Q(1,3),Q(-2,5))]:
        for u in [(1,0),(0,2),(-2,0),(0,-3),(3,4),(-3,4),(Q(2,3),Q(1,5)),(7,-2)]:
            for s in (-1,1):
                yield A,(A[0]+u[0],A[1]+u[1]),s
INVALID=[('zero',(0,0),(0,0),1),('bool-coordinate',(True,0),(2,0),1),
 ('float',(0.,0),(2,0),1),('string',('0',0),(2,0),1),('missing',(0,),(2,0),1),
 ('extra',(0,0,0),(2,0),1),('none',None,(2,0),1),('side-zero',(0,0),(2,0),0),
 ('side-two',(0,0),(2,0),2),('side-bool',(0,0),(2,0),True),
 ('side-fraction',(0,0),(2,0),Q(1)),('nan',(0,0),(float('nan'),0),1)]
