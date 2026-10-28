from fractions import Fraction as F
from geometry import add

def encode(p): return {k:[str(F(x)) for x in v] for k,v in p.items()}
def example(t=F(3)):
    return encode(dict(A=(1,3),B=(0,0),C=(4,0),D=(5,3),E=(1+4*t,3)))
def valid_cases():
    for u in [(4,0),(3,2),(-2,5)]:
        for h in [-2,-1,1,2]:
            for s in [-1,0,2]:
                b=(F(1,3),F(-2,5))
                a=add(b,(F(-u[1]*h,2)+u[0]*s,F(u[0]*h,2)+u[1]*s))
                c=add(b,u);d=add(a,u)
                for t in [F(-2),F(0),F(1,2),F(1),F(3)]:
                    e=add(a,(t*u[0],t*u[1]))
                    yield encode(dict(A=a,B=b,C=c,D=d,E=e))
def invalid_cases():
    import copy
    cases=[]
    for label,key,value in [
      ('zero base','C',[0,0]),('flat upper','A',[1,0]),
      ('wrong fourth vertex','D',[6,3]),('off upper line','E',[3,4]),
      ('opposite height, same unsigned ratio','E',[3,-3]),
      ('base apex','E',[3,0]),('crossed relabelling','D',[0,0]),
      ('float coordinate','A',[1.0,3]),('boolean coordinate','A',[True,3]),
      ('noncanonical fraction','A',['2/2',3])]:
        p=copy.deepcopy(example());p[key]=value;cases.append((label,p))
    return cases
