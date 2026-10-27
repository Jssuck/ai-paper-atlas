from fractions import Fraction as Q


def positives():
    # 7 slopes * 3 heights * 3 opposite ray scales * 4 similarities = 252.
    for slope in range(-3, 4):
        for height in (1, 2, 3):
            for scale in (Q(1,2), Q(1), Q(3)):
                p = [(0,0), (2,0), (slope,height), (2-scale*slope,-scale*height)]
                for mode in range(4):
                    def transform(z):
                        x,y=map(Q,z)
                        if mode==1: x,y=-y,x
                        if mode==2: x,y=x,-y
                        if mode==3: x,y=x/Q(3)+Q(2,5),y/Q(3)-Q(7,4)
                        return [str(x),str(y)]
                    yield dict(zip(('E','F','A','D'),map(transform,p)))


def negative_cases():
    return {
        'same_side_equal_ordinary_angles': {'E':['0','0'],'F':['2','0'],'A':['1','1'],'D':['1','1']},
        'opposite_side_unequal_angles': {'E':['0','0'],'F':['2','0'],'A':['1','1'],'D':['2','-1']},
        'supplementary_not_equal': {'E':['0','0'],'F':['2','0'],'A':['1','1'],'D':['3','-1']},
        'zero_transversal': {'E':['0','0'],'F':['0','0'],'A':['1','1'],'D':['-1','-1']},
        'zero_ray': {'E':['0','0'],'F':['2','0'],'A':['0','0'],'D':['1','-1']},
        'coincident_lines': {'E':['0','0'],'F':['2','0'],'A':['1','0'],'D':['3','0']},
    }
