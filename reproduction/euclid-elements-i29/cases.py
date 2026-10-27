from fractions import Fraction as Q

EXAMPLE={'G':['0','1'],'H':['1','0'],'B':['2','1'],'D':['4','0']}

def positives():
    for slope in range(-3,4):
        u=(Q(1),Q(slope))
        t=(-u[1]+Q(1,3)*u[0],u[0]+Q(1,3)*u[1])
        for scale in (Q(1,3),Q(1),Q(7,2)):
            for ray in (-1,1):
                for rotation in range(4):
                    for shift in ((Q(0),Q(0)),(Q(-5,3),Q(8,7))):
                        def point(x):
                            for _ in range(rotation): x=(-x[1],x[0])
                            return [str(x[i]+shift[i]) for i in range(2)]
                        yield {'G':point((Q(0),Q(0))),'H':point(t),'B':point(tuple(ray*z for z in u)),
                               'D':point(tuple(t[i]+scale*ray*u[i] for i in range(2)))}

def negatives():
    import copy
    edits=[('G',['1','0']),('B',['0','1']),('D',['1','0']),('B',['2','-1']),
           ('D',['-2','0']),('D',['4','1/1000000']),('B',['2','2']),('D',['4','2'])]
    for k,v in edits:
        x=copy.deepcopy(EXAMPLE);x[k]=v;yield x
