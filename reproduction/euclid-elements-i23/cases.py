from geometry import construct,verify

def positives():
    for D,E in [((2,0),(1,2)),((3,1),(-2,4)),((1,1),(-1,1)),((2,1),(-3,-1)),((1,0),(2,-3)),((2,3),(4,1))]:
        for A,B in [((0,0),(1,0)),((2,-3),(4,0)),((-1,2),(-3,1)),((0,0),(0,-2))]:
            for scale in (1,2,3):
                for side in (-1,1):
                    yield ((0,0),D,tuple(scale*x for x in E),A,B,side)

def negatives():
    base=[(0,0),(2,0),(1,2),(0,0),(1,0),1]
    for idx,value in [(1,(0,0)),(2,(0,0)),(2,(3,0)),(2,(-3,0)),(4,(0,0)),(5,0),(5,True),(5,'1'),(0,(True,0)),(1,(1.0,0)),(2,('x',1)),(3,(1,)),(4,(1,2,3)),(1,('1/0',0))]:
        a=base.copy();a[idx]=value;yield a

def run():
    n=0;irr=0;mirrors=0
    from fractions import Fraction
    from math import isqrt
    for args in positives():
        c=construct(*args)
        if not verify(c,*args):raise RuntimeError('certificate rejection')
        n+=1;d=Fraction(c['radicand'])
        irr+=isqrt(d.numerator)**2!=d.numerator or isqrt(d.denominator)**2!=d.denominator
        mirrors+=not c['signed_orientation_preserved']
    neg=0
    for args in negatives():
        try:construct(*args)
        except ValueError:neg+=1
        else:raise RuntimeError('invalid input accepted')
    return {'positive_certificates':n,'negative_inputs':neg,'irrational_scale_certificates':irr,'orientation_reversing_certificates':mirrors}
